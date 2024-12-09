import socket
import threading
import subprocess
import os


class Server:
    def __init__(self, host="127.0.0.1", port=5555):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False

    def handle_client(self, client_socket):
        """Gère une connexion client."""
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

            # Sauvegarder le fichier temporairement
            temp_filename = f"temp_{filename}"
            with open(temp_filename, 'wb') as f:
                f.write(file_content)
            print(f"Fichier {temp_filename} sauvegardé.")

            # Exécuter le fichier Python
            python_path = r'C:\Users\julie\AppData\Local\Programs\Python\Python312\python.exe'
            result = subprocess.run([python_path, temp_filename], capture_output=True, text=True)

            # Envoyer le résultat ou l'erreur
            if result.returncode == 0:
                client_socket.sendall(f"Exécution réussie :\n{result.stdout}".encode('utf-8'))
            else:
                client_socket.sendall(f"Erreur lors de l'exécution :\n{result.stderr}".encode('utf-8'))

            # Supprimer le fichier temporaire
            os.remove(temp_filename)

        except Exception as e:
            print(f"Erreur serveur : {e}")
            client_socket.sendall(f"Erreur serveur : {e}".encode('utf-8'))
        finally:
            client_socket.close()

    def start(self):
        """Démarre le serveur."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            print(f"Serveur démarré sur {self.host}:{self.port}")

            # Lancer un thread pour surveiller les commandes manuelles
            stop_thread = threading.Thread(target=self.wait_for_stop_command, daemon=True)
            stop_thread.start()

            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"Connexion établie avec {client_address}")
                    client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                    client_handler.start()
                except socket.error:
                    break

        except Exception as e:
            print(f"Erreur serveur : {e}")
        finally:
            self.stop()

    def wait_for_stop_command(self):
        """Attend une commande manuelle pour arrêter le serveur."""
        while self.running:
            command = input("Tapez 'stop' pour arrêter le serveur : ").strip().lower()
            if command == "stop":
                print("Arrêt du serveur demandé...")
                self.stop()
                break

    def stop(self):
        """Arrête le serveur proprement."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Serveur arrêté proprement.")


if __name__ == "__main__":
    server = Server()
    server.start()
