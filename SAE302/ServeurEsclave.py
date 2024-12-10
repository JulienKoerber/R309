import socket
import threading
import subprocess

SLAVE_IP = "0.0.0.0"
SLAVE_PORT = 6000

def execute_code(code_str):
    """Exécute le code Python reçu."""
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

def handle_request(conn):
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

        # Exécution
        response = execute_code(code_str)

        # Envoi de la réponse
        resp_bytes = response.encode('utf-8')
        resp_size = len(resp_bytes)
        conn.sendall(resp_size.to_bytes(4, 'big'))
        conn.sendall(resp_bytes)

    except Exception as e:
        print("Erreur handle_request:", e)
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SLAVE_IP, SLAVE_PORT))
        s.listen(5)
        print(f"Serveur esclave en écoute sur {SLAVE_IP}:{SLAVE_PORT}")
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_request, args=(conn,))
            t.start()

if __name__ == "__main__":
    main()
