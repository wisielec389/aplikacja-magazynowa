magazyn = []
MAX_MIEJSC = 10

def wyswietl_stan():
    print("\n--- AKTUALNY STAN MAGAZYNU ---")
    if not magazyn:
        print("Magazyn jest pusty.")
    else:
        for i, produkt in enumerate(magazyn):
            print(f"{i+1}. Nazwa: {produkt['nazwa']}, Ilość: {produkt['ilosc']}")
    print(f"Wolne miejsca: {MAX_MIEJSC - len(magazyn)}")
    print("------------------------------")

def dodaj_produkt():
    if len(magazyn) >= MAX_MIEJSC:
        print("BŁĄD: Magazyn jest pełny! Usuń coś, aby dodać nowy produkt.")
        return

    nazwa = input("Podaj nazwę produktu: ")
    try:
        ilosc = int(input("Podaj ilość (ile sztuk składować): "))
        magazyn.append({"nazwa": nazwa, "ilosc": ilosc})
        print(f"Dodano produkt: {nazwa}")
    except ValueError:
        print("BŁĄD: Ilość musi być liczbą!")

def usun_produkt():
    wyswietl_stan()
    if not magazyn:
        return
    
    try:
        index = int(input("Podaj numer produktu do usunięcia: ")) - 1
        if 0 <= index < len(magazyn):
            usuniety = magazyn.pop(index)
            print(f"Usunięto z magazynu: {usuniety['nazwa']}")
        else:
            print("BŁĄD: Nie ma produktu o takim numerze.")
    except ValueError:
        print("BŁĄD: Podaj poprawną liczbę.")

# Główna pętla programu
while True:
    print("\n1. Wyświetl stan | 2. Dodaj produkt | 3. Usuń produkt | 4. Wyjdź")
    wybor = input("Wybierz opcję: ")

    if wybor == '1':
        wyswietl_stan()
    elif wybor == '2':
        dodaj_produkt()
    elif wybor == '3':
        usun_produkt()
    elif wybor == '4':
        print("Zamykanie programu...")
        break
    else:
        print("Niepoprawny wybór, spróbuj ponownie.")
