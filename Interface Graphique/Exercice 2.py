import tkinter as tk
from tkinter import ttk, messagebox

def convertir_temperature():
    try:
        temperature = float(entree.get())
        unite = combobox_unite.get()

        if unite == "Celsius" and temperature < -273.15:
            raise ValueError("La température ne peut pas être inférieure à -273.15 °C.")
        elif unite == "Kelvin" and temperature < 0:
            raise ValueError("La température ne peut pas être inférieure à 0 K.")

        if unite == "Celsius":
            resultat = temperature + 273.15
            label_resultat.config(text=f"{resultat:.2f} K")
        else:
            resultat = temperature - 273.15
            label_resultat.config(text=f"{resultat:.2f} °C")

    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
    except Exception:
        messagebox.showerror("Erreur", "Veuillez entrer une valeur numérique valide.")

fenetre = tk.Tk()
fenetre.title("Convertisseur Celsius <-> Kelvin")
fenetre.geometry("300x200")

label_instruction = tk.Label(fenetre, text="Entrez la température à convertir:")
label_instruction.pack(pady=5)

entree = tk.Entry(fenetre, width=20)
entree.pack(pady=5)

combobox_unite = ttk.Combobox(fenetre, values=["Celsius", "Kelvin"], state="readonly")
combobox_unite.current(0)
combobox_unite.pack(pady=5)

bouton_convertir = tk.Button(fenetre, text="Convertir", command=convertir_temperature)
bouton_convertir.pack(pady=10)

label_resultat = tk.Label(fenetre, text="", fg="blue")
label_resultat.pack(pady=5)

bouton_quitter = tk.Button(fenetre, text="Quitter", command=fenetre.destroy)
bouton_quitter.pack(pady=10, side="bottom")

fenetre.mainloop()
