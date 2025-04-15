import random
import math
import time

# Funkcja do drukowania z opóźnieniem
def print_with_delay(*args, **kwargs):
    print(*args, **kwargs)
    time.sleep(0.1) #opóźnienie

# Inicjalizacja graczy
gracz1 = {'kasa': 0, 'pole': 0, 'exit_jail': False, 'injail': False, 'jail_turns': 0}
gracz2 = {'kasa': 0, 'pole': 0, 'exit_jail': False, 'injail': False, 'jail_turns': 0}
gracz3 = {'kasa': 0, 'pole': 0, 'exit_jail': False, 'injail': False, 'jail_turns': 0}
gracz4 = {'kasa': 0, 'pole': 0, 'exit_jail': False, 'injail': False, 'jail_turns': 0}

gracz1_nieruchomosci = []
gracz2_nieruchomosci = []
gracz3_nieruchomosci = []
gracz4_nieruchomosci = []

nieruchomosci_graczy = [
    gracz1_nieruchomosci,
    gracz2_nieruchomosci,
    gracz3_nieruchomosci,
    gracz4_nieruchomosci
]

gracze = []

pola = [
    'Start', 'Br1', 'Br2', 'Szansa', 'Bł1', 'Bł2', 'Odwiedziny', 'R1', 'R2', 'Szansa',
    'O1', 'O2', 'Parking', 'C1', 'C2', 'Szansa', 'Ż1', 'Ż2', 'Więzienie', 'Z1', 'Z2', 'Szansa', 'N1', 'N2'
]

nieruchomosci = [
    'Br1', 'Br2', 'Bł1', 'Bł2', 'R1', 'R2', 'O1', 'O2',
    'C1', 'C2', 'Ż1', 'Ż2', 'Z1', 'Z2', 'N1', 'N2'
]

# Grupy kolorów nieruchomości
grupy_kolorow = {
    'brązowe': ['Br1', 'Br2'],
    'jasnoniebieskie': ['Bł1', 'Bł2'],
    'różowe': ['R1', 'R2'],
    'pomarańczowe': ['O1', 'O2'],
    'czerwone': ['C1', 'C2'],
    'żółte': ['Ż1', 'Ż2'],
    'zielone': ['Z1', 'Z2'],
    'ciemnoniebieskie': ['N1', 'N2']
}

pozostale_nieruchomosci = nieruchomosci.copy()

increment = 0


# Wybór liczby graczy
while True:
    wybor = int(input("Ile graczy? (2–4): "))
    if wybor in [2, 3, 4]:
        if wybor >= 2:
            gracz1['kasa'] = 20
            gracze.append(gracz1)
            gracz2['kasa'] = 20
            gracze.append(gracz2)
        if wybor >= 3:
            gracz3['kasa'] = 20
            gracze.append(gracz3)
        if wybor == 4:
            gracz4['kasa'] = 20
            gracze.append(gracz4)
        break



# Funkcje pomocnicze

def ma_caly_kolor(gracz_id, nieruchomosc):
    for kolor, nier_list in grupy_kolorow.items():
        if nieruchomosc in nier_list:
            # Sprawdz czy gracz ma wszystkie nieruchomości z tej grupy
            return all(nier in nieruchomosci_graczy[gracz_id] for nier in nier_list)
    return False

def znajdz_nastepne_pole(gracz, kolory):
    """Znajduje następne pole danego koloru"""
    aktualne_pole = gracz['pole']
    for i in range(1, 24):
        nastepne_pole = (aktualne_pole + i) % 24
        nazwa_pola = pola[nastepne_pole]
        if nazwa_pola in nieruchomosci:
            kolor = None
            if nazwa_pola in ['Br1', 'Br2']: kolor = 'brązowe'
            elif nazwa_pola in ['Bł1', 'Bł2']: kolor = 'jasnoniebieskie'
            elif nazwa_pola in ['R1', 'R2']: kolor = 'różowe'
            elif nazwa_pola in ['O1', 'O2']: kolor = 'pomarańczowe'
            elif nazwa_pola in ['C1', 'C2']: kolor = 'czerwone'
            elif nazwa_pola in ['Ż1', 'Ż2']: kolor = 'żółte'
            elif nazwa_pola in ['Z1', 'Z2']: kolor = 'zielone'
            elif nazwa_pola in ['N1', 'N2']: kolor = 'ciemnoniebieskie'
            
            if kolor in kolory:
                return nastepne_pole
    return None

