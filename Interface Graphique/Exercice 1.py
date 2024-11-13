import tkinter as tk
from tkinter import messagebox
def afficher_message():
    texte = entree.get()
    if texte:
        label_message.config(text=f"Message: Bonjour {texte} !")
    else:
        messagebox.showwarning("Attention", "Le champ de texte est vide!")

fenetre = tk.Tk()
fenetre.title("Exemple d'Interface Graphique")
fenetre.geometry("300x200")

label_entree = tk.Label(fenetre, text="Entrez votre prénom :")
label_entree.pack(pady=5)
entree = tk.Entry(fenetre, width=30)
entree.pack(pady=5)

bouton_afficher = tk.Button(fenetre, text="Afficher", command=afficher_message)
bouton_afficher.pack(pady=10)

label_message = tk.Label(fenetre, text="", fg="green")
label_message.pack(pady=5)

bouton_quitter = tk.Button(fenetre, text="Quitter", command=fenetre.destroy)
bouton_quitter.pack(pady=10, side="bottom")

fenetre.mainloop()