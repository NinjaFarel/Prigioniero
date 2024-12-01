import random  # Non uso numpy per non dover installare librerie esterne


def main():
    print("Due prigionieri devono collaborare per trovare una chiave nascosta sotto una casella di una scacchiera 8x8. "
          "Sopra ogni casella della scacchiera c’è una moneta posta a testa o a croce. "
          "Uno dei prigionieri può invertire una sola moneta prima di essere portato via per "
          "comunicare all'altro la posizione.\nCome? Con questo script!\n")

    dimensione, dimensione_reale = chiedi_dimensione()

    scelta = input("\nInserisci \"M\" per riempire la scacchiera manualmente, lascia vuoto per riempirla casualmente: ")
    if scelta.lower() == "m":
        scacchiera = riempi_manualmente(dimensione, dimensione_reale)
    else:
        scacchiera = riempi_casualmente(dimensione, dimensione_reale)

    print("\nOk, la scacchiera è stata così riempita:")
    mostra_scacchiera(dimensione, scacchiera)

    print("\nLa strategia è quella di assegnare ad ogni cella della scacchiera un valore binario e calcolare la parità "
          "dei bit di tutte le monete testa (in questo caso rappresentate come 1). Invertendo la moneta giusta "
          "sarà possibile codificare nella serie di bit di parità la posizione in binario della chiave!")

    print("\nInserisci le coordinate in formato \"i, j\" della chiave (parte da 0, 0 in alto a sinistra): ")
    chiave = chiedi_coordinate(dimensione)

    parita = calcola_parita(scacchiera)
    pos_chiave = coord_to_pos(chiave[0], chiave[1], dimensione_reale)
    print(f"\nLa parità attuale è: {bin(parita)}")
    print(f"La chiave è nella cella: {bin(pos_chiave)}")

    if parita == pos_chiave:
        print("\nIncredibile ma vero, non dobbiamo cambiare niente!")
    else:
        pos_moneta = parita ^ pos_chiave
        moneta = pos_to_coord(pos_moneta, dimensione_reale)
        print("\nPer calcolare la moneta da cambiare, basta uno XOR tra la parità e la chiave, "
              f"che nel nostro caso fa: {bin(pos_moneta)}")
        scacchiera[moneta[0]][moneta[1]] += 4

    scacchiera[chiave[0]][chiave[1]] += 2
    print("\nLa nostra scacchiera finale sarà quindi (C è la chiave, X la moneta da cambiare, "
          "in maiuscolo se precedentemente 1, viceversa minuscolo):")
    mostra_scacchiera(dimensione, scacchiera)

    scelta = input("\n\nPremi Q per uscire, lascia vuoto per riprovare: ")
    if scelta.lower() == "q":
        return

    main()


def chiedi_dimensione() -> tuple[int, int]:
    while True:
        try:
            dimensione = int(input("Inserisci la dimensione della scacchiera: "))
            if dimensione == 0:
                raise ValueError
            break
        except ValueError:
            print("La dimensione deve essere un numero valido! Riprova.")

    # Prende la potenza di 2 più vicina (per eccesso)
    dimensione_reale = 1 << (dimensione - 1).bit_length() if dimensione > 0 else 1

    return dimensione, dimensione_reale


def riempi_manualmente(dimensione: int, dimensione_reale: int) -> list[list[int]]:
    print("\nInserisci le coordinate in formato \"i, j\" di tutte le monete testa, "
          "separandole con un \"a capo\" (puoi annullare una selezione ripetendola):")
    scelta = ""
    scacchiera = [[0 for _ in range(dimensione_reale)] for _ in range(dimensione_reale)]

    while scelta.lower() != "q":
        coordinate = chiedi_coordinate(dimensione)
        scacchiera[coordinate[0]][coordinate[1]] = 1 - scacchiera[coordinate[0]][coordinate[1]]

        scelta = input("Premi Q per uscire, lascia vuoto per continuare a girare monete: ")

    return scacchiera


def riempi_casualmente(dimensione: int, dimensione_reale: int) -> list[list[int]]:
    scacchiera = []
    for i in range(dimensione_reale):
        scacchiera.append([])
        for j in range(dimensione_reale):
            if i > dimensione - 1 or j > dimensione - 1:
                scacchiera[i].append(0)  # Considera 0 tutte le celle oltre la dimensione stabilita
            else:
                scacchiera[i].append(random.getrandbits(1))

    return scacchiera


def mostra_scacchiera(n: int, scacchiera: list[list[int]]):
    scacchiera_formattata = ["┌" + "┬".join("─" * 5 for _ in range(n)) + "┐"]
    for i in range(2 * n - 1):
        if i % 2:
            scacchiera_formattata.append("├" + "┼".join("─" * 5 for _ in range(n)) + "┤")
        else:
            scacchiera_formattata.append(
                "│" + "│".join(f"  {codifica(scacchiera[int(i / 2)][j])}  " for j in range(n)) + "│")
    scacchiera_formattata.append("└" + "┴".join("─" * 5 for _ in range(n)) + "┘")

    print("\n".join(scacchiera_formattata))


def codifica(x: int) -> str:
    # Usato per sostituire C o X a chiave e moneta rispettivamente
    match x:
        case 2:
            return "c"
        case 3:
            return "C"
        case 4:
            return "x"
        case 5:
            return "X"
        case _:
            return str(x)


def calcola_parita(scacchiera: list[list[int]]) -> int:
    parita = 0
    for i, riga in enumerate(scacchiera):
        for cella in riga:
            if cella:
                parita ^= coord_to_pos(cella, i, len(scacchiera))
                # Effettua uno XOR per tutte le monete testa in base alla loro posizione

    return parita


def coord_to_pos(x: int, y: int, dim: int) -> int:
    return x + y * dim


def pos_to_coord(pos: int, dim: int) -> tuple[int, int]:
    return pos - dim * int(pos / dim), int(pos / dim)


def chiedi_coordinate(dimensione: int) -> tuple[int, ...]:
    while True:
        coordinate = input()
        try:
            parti = coordinate.split(",")
            if len(parti) != 2:
                raise ValueError
            for coordinata in parti:
                if coordinata > str(dimensione - 1):
                    raise ValueError
            return tuple(map(int, map(str.strip, parti)))
        except ValueError:
            print("Coordinate non corrette! Riprova.")


if __name__ == "__main__":
    main()
