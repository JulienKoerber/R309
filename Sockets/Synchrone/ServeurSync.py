import socket

serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur_socket.bind(('localhost', 12345))
serveur_socket.listen(1)
print("Serveur en attente de connexion...")

while True:
    client_socket, adresse = serveur_socket.accept()
    print(f"Connexion établie avec {adresse}")

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if message == "bye":
            print("Le client a quitté la conversation.")
            break
        elif message == "arret":
            print("Arrêt du serveur et du client.")
            serveur_socket.close()
            exit()

        print(f"Message reçu : {message}")
        reponse = input("Réponse : ")
        client_socket.send(reponse.encode('utf-8'))

    client_socket.close()
