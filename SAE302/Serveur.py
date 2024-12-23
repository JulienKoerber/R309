import socket
import threading
import subprocess
import sys
import os
import psutil

MASTER_IP = "127.0.0.1"
MASTER_PORT = 5000
MAX_LOCAL_TASKS = 2  
SLAVE_SERVERS = [
    ("127.0.0.1", 6000),
]

current_local_tasks = 0
current_lock = threading.Lock()

def cleanup_java_files():
    if os.path.exists("Main.java"):
        os.remove("Main.java")
    if os.path.exists("Main.class"):
        os.remove("Main.class")

def cleanup_c_files():
    if os.path.exists("main.c"):
        os.remove("main.c")
    if os.path.exists("main.out"):
        os.remove("main.out")

def execute_code(language, code_str):
    if language == "cpu_load" and code_str == "GET_CPU_LOAD":
        cpu_percent = psutil.cpu_percent(interval=0.5)
        return f"Charge CPU actuelle: {cpu_percent:.2f}%"

    try:
        if language == "python":
            result = subprocess.run(
                ["python3", "-c", code_str],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=20 
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return "Erreur d'exécution Python:\n" + result.stderr
        elif language == "java":
            with open("Main.java", "w", encoding="utf-8") as f:
                f.write(code_str)
            compile_res = subprocess.run(
                ["javac", "Main.java"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=20
            )
            if compile_res.returncode != 0:
                cleanup_java_files()
                return "Erreur de compilation Java:\n" + compile_res.stderr

            run_res = subprocess.run(
                ["java", "Main"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=20
            )
            cleanup_java_files()
            if run_res.returncode == 0:
                return run_res.stdout
            else:
                return "Erreur d'exécution Java:\n" + run_res.stderr

        elif language == "c":
            with open("main.c", "w", encoding="utf-8") as f:
                f.write(code_str)
            compile_res = subprocess.run(
                ["gcc", "main.c", "-o", "main.out"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=20
            )
            if compile_res.returncode != 0:
                cleanup_c_files()
                return "Erreur de compilation C:\n" + compile_res.stderr

            run_res = subprocess.run(
                ["./main.out"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=20
            )
            cleanup_c_files()
            if run_res.returncode == 0:
                return run_res.stdout
            else:
                return "Erreur d'exécution C:\n" + run_res.stderr

        else:
            return "Langage non supporté."
    except subprocess.TimeoutExpired:
        if language == "java":
            cleanup_java_files()
        if language == "c":
            cleanup_c_files()
        return f"Erreur : temps d'exécution dépassé ({language.capitalize()})."
    except Exception as e:
        if language == "java":
            cleanup_java_files()
        if language == "c":
            cleanup_c_files()
        return f"Erreur interne ({language.capitalize()}) : {str(e)}"

def delegate_to_slave(language, code_str):
    print("Tentative de délégation aux esclaves...")
    lang_bytes = language.encode('utf-8')
    lang_size = len(lang_bytes)
    code_bytes = code_str.encode('utf-8')
    code_size = len(code_bytes)

    for ip, port in SLAVE_SERVERS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((ip, port))
                s.sendall(lang_size.to_bytes(4, 'big'))
                s.sendall(lang_bytes)
                s.sendall(code_size.to_bytes(4, 'big'))
                s.sendall(code_bytes)

                resp_size_data = s.recv(4)
                if len(resp_size_data) < 4:
                    print(f"Esclave {ip}:{port} a retourné une réponse invalide.")
                    continue
                resp_size = int.from_bytes(resp_size_data, 'big')
                response = b''
                while len(response) < resp_size:
                    chunk = s.recv(resp_size - len(response))
                    if not chunk:
                        break
                    response += chunk
                print(f"Réponse de l'esclave {ip}:{port} reçue.")
                return response.decode('utf-8')
        except Exception as e:
            print(f"Impossible de joindre l'esclave {ip}:{port}: {e}")
            continue

    return "Erreur : Le serveur esclave n'est pas disponible pour traiter la demande."

def handle_client(conn, addr):
    global current_local_tasks
    print(f"Connexion du client {addr}")
    try:
        lang_size_data = conn.recv(4)
        if len(lang_size_data) < 4:
            return
        lang_size = int.from_bytes(lang_size_data, 'big')
        lang_bytes = b''
        while len(lang_bytes) < lang_size:
            chunk = conn.recv(lang_size - len(lang_bytes))
            if not chunk:
                return
            lang_bytes += chunk
        language = lang_bytes.decode('utf-8')

        size_data = conn.recv(4)
        if len(size_data) < 4:
            return
        code_size = int.from_bytes(size_data, 'big')
        code = b''
        while len(code) < code_size:
            chunk = conn.recv(code_size - len(code))
            if not chunk:
                return
            code += chunk
        code_str = code.decode('utf-8')

        print(f"Langage reçu: {language}, code de longueur {len(code_str)}")

        with current_lock:
            local_load = current_local_tasks

        if language == "cpu_load" and code_str == "GET_CPU_LOAD":
            response = execute_code(language, code_str)
        else:
            if local_load >= MAX_LOCAL_TASKS and SLAVE_SERVERS:
                print("Charge élevée, tentative de délégation...")
                response = delegate_to_slave(language, code_str)
            else:
                with current_lock:
                    current_local_tasks += 1
                print("Exécution du code...")
                response = execute_code(language, code_str)
                with current_lock:
                    current_local_tasks -= 1

        resp_bytes = response.encode('utf-8')
        resp_size = len(resp_bytes)
        conn.sendall(resp_size.to_bytes(4, 'big'))
        conn.sendall(resp_bytes)

    except Exception as e:
        print("Erreur handle_client:", e)
    finally:
        conn.close()
        print(f"Connexion avec {addr} terminée.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((MASTER_IP, MASTER_PORT))
        s.listen(5)
        print(f"Serveur maître en écoute sur {MASTER_IP} : {MASTER_PORT}, MAX_LOCAL_TASKS={MAX_LOCAL_TASKS}")
        try:
            while True:
                conn, addr = s.accept()
                t = threading.Thread(target=handle_client, args=(conn, addr))
                t.start()
        except KeyboardInterrupt:
            print("\nArrêt du serveur maître...")
        except Exception as e:
            print("Erreur inattendue :", e)
        finally:
            s.close()
            print("Socket fermé, serveur terminé.")

if __name__ == "__main__":
    main()
