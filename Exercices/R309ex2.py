# 1. Définir le nom du fichier dans une variable
nom_fichier = "testex2.txt"

# 2. Essayer d'ouvrir et de lire le fichier
try:
    # Ouverture du fichier en lecture avec le mot-clé 'with'
    with open(nom_fichier, 'r') as fichier:
        # Lecture et affichage des lignes
        for ligne in fichier:
            ligne = ligne.rstrip("\n\r")  # Retire les retours à la ligne
            print(ligne)

# 3. Gestion des exceptions
except FileNotFoundError:
    print("Erreur : Le fichier spécifié est introuvable.")
except IOError:
    print("Erreur : Un problème d'accès au fichier est survenu.")
except FileExistsError:
    print("Erreur : Le fichier existe déjà alors qu'il ne devrait pas.")
except PermissionError:
    print("Erreur : Vous n'avez pas les permissions nécessaires pour accéder au fichier.")

# 4. Bloc finally pour indiquer la fin du programme
finally:
    print("Fin du programme.")
