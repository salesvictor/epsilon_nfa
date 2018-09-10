from nfa_generator import *


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

    if structure[0] != '[':  # means st is a regex
        gr = Graph(structure)
        gr.generate_enfa()
        gr.generate_nfa()
        automaton = convert_graph_to_list(gr)
    else:  # means structure is a NFA or a eps-NFA
        automaton = structure  # this works only if structure is NFA

    # Goes through all substrings of the input_string
    for i, end_letter in enumerate(reversed(input_string)):
        end_index = len(input_string) - i
        for start_index, start_letter in enumerate(input_string):
            if start_index < end_index:
                substring = input_string[start_index:end_index]
                if string_through_NFA(substring, automaton):
                    answer.append(substring)

    # Resetting node.total to be able to create a new graph
    Node.total = 0

    return answer


def convert_graph_to_list(graph_format_automaton):
    list_format_automaton = [[], []]
    for accepted_state in graph_format_automaton.end:
        list_format_automaton[1].append(accepted_state.number)
    aux = []

    for node in graph_format_automaton.nodes:
        t = [node.number]
        for child in node.children:
            t.append([child[0][0], child[1].number])
        t = tuple(t)
        aux.append(t)
    aux.sort()

    for transition in aux:
        list_format_automaton[0].append(list(transition[1:]))

    return list_format_automaton


def convert_list_to_graph(list_format_automaton):
    # TODO
    return list_format_automaton
