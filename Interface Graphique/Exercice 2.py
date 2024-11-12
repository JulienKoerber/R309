import tkinter as tk
from tkinter import ttk, messagebox


# Fonction de conversion Celsius <-> Kelvin
def convertir_temperature():
    try:
        # Récupérer la température entrée par l'utilisateur et l'unité sélectionnée
        temperature = float(entree.get())
        unite = combobox_unite.get()

        # Vérifier les valeurs sous le zéro absolu
        if unite == "Celsius" and temperature < -273.15:
            raise ValueError("La température ne peut pas être inférieure à -273.15 °C.")
        elif unite == "Kelvin" and temperature < 0:
            raise ValueError("La température ne peut pas être inférieure à 0 K.")

        # Conversion
        if unite == "Celsius":
            resultat = temperature + 273.15  # Convertir Celsius en Kelvin
            label_resultat.config(text=f"{resultat:.2f} K")
        else:
            resultat = temperature - 273.15  # Convertir Kelvin en Celsius
            label_resultat.config(text=f"{resultat:.2f} °C")

    except ValueError as e:
        # Gérer les erreurs de conversion ou de valeur
        messagebox.showerror("Erreur", str(e))
    except Exception:
        # Autre erreur (ex : saisie invalide)
        messagebox.showerror("Erreur", "Veuillez entrer une valeur numérique valide.")


# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Convertisseur Celsius <-> Kelvin")
fenetre.geometry("300x200")

# Label d'instruction
label_instruction = tk.Label(fenetre, text="Entrez la température :")
label_instruction.pack(pady=5)

# Champ de saisie pour la température
entree = tk.Entry(fenetre, width=20)
entree.pack(pady=5)

# Combobox pour choisir l'unité de température
combobox_unite = ttk.Combobox(fenetre, values=["Celsius", "Kelvin"], state="readonly")
combobox_unite.current(0)  # Valeur par défaut "Celsius"
combobox_unite.pack(pady=5)

# Bouton pour effectuer la conversion
bouton_convertir = tk.Button(fenetre, text="Convertir", command=convertir_temperature)
bouton_convertir.pack(pady=10)

# Étiquette pour afficher le résultat
label_resultat = tk.Label(fenetre, text="", fg="blue")
label_resultat.pack(pady=5)

bouton_quitter = tk.Button(fenetre, text="Quitter", command=fenetre.destroy)
bouton_quitter.pack(pady=10, side="bottom")

# Lancement de la boucle principale de la fenêtre
fenetre.mainloop()
