import socket

serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur_socket.bind(('localhost', 12345))
serveur_socket.listen(1)

print("Le serveur est en attente de connexion...")

client_socket, adresse = serveur_socket.accept()
print(f"La connexion a été établie avec {adresse}")

message = client_socket.recv(1024).decode('utf-8')
print(f"Message reçu : {message}")

client_socket.send("Le message a bien été reçu".encode('utf-8'))

client_socket.close()
serveur_socket.close()
