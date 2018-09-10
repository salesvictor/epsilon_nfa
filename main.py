from substring import *


def main():
    # Casos de teste:
    regex1 = "(a+b)*bb(b+a)*"
    regex2 = "(a(b+c))*"
    regex3 = "a*b+b*a"
    regex4 = "a*b*c*"

    string1 = "baabba"
    string2 = "abacabc"

    print("Cadeia 1: " + string1 + "\n")
    print("\tregex 1: " + regex1)
    print("\tSubstrings aceitas: " + str(list(set(substrings(regex1, string1)))) + "\n")
    print("\tregex 2: " + regex2)
    print("\tSubstrings aceitas: " + str(list(set(substrings(regex2, string1)))) + "\n")
    print("\tregex 3: " + regex3)
    print("\tSubstrings aceitas: " + str(list(set(substrings(regex3, string1)))) + "\n")
    print("\tregex 4: " + regex4)
    print("\tSubstrings aceitas: " + str(list(set(substrings(regex4, string1)))) + "\n\n")
    print("Cadeia 2: " + string2 + "\n")
    print("\tregex 2: " + regex2)
    print("\tSubstrings aceitas: " + str(list(set(substrings(regex2, string2)))) + "\n")
    print("\tregex 4: " + regex4)
    print("\tSubstrings aceitas: " + str(list(set(substrings(regex4, string2)))) + "\n")


if __name__ == '__main__':
    main()
