import socket
import threading
import subprocess
import os


def handle_client(client_socket):
    try:
        # Recevoir le nom du fichier
        filename = client_socket.recv(1024).decode('utf-8')
        print(f"Fichier reçu : {filename}")

        if not filename.endswith('.py'):
            client_socket.sendall("Erreur: Seuls les fichiers .py sont acceptés.".encode('utf-8'))
            return

        # Recevoir le contenu du fichier
        file_content = b""
        while True:
            data = client_socket.recv(4096)
            if data == b"END":
                break
            file_content += data

        temp_filename = f"temp_{filename}"
        with open(temp_filename, 'wb') as f:
            f.write(file_content)
        print(f"Fichier {temp_filename} sauvegardé.")

        # Chemin complet vers l'exécutable Python
        python_path = r'python'

        # Exécuter le fichier Python
        result = subprocess.run([python_path, temp_filename], capture_output=True, text=True)
        if result.returncode == 0:
            client_socket.sendall(f"\n{result.stdout}".encode('utf-8'))
        else:
            client_socket.sendall(f"Erreur lors de l'exécution :\n{result.stderr}".encode('utf-8'))

        # Supprimer le fichier temporaire
        os.remove(temp_filename)

    except Exception as e:
        print(f"Erreur serveur : {e}")
        client_socket.sendall(f"Erreur serveur : {e}".encode('utf-8'))
    finally:
        client_socket.close()


def start_server():
    host = '127.0.0.1'
    port = 4200

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        print(f"Serveur démarré sur {host}:{port}")
        server_socket.listen(5)

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connexion établie avec {client_address}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

    except Exception as e:
        print(f"Erreur serveur : {e}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
