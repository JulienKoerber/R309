import tkinter as tk
from tkinter import messagebox

# Fonction exécutée lors du clic sur le bouton
def afficher_message():
    texte = entree.get()  # Récupère le texte de l'entrée
    if texte:
        label_message.config(text=f"Message: {texte}")
    else:
        messagebox.showwarning("Attention", "Le champ de texte est vide!")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Exemple d'Interface Graphique")
fenetre.geometry("300x200")

# Champ de saisie
label_entree = tk.Label(fenetre, text="Entrez un message :")
label_entree.pack(pady=5)
entree = tk.Entry(fenetre, width=30)
entree.pack(pady=5)

# Bouton pour afficher le message
bouton_afficher = tk.Button(fenetre, text="Afficher", command=afficher_message)
bouton_afficher.pack(pady=10)

# Étiquette pour afficher le message
label_message = tk.Label(fenetre, text="", fg="blue")
label_message.pack(pady=5)

# Lancement de la boucle principale de la fenêtre
fenetre.mainloop()
