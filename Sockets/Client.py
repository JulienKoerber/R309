import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

client_socket.send("Bonjour, serveur!".encode('utf-8'))

reponse = client_socket.recv(1024).decode('utf-8')
print(f"Réponse du serveur : {reponse}")

client_socket.close()
