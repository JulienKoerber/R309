import socket
import threading
import subprocess
import sys

# Paramètres du serveur maître
MASTER_IP = "0.0.0.0"
MASTER_PORT = 5000
MAX_LOCAL_TASKS = 2  # Seuil pour déléguer aux esclaves

# Liste des esclaves (peut être étendue)
SLAVE_SERVERS = [
    ("127.0.0.1", 6000),
    # ("127.0.0.1", 6001),  # Ajouter d’autres esclaves ici si besoin
]

current_local_tasks = 0
current_lock = threading.Lock()

def execute_code_locally(code_str):
    """Exécute du code Python localement via subprocess."""
    try:
        result = subprocess.run(
            ["python3", "-c", code_str],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return "Erreur d'exécution:\n" + result.stderr
    except subprocess.TimeoutExpired:
        return "Erreur : temps d'exécution dépassé."

def delegate_to_slave(code_str):
    """Délègue l'exécution du code à un esclave disponible."""
    code_bytes = code_str.encode('utf-8')
    for ip, port in SLAVE_SERVERS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((ip, port))
                # Envoi du code
                s.sendall(len(code_bytes).to_bytes(4, 'big'))
                s.sendall(code_bytes)
                
                # Réception de la réponse
                resp_size_data = s.recv(4)
                if len(resp_size_data) < 4:
                    continue
                resp_size = int.from_bytes(resp_size_data, 'big')
                response = b''
                while len(response) < resp_size:
                    chunk = s.recv(resp_size - len(response))
                    if not chunk:
                        break
                    response += chunk
                return response.decode('utf-8')
        except Exception:
            # Essayer l'esclave suivant
            continue
    return "Erreur : Aucun esclave disponible pour traiter la demande."

def handle_client(conn, addr):
    global current_local_tasks
    try:
        # Réception du code
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

        # Décision d'exécution
        with current_lock:
            local_load = current_local_tasks

        if local_load >= MAX_LOCAL_TASKS and SLAVE_SERVERS:
            response = delegate_to_slave(code_str)
        else:
            with current_lock:
                current_local_tasks += 1
            response = execute_code_locally(code_str)
            with current_lock:
                current_local_tasks -= 1

        # Envoi de la réponse au client
        resp_bytes = response.encode('utf-8')
        resp_size = len(resp_bytes)
        conn.sendall(resp_size.to_bytes(4, 'big'))
        conn.sendall(resp_bytes)

    except Exception as e:
        print("Erreur handle_client:", e)
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((MASTER_IP, MASTER_PORT))
        s.listen(5)
        print(f"Serveur maître en écoute sur {MASTER_IP}:{MASTER_PORT}")
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
