def divEntier(x: int, y: int) -> int:
    if y == 0:
        raise ZeroDivisionError("La division par zéro n'est pas permise.")

    if x < y:
        return 0
    else:
        x = x - y
        return divEntier(x, y) + 1
def main():
    try:
        x = int(input("x : "))
        y = int(input("y : "))

        if y <= 0:
            print("La valeur de y doit être positive")
            return

        resultat = divEntier(x, y)
        print(f"La division de {x} par {y} est : {resultat}")

    except ValueError:
        print("entrez un nombre entier")
    except ZeroDivisionError as e:
        print(e)
if __name__ == "__main__":
    main()
