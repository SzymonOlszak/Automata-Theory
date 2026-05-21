# Zadanie wykonane na ocenę 5
# Jako symbol pusty wykorzystano znak '_', a jako brak przesunięcia głowicy znak '-'.

# Inicjalizacja tabeli przejść, poniżej znajduje się kod generujący stany i symbole w celu oszczędzenia miejsca
states = {}

# Przejścia dla symboli alfabetu wejściowego (0-9) dla stanów q0/q1/q2/q3/q4
for j in range(0, 5):
    for i in range(0, 10):
        if j == 0:
            if i >= 5:   # Uwzględnienie przeniesienia dla cyfry jedności >= 5
                states[(str(i), f"q{j}")] = (str(i - 5), f"q2", "L")
                continue
            states[(str(i), f"q0")] = (str(i + 5), f"q1", "L")    # Zwyczajne dodanie 5 dla cyfr < 5
        if j in [2, 4]:
            trans_digit = {2: "q4", 4: "q5"}
            no_trans = {2: "q3", 4: "qs"}
            if i == 9:
                states[(str(i), f"q{j}")] = (str(0), f"{trans_digit[j]}", "L")
                continue
            states[(str(i), f"q{j}")] = (str(i + 1), f"{no_trans[j]}", "L")
        elif j in [1, 3]:
            which_state = {1: "q3", 3: "qs"}
            states[(str(i), f"q{j}")] = (str(i), f"{which_state[j]}", "L")

# Przejścia dla cyfr 0-9 dla stanów q5,qs, qk,qe
for i in range(0, 10):
    for l in ["q5", "qs"]:
        states[(str(i), f"{l}")] = ("", f"qe", "-")

# Przejścia dla symbolu pustego dla wszystkich stanów
states[("_", "q0")] = ("", "qe", "-")
for i in ["q1", "q3", "qs"]:
    states[("_", f"{i}")] = ("", "qk", "-")
for i in ["q2", "q4", "q5"]:
    states[("_", f"{i}")] = ("1", "qk", "-")

# Wydruk tabeli przejść
sorted_states = sorted(states.items(), key=lambda x: x[0][1])
for key, value in sorted_states:
    print(f"{key} -> {value}")


def run_machine():
    current_state = "q0"
    states_history = ["q0",]
    tape = list("_" + input("Podaj maksymalnie trzycyfrową liczbę\n"))
    head = len(tape) - 1     # Zapis długości taśmy na podstawie której wyznaczana jest pozycja początkowa głowicy (cyfra jedności)

    while True:
        digit = tape[head]  # Odczyt symbolu z taśmy przed głowę
        print(f"\nAktualny stan: {current_state}")
        print(f"Wprowadzona cyfra/symbol: {digit}\n")
        pair = (digit, current_state)  # Połączenie aktualnego stanu z symbolem na taśmie
        if pair not in states:
            print("Brak przejścia:", pair)
            break
        '''
        Za pomocą utworzonej funkcji przejścia odczytywane są: zapisywana cyfra, 
        następny stan oraz kierunek ruchu głowicy. Następnie na taśmie zostaje zapisana ustalona wcześniej cyfra
        '''
        new_digit, next_state, direction = states[pair]
        tape[head] = new_digit
        if next_state != "-":
            current_state = next_state
            states_history.append(current_state)

        if direction == "L":
            head -= 1   # Zmniejszenie zapisanej długości taśmy o 1, co przesuwa głowicę do cyfry na lewo od poprzedniej

            print("Przesunięto głowicę w lewo")
            print("Historia stanów: " + " -> ".join(states_history))
            continue

        if direction == "-":
            print("Historia stanów: " + " -> ".join(states_history))
            if current_state in ["qe"]:
                if len(states_history) > 3:
                    print(f"-----PRZEKROCZONO MAKSYMALNĄ LICZBĘ CYFR, LICZBA NIE ZOSTAŁA ZWIĘKSZONA-----\n WYNIK: SŁOWO ODRZUCONE")
                else:
                    print("-----NIE PODANO LICZBY-----")
                break

            print(f"Stan końcowy: {current_state} \nLiczba po zwiększeniu: {''.join(tape)}\n"
                f"WYNIK: SŁOWO ZAAKCEPTOWANE")

            break


run_machine()