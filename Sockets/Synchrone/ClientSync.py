import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

while True:
    message = input("Votre message : ")
    client_socket.send(message.encode('utf-8'))
    if message in ["bye", "arret"]:
        break

    reponse = client_socket.recv(1024).decode('utf-8')
    print(f"Réponse du serveur : {reponse}")

client_socket.close()