def przenies_gracza(gracz, pole_cel):
    """Przenosi gracza na określone pole"""
    gracz['pole'] = pole_cel
    print_with_delay(f"Przeniesiono na {pola[pole_cel]}")
    return pole_cel

def obsluz_nieruchomosc(gracz, numer_gracza):
    """Obsługuje logikę nieruchomości po przeniesieniu"""
    obecne_pole = pola[gracz['pole']]
    if obecne_pole in nieruchomosci:
        indeks = nieruchomosci.index(obecne_pole)
        koszt = math.ceil((indeks+1) / 4)
        if obecne_pole[0] == 'N': koszt += 1
        
        for i, nier in enumerate(nieruchomosci_graczy):
            if obecne_pole in nier:
                if i != numer_gracza:
                    # Sprawdzamy czy właściciel ma wszystkie nieruchomości tego koloru
                    for kolor, nier_list in grupy_kolorow.items():
                        if obecne_pole in nier_list:
                            if all(n in nieruchomosci_graczy[i] for n in nier_list):
                                koszt *= 2
                                print_with_delay(f"💸 PODWÓJNY CZYNSZ! Gracz {i+1} ma cały kolor {kolor}")
                            break
                    
                    gracz['kasa'] -= koszt
                    gracze[i]['kasa'] += koszt
                    print_with_delay(f"🏠 Nieruchomość należy do gracza {i+1}. Czynsz: {koszt} zł")
                else:
                    print_with_delay("✅ To twoja nieruchomość.")
                return
                
        if gracz['kasa'] >= koszt:
            gracz['kasa'] -= koszt
            nieruchomosci_graczy[numer_gracza].append(obecne_pole)
            pozostale_nieruchomosci.remove(obecne_pole)
            print_with_delay(f"💼 Kupujesz {obecne_pole} za {koszt} zł")
            
            # Sprawdź czy gracz zdobył cały kolor
            for kolor, nier_list in grupy_kolorow.items():
                if obecne_pole in nier_list:
                    if all(n in nieruchomosci_graczy[numer_gracza] for n in nier_list):
                        print_with_delay(f"🎉 Gratulacje! Masz cały kolor {kolor}!")
                    break
        else:
            print_with_delay(f"❌ Nie stać cię na {obecne_pole} ({koszt} zł)")
            
            
