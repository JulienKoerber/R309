import socket
import threading
import subprocess
import os

SLAVE_IP = "127.0.0.1"
SLAVE_PORT = 6000

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

def handle_request(conn, addr):
    print(f"Connexion du maître: {addr}")
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

        print(f"Reçu code {language}, longueur {len(code_str)}")

        response = execute_code(language, code_str)

        resp_bytes = response.encode('utf-8')
        resp_size = len(resp_bytes)
        conn.sendall(resp_size.to_bytes(4, 'big'))
        conn.sendall(resp_bytes)
        print("Réponse envoyée au maître.")

    except Exception as e:
        print("Erreur handle_request:", e)
    finally:
        conn.close()
        print(f"Connexion avec {addr} terminée.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SLAVE_IP, SLAVE_PORT))
        s.listen(5)
        print(f"Serveur Esclave en écoute sur {SLAVE_IP} : {SLAVE_PORT}")
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_request, args=(conn, addr))
            t.start()

if __name__ == "__main__":
    main()
