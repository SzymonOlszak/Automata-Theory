# ----------------Zadanie wykonane na ocenę 4----------------
"""
Słownik 'states' mapuje nazwy stanów na ich wartości numeryczne odpowiadające wrzuconej kwocie (0-16 zł).
W momencie przekroczenia wartości 9 zł, pojawia się możliwość przejścia do stanu akcpeptującego - kupno biletu na basen.
Przy osiągnięciu wartości 12 zł lub większej automat nie przewiduje możliwości wrzucenia monet, pozostaje wybór biletów.
"""
states = {"q0": {"q1": 1, "q2": 2, "q5": 5},
          "q1": {"q2": 2, "q3": 3, "q6": 6},
          "q2": {"q3": 3, "q4": 4, "q7": 7},
          "q3": {"q4": 4, "q5": 5, "q8": 8},
          "q4": {"q5": 5, "q6": 6, "q9": 9},
          "q5": {"q6": 6, "q7": 7, "q10": 10},
          "q6": {"q7": 7, "q8": 8, "q11": 11},
          "q7": {"q8": 8, "q9": 9, "q12": 12},
          "q8": {"q9": 9, "q10": 10, "q13": 13},
          "q9": {"q10": 10, "q11": 11, "q14": 14, "qP": "P"},
          "q10": {"q11": 1, "q12": 12, "q15": 15, "qPR1": "P"},
          "q11": {"q12": 12, "q13": 13, "q16": 16, "qPR2": "P"},
          "q12": {"qPS": "PS", "qPR3": "P"},
          "q13": {"qPSR1": "PS", "qPR4": "P"},
          "q14": {"qPSR2": "PS", "qPR5": "P"},
          "q15": {"qPSR3": "PS", "qPR6": "P"},
          "q16": {"qPSR4": "PS", "qPR7": "P"}
          }


def run_dfa():
    global current_state, save_state, list_states

    current_state = "q0"  # Zapisuje aktualny stan
    list_states = ['q0']  # Historia przejść stanów

    print("\nWITAMY")
    print("Koszt biletu na basen - 9 zł, koszt biletu na basen i saunę - 12 zł.\n")
    while True:
        value = None
        """
        Weryfikacja zebranej kwoty w celu zakomunikowania użytkownikowi, jakimi opcjami dysponuje.
        """
        if int(current_state[1:]) < 9:
            value = input("\nWrzuć monetę 1,2 lub 5 zł")
        elif 9 <= int(current_state[1:]) < 12:
            value = input("\nWrzuć monetę 1,2 lub 5 zł lub wybierz bilet na pływalnię - P")
        else:
            value = input("\nWybierz bilet, P - pływalnia, PS-pływalnia + sauna")

        """
        Weryfikacja, czy zebrana kwota pozwala na wejście do stanu akceptującego.
        Jeśli tak, następuje wejście do funkcji kończącej i przerwanie pętli.
        """
        if value == "P" and int(current_state[1:]) >= 9:
            set_final_state(value)
            break

        elif value == "PS" and int(current_state[1:]) >= 12:
            set_final_state(value)
            break
        else:
            if value == "P" or value == "PS":
                print("Zbyt mało środków na zakup biletu")
                continue
            elif int(current_state[1:]) >= 12:         # Jeśli osiagnięto kwotę potrzebną do kupna biletów, to nie ma możliwości jej zwiększenia.
                print("\nBrak możliwości dodania środków - wybierz bilet")
                continue
        # Weryfikacja, czy wprowadzone kwoty należą do alfabetu wejściowego
        if value in ["1", "2", "5"]:
            change_state(value)
        else:
            continue


def change_state(value):
    """
    Realizacja funkcji przejścia. Następuje przejście do nowego stanu na podstawie tabeli przejść automatu.
    Wartość monety (1, 2 lub 5 zł) jest mapowana na indeks 0, 1 lub 2 na podstawie kolejności wartości zdefiniowanej
    w stanie początkowym q0. Uzyskany indeks służy do wyboru odpowiedniego klucza z aktualnego stanu, co determinuje
    kolejny stan automatu.
    """
    global current_state
    current_state = list(states[f"{current_state}"].keys())[list(states["q0"].values()).index(int(value))]
    print(f"\nAktualny stan konta: {current_state[1:]} zł")
    save_history(current_state)


def save_history(state):
    """
    Zapis historii stanów w celu wyświetlenia historii przejść.
    """
    list_states.append(state)
    print(" -> ".join(list_states))


def set_final_state(ticket):
    """
    Funkcja przenosząca automat do odpowiedniego stanu akceptującego.
    Dla stanów qP oraz qPS przypisywana jest reszta 0, a dla pozostałych stanów akceptująych reszta odczytywana
    jest za pomocą ostatniego znaku w nazwie stanu, który odpowiada wartości reszty.
    """
    global current_state

    if ticket == "P":
        current_state = list(states[f"{current_state}"].keys())[list(states[current_state].values()).index("P")]
        list_states.append(current_state)
        if current_state == "qP":
            change = 0
        else:
            change = current_state[-1]
        print(f"\nDziękujemy za zakup biletu na basen, wydano {change} zł reszty.\n")
    else:
        current_state = list(states[f"{current_state}"].keys())[list(states[current_state].values()).index("PS")]
        list_states.append(current_state)
        if current_state == "qPS":
            change = 0
        else:
            change = current_state[-1]
        print(f"\nDziękujemy za zakup biletu na basen i saunę, wydano {change} zł reszty.\n")
    print(" -> ".join(list_states))


if __name__ == '__main__':
    # while True:
    run_dfa()