def szansa(numer_gracza):
    """Funkcja obsługująca kartę szansy"""
    gracz = gracze[numer_gracza]
    opcje = [
        ("Przejdź na następne jasnoniebieskie pole (Bł1, Bł2)", ['jasnoniebieskie']),
        ("Przejdź na następne czerwone pole (C1, C2)", ['czerwone']),
        ("Przejdź na następne różowe lub ciemnoniebieskie pole (R1, R2, N1, N2)", ['różowe', 'ciemnoniebieskie']),
        ("Przejdź na następne pomarańczowe lub zielone pole (O1, O2, Z1, Z2)", ['pomarańczowe', 'zielone']),
        ("Przejdź do Skate Parku (O1)", None, 10),
        ("Przejdź na następne brązowe lub żółte pole (Br1, Br2, Ż1, Ż2)", ['brązowe', 'żółte']),
        ("Przejdź na następne pomarańczowe pole (O1,O2)", ['pomarańczowe']),
        ("Przejdź na następne jasnoniebieskie lub czerwone pole (Bł1, Bł2, C1, C2)", ['jasnoniebieskie', 'czerwone']),
        ("Wychodzisz z więzienia za darmo", "exit_jail"),
        ("Przejdź do Ulicy Belwederskiej (N2)", None, 22),
        ("Odbierz od każdego gracza 1$", "collect_1"),
        ("Przesuń się o 1 pole lub weź kolejną kartę szansy", "move_or_card"),
        ("Przejdź na start", None, 0),
        ("Przesuń się od 1-5 pól", "move_1_5"),
        ("Zapłać banku 2$", "pay_2"),
        ("Odbierz 2$ od banku", "get_2")
    ]
    
    wybrana = random.choice(opcje)
    print_with_delay(f"\n🎴 Karta Szansy: {wybrana[0]}")
    
    if wybrana[1] == "exit_jail":
        gracz['exit_jail'] = True
        print_with_delay("Masz kartę 'Wyjdź z więzienia' do wykorzystania!")
    
    elif wybrana[1] == "collect_1":
        for i, g in enumerate(gracze):
            if i != numer_gracza and g['kasa'] >= 1:
                g['kasa'] -= 1
                gracz['kasa'] += 1
        print_with_delay("Odebrano 1$ od każdego gracza")
    
    elif wybrana[1] == "move_or_card":
        if random.random() < 0.5:
            przenies_gracza(gracz, (gracz['pole'] + 1) % 24)
            obsluz_nieruchomosc(gracz, numer_gracza)
        else:
            print_with_delay("Losujesz kolejną kartę szansy")
            szansa(numer_gracza)
    
    elif wybrana[1] == "move_1_5":
        ruch = random.randint(1, 5)
        przenies_gracza(gracz, (gracz['pole'] + ruch) % 24)
        obsluz_nieruchomosc(gracz, numer_gracza)
    
    elif wybrana[1] == "pay_2":
        gracz['kasa'] -= 2
        print_with_delay("Zapłaciłeś bankowi 2$")
    
    elif wybrana[1] == "get_2":
        gracz['kasa'] += 2
        print_with_delay("Otrzymałeś 2$ od banku")
    
    elif len(wybrana) == 3:
        przenies_gracza(gracz, wybrana[2])
        if wybrana[2] != 0:
            obsluz_nieruchomosc(gracz, numer_gracza)
        else:
            gracz['kasa'] += 2
            print_with_delay("💰 Przejście przez START! +2$")
    
    else:
        kolory = wybrana[1]
        nastepne_pole = znajdz_nastepne_pole(gracz, kolory)
        if nastepne_pole is not None:
            przenies_gracza(gracz, nastepne_pole)
            obsluz_nieruchomosc(gracz, numer_gracza)
        else:
            print_with_delay("Nie znaleziono odpowiedniego pola")

