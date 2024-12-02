import socket
import threading
import os


def handle_client(client_socket, client_address):
    """Gère la communication avec un client."""
    print(f"Connexion acceptée de {client_address}")
    try:
        # Réception du nom du fichier
        filename = client_socket.recv(1024).decode('utf-8')
        if not filename.endswith('.py'):
            client_socket.sendall("Erreur : Seuls les fichiers .py sont acceptés.".encode('utf-8'))
            return

        # Réception des données du fichier
        with open(f"reçu_{filename}", 'wb') as file:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                file.write(data)

        print(f"Fichier reçu et enregistré sous: reçu_{filename}")

        # Lecture et exécution du fichier Python
        try:
            with open(f"reçu_{filename}", 'r') as f:
                exec(f.read())
            client_socket.sendall("Fichier exécuté avec succès.".encode('utf-8'))
        except Exception as e:
            error_message = f"Erreur lors de l'exécution : {e}"
            print(error_message)
            client_socket.sendall(error_message.encode('utf-8'))
    except Exception as e:
        print(f"Erreur avec le client {client_address} : {e}")
    finally:
        client_socket.close()
        print(f"Connexion avec {client_address} terminée.")


def start_server(host="0.0.0.0", port=4200):
    """Démarre le serveur avec gestion automatique du port."""
    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen(5)

            print(f"Serveur en attente de connexions sur le port {port}...")
            while True:
                client_socket, client_address = server_socket.accept()
                threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
        except PermissionError as pe:
            print(f"PermissionError : {pe}. Essayez d'exécuter avec des privilèges administratifs.")
            break
        except OSError as oe:
            print(f"OSError : {oe}. Le port {port} est indisponible. Essai avec le port {port + 1}.")
            port += 1
        except Exception as e:
            print(f"Erreur inattendue : {e}")
            break
        finally:
            server_socket.close()



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Serveur Python acceptant des fichiers Python à exécuter.")
    parser.add_argument("--port", type=int, default=4200, help="Port sur lequel écouter les connexions (par défaut : 4200).")
    args = parser.parse_args()

    start_server(port=args.port)
