nom_fichier = "testex2.txt"

try:
    with open(nom_fichier, 'r') as fichier:
        for ligne in fichier:
            ligne = ligne.rstrip("\n\r")
            print(ligne)

except FileNotFoundError:
    print("Erreur : Le fichier spécifié est introuvable.")
except IOError:
    print("Erreur : Un problème d'accès au fichier est survenu.")
except FileExistsError:
    print("Erreur : Le fichier existe déjà alors qu'il ne devrait pas.")
except PermissionError:
    print("Erreur : Vous n'avez pas les permissions nécessaires pour accéder au fichier.")

finally:
    print("Fin du programme.")
