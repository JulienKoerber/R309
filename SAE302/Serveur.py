import socket
import threading


# Fonction pour exécuter le code Python envoyé
def handle_client(client_socket):
    try:
        # Recevoir le nom du fichier
        filename = client_socket.recv(1024).decode('utf-8')
        print(f"Fichier reçu: {filename}")

        # Vérification si le fichier est un .py
        if not filename.endswith('.py'):
            client_socket.sendall("Erreur: Seuls les fichiers .py sont acceptés.")
            client_socket.close()
            return

        # Recevoir le contenu du fichier
        file_content = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            file_content += data

        # Sauvegarder le fichier reçu sur le serveur
        with open(filename, 'wb') as f:
            f.write(file_content)
        print(f"Fichier {filename} sauvegardé.")

        # Exécuter le code Python
        try:
            exec_result = exec(file_content)
            client_socket.sendall("Execution réussie.\nRésultat: " + str(exec_result).encode('utf-8'))
        except Exception as e:
            client_socket.sendall(f"Erreur lors de l'exécution du fichier: {e}".encode('utf-8'))

    except Exception as e:
        print(f"Erreur serveur: {e}")
    finally:
        client_socket.close()


# Fonction pour démarrer le serveur
def start_server():
    host = '127.0.0.1'
    port = 4300

    # Création du socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permet la réutilisation de l'adresse et du port
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Lier le serveur à l'adresse et au port
        server_socket.bind((host, port))
        print(f"Serveur démarré sur {host}:{port}")

        # Écouter les connexions entrantes
        server_socket.listen(5)

        # Attendre les connexions des clients
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connexion établie avec {client_address}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

    except Exception as e:
        print(f"Erreur serveur: {e}")
    finally:
        server_socket.close()


# Démarrer le serveur
if __name__ == "__main__":
    start_server()
