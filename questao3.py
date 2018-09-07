# A ordem padronizada para o autômato é [delta, estado_final] onde delta
# é uma lista de listas contendo a função de transição e estado_final é
# uma lista contendo os estado finais do autômato.


def questao1(regex):
    return [[[("a", 1), ("b", 2)], [("a", 1), ("b", 2)], [("a", 2), ("b", 2)]], []]


def questao2(epsilon_automaton):
    return epsilon_automaton


def string_through_NFA(string, automaton):
    """
    searches each string's substring in the given automaton
    :return: returns True if the string belongs to the automaton and False otherwise
    """
    current_state = [0]
    transitions = []
    next_state = []
    for letter in string:
        for state in current_state:
            transitions.append(automaton[0][state])  # contains the possible transitions for the current state

        for delta in transitions:
            for i, v in enumerate(delta):
                if v[0] == letter:
                    next_state.append(v[1])
        # if no state was appended to next_state, the transition for this letter was not found. Nicolas Cage died.

        current_state = next_state
        next_state = []
        transitions = []

    for accepted_state in automaton[1]:
        for final_state in current_state:
            if accepted_state == final_state:
                return True
    return False


def substrings(structure, input_string):
    """
    :param structure: can be an automaton or a regex
    :param input_string: string to be sliced into substrings ans tested
    :return: substrings from string accepted by the structure
    """
    answer = []

    if isinstance(structure, str):
        automaton = questao2(questao1(structure))
    else:
        automaton = questao2(structure)

    # Goes through all substrings of the input_string
    for i, end_letter in enumerate(reversed(input_string)):
        end_index = len(input_string) - i
        for start_index, start_letter in enumerate(input_string):
            if start_index < end_index:
                substring = input_string[start_index:end_index]
                if string_through_NFA(substring, automaton):
                    answer.append(substring)

    return answer


def main():
    cadeia1 = "baabba"
    cadeia2 = "abacabc"

    automato1 = [[[("a", 0), ("b", 1)], [("a", 0), ("b", 2)], [("a", 2), ("b", 2)]], [2]]
    automato2 = [[[("a", 3)], [], [("a", 3)], [("b", 1), ("c", 1), ("b", 2), ("c", 2)]], [0, 1, 2]]
    automato3 = [[[("a", 4), ("b", 5), ("a", 1), ("b", 1)], [], [("b", 1)], [("a", 1)], [("a", 2), ("a", 4), ("b", 1)],
                  [("a", 1), ("b", 3), ("b", 5)]], [1]]
    automato4 = [[[("a", 3), ("b", 5), ("c", 6)], [], [("b", 5), ("c", 6)],
                  [("a", 1), ("a", 2), ("a", 3), ("a", 4), ("a", 5), ("b", 5), ("a", 6), ("c", 6)], [("c", 6)],
                  [("b", 1), ("b", 4), ("b", 5), ("b", 6), ("c", 6)], [("c", 1), ("c", 6)]], [0, 1, 2, 3, 4, 5, 6]]

    substrings_accepted = substrings(automato1, cadeia1)
    print("Primeiro automato com cadeia baabba")
    print(substrings_accepted)

    substrings_accepted = substrings(automato2, cadeia1)  # cadeia 1; automato 2
    print("\nSegundo automato com cadeia baabba")
    print(substrings_accepted)

    substrings_accepted = substrings(automato3, cadeia1)  # cadeia 1; automato 3
    print("\nTerceiro automato com cadeia baabba")
    print(substrings_accepted)

    substrings_accepted = substrings(automato4, cadeia1)  # cadeia 1; automato 4
    print("\nQuarto automato com cadeia baabba")
    print(substrings_accepted)

    substrings_accepted = substrings(automato2, cadeia2)  # cadeia 2; automato 2
    print("\nSegundo automato com cadeia abacabc")
    print(substrings_accepted)

    substrings_accepted = substrings(automato4, cadeia2)  # cadeia 2; automato 4
    print("\nQuarto automato com cadeia abacabc")
    print(substrings_accepted)


if __name__ == '__main__':
    main()