def ruch(numer_gracza):
    global gracze, pozostale_nieruchomosci, nieruchomosci_graczy

    if gracze[numer_gracza]['kasa'] < 0:
        return

    # Obsługa więzienia
    if gracze[numer_gracza]['injail']:
        gracze[numer_gracza]['jail_turns'] += 1
        print_with_delay(f"⏳ Gracz {numer_gracza + 1} jest w więzieniu (tura {gracze[numer_gracza]['jail_turns']}/2)")
        
        if gracze[numer_gracza]['exit_jail']:
            gracze[numer_gracza]['injail'] = False
            gracze[numer_gracza]['exit_jail'] = False
            gracze[numer_gracza]['jail_turns'] = 0
            print_with_delay(f"🎴 Gracz {numer_gracza + 1} używa karty 'Wyjdź z więzienia' i opuszcza więzienie!")
        elif gracze[numer_gracza]['jail_turns'] >= 2:
            gracze[numer_gracza]['injail'] = False
            gracze[numer_gracza]['jail_turns'] = 0
            print_with_delay(f"🔓 Gracz {numer_gracza + 1} opuszcza więzienie po 2 turach")
        else:
            return

    rzut = random.randint(1, 6)
    print_with_delay(f"\n🎲 Gracz {numer_gracza + 1} rzucił: {rzut}")
    pole_gracza = gracze[numer_gracza]['pole']
    pole_gracza += rzut

    if pole_gracza > 23:
        pole_gracza -= 24
        gracze[numer_gracza]['kasa'] += 2
        print_with_delay("💰 Przejście przez START! Gracz dostaje 2 zł")

    obecne_pole = pola[pole_gracza]
    print_with_delay(f"📍 Gracz {numer_gracza + 1} stanął na polu: {obecne_pole}")

    if obecne_pole in nieruchomosci:
        indeks = nieruchomosci.index(obecne_pole)
        koszt = math.ceil((indeks+1) / 4)
        if obecne_pole[0] == 'N':
          koszt += 1
        nieruchomosc_zajeta = False
        for i in range(len(gracze)):
            if obecne_pole in nieruchomosci_graczy[i]:
                nieruchomosc_zajeta = True
                if i != numer_gracza:
                    gracze[numer_gracza]['kasa'] -= koszt
                    gracze[i]['kasa'] += koszt
                    print_with_delay(f"🏠 Nieruchomość należy do gracza {i + 1}. Czynsz: {koszt} zł")
                else:
                    print_with_delay("✅ To twoja nieruchomość.")
                break

        if not nieruchomosc_zajeta:
            if gracze[numer_gracza]['kasa'] >= koszt:
                gracze[numer_gracza]['kasa'] -= koszt
                nieruchomosci_graczy[numer_gracza].append(obecne_pole)
                pozostale_nieruchomosci.remove(obecne_pole)
                print_with_delay(f"💼 Gracz {numer_gracza + 1} kupuje nieruchomość {obecne_pole} za {koszt} zł")
            else:
                print_with_delay(f"❌ Gracz {numer_gracza + 1} nie ma wystarczająco środków (koszt: {koszt})")
    elif obecne_pole == 'Szansa':
        szansa(numer_gracza)
    elif obecne_pole == 'Więzienie':
        if not gracze[numer_gracza]['injail']:
            gracze[numer_gracza]['injail'] = True
            gracze[numer_gracza]['jail_turns'] = 0
            gracze[numer_gracza]['pole'] = pola.index('Więzienie')
            print_with_delay("🚓 Gracz trafia do więzienia! Musi odsiedzieć 2 tury (chyba że ma kartę 'Wyjdź z więzienia')")
        else:
            print_with_delay("🔒 Gracz jest już w więzieniu - pozostaje tam dalej")
    else:
        print_with_delay("🔸 Zwykłe pole – nic się nie dzieje.")

    gracze[numer_gracza]['pole'] = pole_gracza
    print_with_delay(f"💰 Kasa gracza {numer_gracza + 1}: {gracze[numer_gracza]['kasa']} zł")

def sprawdz_wygrana():
    """Sprawdza, czy któryś gracz wygrał"""
    aktywni_gracze = [g for g in gracze if g['kasa'] >= 0]
    
    if len(aktywni_gracze) == 1:
        zwyciezca = gracze.index(aktywni_gracze[0])
        print_with_delay(f"\n🎉🎉🎉 Gracz {zwyciezca + 1} wygrywa grę! 🎉🎉🎉")
        print_with_delay("Powód: Wszyscy inni gracze zbankrutowali")
        return True
    
    for i, nier in enumerate(nieruchomosci_graczy):
        if len(nier) == len(nieruchomosci):
            print_with_delay(f"\n🏆🏆🏆 Gracz {i + 1} wygrywa grę! 🏆🏆🏆")
            print_with_delay("Powód: Posiada wszystkie nieruchomości")
            return True
    
    return False

def pokaz_stan_graczy():
    print_with_delay("\n📊 Stan kont graczy:")
    for i, gracz in enumerate(gracze):
        status = ""
        if gracz['kasa'] < 0:
            status = " (BANKRUT)"
        elif gracz['injail']:
            status = f" (Więzienie, tura {gracz['jail_turns']}/2)"
        
        print_with_delay(f"Gracz {i + 1}: {gracz['kasa']} zł", end="")
        if gracz['exit_jail']:
            print_with_delay(" [Karta Wyjdź z Więzienia]", end="")
        print_with_delay(status)
    
    print_with_delay("\n🏠 Nieruchomości:")
    for i, nier in enumerate(nieruchomosci_graczy):
        print_with_delay(f"Gracz {i + 1}: {', '.join(nier) if nier else 'brak'}")
    print_with_delay()

# Funkcja główna
def main():
    global increment
    while True:
        print_with_delay(f'\n=== Runda: {increment+1} ===')
        ruch(increment % len(gracze))
        pokaz_stan_graczy()
        
        if sprawdz_wygrana():
            break
            
        time.sleep(0.5)  # Dodatkowe opóźnienie między rundami
        increment += 1

# Start gry
if __name__ == "__main__":
    main()
