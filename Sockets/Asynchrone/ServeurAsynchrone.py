import socket
import threading

clients = []

def gerer_client(client_socket, adresse):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "bye":
                print(f"{adresse} a quitté la discussion.")
                clients.remove(client_socket)
                client_socket.close()
                break
            elif message == "arret":
                print("Arrêt du serveur.")
                for client in clients:
                    client.close()
                serveur_socket.close()
                exit()
            else:
                print(f"Message reçu de {adresse}: {message}")
                for client in clients:
                    if client != client_socket:
                        client.send(f"De {adresse}: {message}".encode('utf-8'))
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur_socket.bind(('localhost', 12345))
serveur_socket.listen(5)
print("Serveur en attente de connexion...")

while True:
    client_socket, adresse = serveur_socket.accept()
    clients.append(client_socket)
    print(f"Nouvelle connexion de {adresse}")
    thread = threading.Thread(target=gerer_client, args=(client_socket, adresse))
    thread.start()
