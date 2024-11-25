#l'url de mon github est --> www.github.com/JulienKoerber/R309
#J'ai combiner mes codes de l'exercice 1 de la partie interface graphique avec la partie Serveur Synchrone
import tkinter as tk
import socket
class Serveur:
    def __init__(self, master):
        self.master = master
        self.master.title("Serveur")
        self.master.geometry("300x200")

        tk.Label(master, text="Serveur :").pack(pady=2)
        self.entree_hote = tk.Entry(master, width=30)
        self.entree_hote.insert(0, "localhost")
        self.entree_hote.pack(pady=2)

        tk.Label(master, text="Port :").pack(pady=2)
        self.entree_port = tk.Entry(master, width=30)
        self.entree_port.insert(0, "4200")
        self.entree_port.pack(pady=2)

        tk.Label(master, text="Nombre maximum de clients :").pack(pady=2)
        self.entree_clients = tk.Entry(master, width=30)
        self.entree_clients.insert(0, "5")
        self.entree_clients.pack(pady=2)

        self.bouton_demarrer = tk.Button(master, text="Démarrer le serveur", command=self.toggle_serveur)
        self.bouton_demarrer.pack(pady=10)

        self.serveur_socket = None
        self.client_socket = None
        self.serveur_actif = False

    def toggle_serveur(self):
        if not self.serveur_actif:
            self.start_serveur()
        else:
            self.stop_serveur()
    def start_serveur(self):
        self.serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur_socket.bind(('localhost', 4200))
        self.serveur_socket.listen(1)
        self.serveur_actif = True
        self.bouton_demarrer.config(text="stopper le serveur")
        self.bouton_demarrer.config(state="normal")
        self.logs("Serveur démarré sur le port 4200")


    def stop_serveur(self):
        if self.client_socket:
            self.client_socket.close()
        if self.serveur_socket:
            self.serveur_socket.close()
        self.serveur_actif = False
        self.bouton_demarrer.config(text="Démarrer le serveur")
        self.bouton_envoyer.config(state="disabled")
        self.logs("Serveur arrêté")

    def accepter_client(self):
        self.logs("en attente")
        self.client_socket, _ = self.serveur_socket.accept()
        self.logs("Client connecté")

    def recevoir_messages(self):
        while True:
            try:
                message = self.client_socket.recv(4200).decode('utf-8')
                self.log(f"Message reçu : {message}")
            except:
                break

    def envoyer_message(self):
        if self.client_socket:
            message = self.entree.get()
            if message:
                self.client_socket.send(message.encode('utf-8'))
                self.log(f"Message envoyé : {message}")
                self.entree.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = Serveur(root)
    root.mainloop()