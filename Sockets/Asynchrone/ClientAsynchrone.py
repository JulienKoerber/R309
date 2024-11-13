import socket
import threading

def recevoir_messages(socket):
    while True:
        try:
            message = socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Connexion fermée.")
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

thread = threading.Thread(target=recevoir_messages, args=(client_socket,))
thread.start()

while True:
    message = input("Votre message : ")
    client_socket.send(message.encode('utf-8'))
    if message in ["bye", "arret"]:
        client_socket.close()
        break