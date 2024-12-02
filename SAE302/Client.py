import socket
import tkinter as tk
from tkinter import messagebox, filedialog  # Importation de filedialog pour choisir un fichier
import os

# Fonction pour envoyer un fichier au serveur et demander son exécution
def send_and_execute_file():
    server_ip = ip_entry.get()
    server_port = int(port_entry.get())

    # Vérifier si un fichier est sélectionné
    file_path = file_path_entry.get()
    if not file_path or not os.path.exists(file_path):
        messagebox.showerror("Erreur", "Veuillez sélectionner un fichier valide.")
        return

    # Vérification de l'extension du fichier
    if not file_path.endswith('.py'):
        messagebox.showerror("Erreur", "Seuls les fichiers .py sont acceptés.")
        return

    try:
        # Création du socket et connexion au serveur
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        # Envoyer le nom du fichier au serveur
        filename = os.path.basename(file_path)
        client_socket.sendall(filename.encode('utf-8'))

        # Envoyer le contenu du fichier
        with open(file_path, 'rb') as file:
            while chunk := file.read(4096):
                client_socket.sendall(chunk)

        # Demander au serveur d'exécuter le fichier
        client_socket.sendall(b"EXECUTE")

        # Attendre la réponse du serveur (résultat de l'exécution)
        result = client_socket.recv(4096).decode('utf-8')

        # Afficher le résultat dans l'interface graphique
        output_text.delete(1.0, tk.END)  # Effacer l'ancienne sortie
        output_text.insert(tk.END, result)  # Afficher le nouveau résultat

        client_socket.close()
    except Exception as e:
        messagebox.showerror("Erreur de connexion", f"Impossible de se connecter au serveur : {e}")

# Fonction pour choisir un fichier
def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

# Fonction pour se connecter au serveur
def connect_to_server():
    server_ip = ip_entry.get()
    server_port = port_entry.get()
    try:
        if not server_ip or not server_port:
            messagebox.showerror("Erreur", "Veuillez entrer l'IP et le port du serveur.")
            return
        server_port = int(server_port)

        # Vérification de la connexion
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        messagebox.showinfo("Succès", "Connexion réussie au serveur !")
        client_socket.close()
    except Exception as e:
        messagebox.showerror("Erreur de connexion", f"Erreur de connexion : {e}")

# Fonction pour éteindre le client
def shutdown_client():
    if messagebox.askyesno("Quitter", "Voulez-vous vraiment fermer le client ?"):
        window.quit()

# Création de la fenêtre principale
window = tk.Tk()
window.title("Client Python")

# Champ pour l'IP du serveur
tk.Label(window, text="IP du Serveur:").grid(row=0, column=0, padx=10, pady=5)
ip_entry = tk.Entry(window, width=25)
ip_entry.grid(row=0, column=1, padx=10, pady=5)

# Champ pour le port du serveur
tk.Label(window, text="Port du Serveur:").grid(row=1, column=0, padx=10, pady=5)
port_entry = tk.Entry(window, width=25)
port_entry.grid(row=1, column=1, padx=10, pady=5)

# Bouton pour se connecter au serveur
connect_button = tk.Button(window, text="Se connecter au serveur", command=connect_to_server)
connect_button.grid(row=2, columnspan=2, pady=10)

# Champ pour sélectionner le fichier à envoyer
tk.Label(window, text="Fichier à envoyer:").grid(row=3, column=0, padx=10, pady=5)
file_path_entry = tk.Entry(window, width=25)
file_path_entry.grid(row=3, column=1, padx=10, pady=5)

# Bouton pour choisir un fichier
choose_button = tk.Button(window, text="Choisir un fichier", command=choose_file)
choose_button.grid(row=4, columnspan=2, pady=10)

# Bouton pour envoyer et exécuter le fichier
send_button = tk.Button(window, text="Envoyer et exécuter le fichier", command=send_and_execute_file)
send_button.grid(row=5, columnspan=2, pady=10)

# Zone de texte pour afficher le résultat de l'exécution
output_text = tk.Text(window, height=10, width=50)
output_text.grid(row=6, columnspan=2, padx=10, pady=10)

# Bouton pour éteindre le client
shutdown_button = tk.Button(window, text="Éteindre le client", command=shutdown_client)
shutdown_button.grid(row=7, columnspan=2, pady=10)

# Lancer l'interface graphique
window.mainloop()
