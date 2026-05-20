states = {}

# Tworzenie wierszy tabeli dla stanów q1,q2,q3,q4
for j in range(0,5):
    for i in range(0, 10):
        if j == 0:
            if i >= 5:
                states[(str(i), f"q{j}")] = (str(i - 5), f"q2", "L")
                continue
            states[(str(i), f"q0")] = (str(i + 5), f"q1", "L")
        if j in [2, 4]:
            trans_digit= {2: "q4", 4: "q5"}
            no_trans = {2: "q3", 4: "qk"}
            if i == 9:
                states[(str(i), f"q{j}")] = (str(0), f"{trans_digit[j]}", "L")
                continue
            states[(str(i), f"q{j}")] = (str(i + 1), f"{no_trans[j]}", "L")
        elif j in [1,3]:
            which_state = {1: "q3", 3: "qk"}
            states[(str(i), f"q{j}")] = (str(i), f"{which_state[j]}", "L")

# Tworzenie tabeli dla stanu q5,qk i qe
for i in range(0, 10):
    for l in ["5", "k"]:
        states[(str(i), f"q{l}")] = (" ", f"qe", " ")
    states[(str(i), f"qe")] = (" ", " ", " ")

# Tworzenie stanów dla symboli końcowych
states[("_", "q0")] = (" ", "qe", " ")
for i in ["q1", "q3"]:
    states[("_", f"{i}")] = (" ", "qk", " ")
for i in [2, 4, 5]:
    states[("_", f"q{i}")] = ("1", "qk", " ")
for i in ["qe", "qk"]:
    states[("_", f"{i}")] = (" ", " ", " ")


sorted_states = sorted(states.items(),key=lambda x: x[0][1])
for key, value in sorted_states:
    print(f"{key} -> {value}")


def run_machine():
    current_state = "q0"
    states_history = ["q0",]
    digits_history = []
    tape = reversed("_" + input("Podaj maksymalnie trzycyfrową liczbę\n"))

    for digit in tape:
        print(f"\nAktualny stan: {current_state}")
        print(f"Wprowadzona cyfra/symbol: {digit}\n")
        pair = (digit, current_state)
        if pair not in states:
            print("Brak przejścia:", pair)
            break

        new_digit, current_state, move = states[pair]

        if move == "L":
            digits_history.append(new_digit)
            print("Przesunięto głowicę w lewo")
            states_history.append(current_state)
            print("Historia stanów: " + " -> ".join(states_history))

            continue
        else:
            states_history.append(current_state)
            print("Historia stanów: " + " -> ".join(states_history))
            if current_state in ["qe"]:
                if len(states_history) > 3:
                    print(f"-----PRZEKROCZONO LICZBĘ CYFR, LICZBA NIE ZOSTAŁA ZWIĘKSZONA-----\n WYNIK: SŁOWO ODRZUCONE")
                else:
                    print("-----NIE PODANO LICZBY-----")
                break
            digits_history.append(new_digit)
            print(digits_history)
            digits_history.reverse()

            print(f"Stan końcowy: {current_state} \nLiczba po zwiększeniu: {''.join(digits_history)} \n"
                  f"WYNIK: SŁOWO ZAAKCEPTOWANE")

            break


run_machine()