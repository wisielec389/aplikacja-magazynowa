import matplotlib.pyplot as plt

# Inicjalizacja magazynu jako lista słowników
# Każdy produkt będzie miał: nazwa, ilosc, waga_jednostkowa (w kg)
# Magazyn będzie listą miejsc, gdzie każde miejsce to słownik z produktem i jego wagą
magazyn = [None] * 10  # 10 miejsc, początkowo puste
MAX_MIEJSC = 10
MAX_OBCIAZENIE_NA_MIEJSCE_KG = 1000  # 1 tona = 1000 kg

def wyswietl_stan():
    print("\n--- AKTUALNY STAN MAGAZYNU ---")
    zajete_miejsca = 0
    for i, miejsce in enumerate(magazyn):
        if miejsce:
            produkt = miejsce['produkt']
            waga_totalna_miejsca = produkt['ilosc'] * produkt['waga_jednostkowa']
            print(f"{i+1}. Nazwa: {produkt['nazwa']}, Ilość: {produkt['ilosc']} szt., "
                  f"Waga jednostkowa: {produkt['waga_jednostkowa']} kg, "
                  f"Całkowita waga na miejscu: {waga_totalna_miejsca:.2f} kg "
                  f"({(waga_totalna_miejsca/MAX_OBCIAZENIE_NA_MIEJSCE_KG)*100:.2f}% obciążenia)")
            zajete_miejsca += 1
        else:
            print(f"{i+1}. WOLNE")
    print(f"Zajętych miejsc: {zajete_miejsca}/{MAX_MIEJSC}")
    print(f"Wolnych miejsc (slotów): {MAX_MIEJSC - zajete_miejsca}")
    print("------------------------------")

def znajdz_wolne_miejsce():
    for i, miejsce in enumerate(magazyn):
        if miejsce is None:
            return i
    return -1 # Brak wolnych miejsc

def dodaj_produkt():
    wolne_miejsce_idx = znajdz_wolne_miejsce()
    if wolne_miejsce_idx == -1:
        print("BŁĄD: Magazyn jest pełny! Brak wolnych slotów.")
        return

    nazwa = input("Podaj nazwę produktu: ")
    try:
        ilosc = int(input("Podaj ilość (ile sztuk składować): "))
        waga_jednostkowa = float(input("Podaj wagę jednostkową produktu w kg: "))
        
        if waga_jednostkowa <= 0:
            print("BŁĄD: Waga jednostkowa musi być dodatnia.")
            return

        total_waga_produktu = ilosc * waga_jednostkowa
        if total_waga_produktu > MAX_OBCIAZENIE_NA_MIEJSCE_KG:
            print(f"BŁĄD: Całkowita waga ({total_waga_produktu:.2f} kg) przekracza "
                  f"maksymalne obciążenie dla jednego miejsca ({MAX_OBCIAZENIE_NA_MIEJSCE_KG} kg).")
            return

        produkt_info = {
            "nazwa": nazwa,
            "ilosc": ilosc,
            "waga_jednostkowa": waga_jednostkowa
        }
        
        magazyn[wolne_miejsce_idx] = {'produkt': produkt_info, 'waga_zajmowana': total_waga_produktu}
        print(f"Dodano produkt '{nazwa}' na miejscu {wolne_miejsce_idx + 1}.")

    except ValueError:
        print("BŁĄD: Ilość i waga muszą być liczbami!")

def usun_produkt():
    wyswietl_stan()
    
    zajete_miejsca_count = sum(1 for m in magazyn if m is not None)
    if zajete_miejsca_count == 0:
        print("Magazyn jest pusty, nie ma czego usuwać.")
        return

    try:
        numer_miejsca = int(input("Podaj numer miejsca (1-10) produktu do usunięcia: "))
        index = numer_miejsca - 1

        if 0 <= index < MAX_MIEJSC and magazyn[index] is not None:
            usuniety_produkt = magazyn[index]['produkt']
            magazyn[index] = None  # Ustawienie miejsca jako wolnego
            print(f"Usunięto '{usuniety_produkt['nazwa']}' z miejsca {numer_miejsca}.")
        elif 0 <= index < MAX_MIEJSC and magazyn[index] is None:
            print(f"BŁĄD: Miejsce {numer_miejsca} jest już wolne.")
        else:
            print("BŁĄD: Nie ma miejsca o takim numerze.")
    except ValueError:
        print("BŁĄD: Podaj poprawną liczbę dla numeru miejsca.")

def pokaz_wykres_obciazenia():
    miejsca = [f"M.{i+1}" for i in range(MAX_MIEJSC)]
    wagi = []
    kolory = []

    for miejsce in magazyn:
        if miejsce:
            waga_aktualna = miejsce['waga_zajmowana']
            wagi.append(waga_aktualna)
            procent_obciazenia = (waga_aktualna / MAX_OBCIAZENIE_NA_MIEJSCE_KG) * 100
            
            if procent_obciazenia > 90:
                kolory.append('red')
            elif procent_obciazenia > 50:
                kolory.append('orange')
            else:
                kolory.append('green')
        else:
            wagi.append(0)
            kolory.append('lightgrey') # Wolne miejsce

    plt.figure(figsize=(12, 6)) # Zwiększamy rozmiar wykresu
    bars = plt.bar(miejsca, wagi, color=kolory)
    plt.ylabel("Waga (kg)")
    plt.title("Zapełnienie miejsc w magazynie (Waga)")
    plt.ylim(0, MAX_OBCIAZENIE_NA_MIEJSCE_KG * 1.1) # Lekki bufor powyżej max obciążenia
    plt.axhline(y=MAX_OBCIAZENIE_NA_MIEJSCE_KG, color='r', linestyle='--', label='Max obciążenie (1000 kg)')
    plt.legend()

    # Dodawanie etykiet z wartościami na słupkach
    for bar in bars:
        yval = bar.get_height()
        if yval > 0:
            plt.text(bar.get_x() + bar.get_width()/2, yval + 20, round(yval, 2), ha='center', va='bottom')
            procent = (yval / MAX_OBCIAZENIE_NA_MIEJSCE_KG) * 100
            plt.text(bar.get_x() + bar.get_width()/2, yval + 60, f"{procent:.1f}%", ha='center', va='bottom', fontsize=8)


    plt.show()


# Główna pętla programu
while True:
    print("\n--- MENU MAGAZYNU ---")
    print("1. Wyświetl stan magazynu")
    print("2. Dodaj produkt")
    print("3. Usuń produkt")
    print("4. Pokaż wykres obciążenia")
    print("5. Wyjdź")
    print("---------------------")
    wybor = input("Wybierz opcję: ")

    if wybor == '1':
        wyswietl_stan()
    elif wybor == '2':
        dodaj_produkt()
    elif wybor == '3':
        usun_produkt()
    elif wybor == '4':
        pokaz_wykres_obciazenia()
    elif wybor == '5':
        print("Zamykanie programu...")
        break
    else:
        print("Niepoprawny wybór, spróbuj ponownie.")
  
