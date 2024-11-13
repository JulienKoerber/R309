import socket

serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur_socket.bind(('localhost', 12345))
serveur_socket.listen(1)
print("Le Serveur attend la connexion du client...")

while True:
    client_socket, adresse = serveur_socket.accept()
    print(f"La connexion a été avec {adresse}")

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
