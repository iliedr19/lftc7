import os
from LR0.canonicalcollection import CanonicalCollection
from LR0.grammar import Grammar
from LR0.lr import LR
from ParsingTable.parsingtable import ParsingTable
from Utils.pair import Pair
from Scanner.myscanner import MyScanner
from Tests.tests import Tests


def print_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(str(content))


def print_menu():
    print("\n\n0. Exit")
    print("1. Print non-terminals")
    print("2. Print terminals")
    print("3. Print starting symbol")
    print("4. Print all productions")
    print("5. Print all productions for a non terminal")
    print("6. Is the grammar a context free grammar (CFG) ?")
    print("7. Run LR0 for G1.txt and parse Sequence.txt")
    print("8. Run LR0 for G2.txt")
    print("9. Run LR0 for G3.txt")
    print("10. Run tests")


def print_menu_parser():
    print("\n1. Parse P1.txt")
    print("2. Parse P2.txt")
    print("3. Parse P3.txt")
    print("4. Exit\n")


def run_grammar():
    grammar = Grammar()
    grammar.load_from_file("Input_Output/G1.txt")
    not_stopped = True

    while not_stopped:
        print_menu()
        option = int(input("Enter your option: "))

        if option == 0:
            not_stopped = False
        elif option == 1:
            print(f"\n\nNon-terminals -> {grammar.get_non_terminals()}")
        elif option == 2:
            print(f"\n\nTerminals -> {grammar.get_terminals()}")
        elif option == 3:
            print(f"\n\nStarting symbol -> {grammar.get_starting_symbol()}")
        elif option == 4:
            print("\n\nAll productions: ")
            for lhs, rhs in grammar.get_productions().items():
                print(f"{lhs} -> {rhs}")
        elif option == 5:
            non_terminal = input("Enter a non-terminal: ")
            print(f"\n\nProductions for the non-terminal: {non_terminal}")
            try:
                productions = grammar.get_productions()[non_terminal]
                for rhs in productions:
                    print(f"{non_terminal} -> {rhs}")
            except KeyError:
                print("This is not a defined non-terminal")
        elif option == 6:
            print(f"\n\nIs it a context free grammar (CFG) ? {grammar.is_CFG()}")
        elif option == 7:
            empty_file("Input_Output/Out1.txt")

            grammar1 = Grammar()
            grammar1.load_from_file("Input_Output/G1.txt")
            lr_alg = LR(grammar1)
            canonical_collection = lr_alg.canonical_collection()

            print("States")
            for i, state in enumerate(canonical_collection.get_states()):
                print(f"{i} {state}")

            print("\nState transitions")
            for key, value in canonical_collection.get_adjacency_list().items():
                print(f"{key} -> {value}")

            parsing_table = lr_alg.get_parsing_table(canonical_collection)
            if not parsing_table.entries:
                print("We have conflicts in the parsing table so we can't go further with the algorithm")
                write_to_file("Input_Output/Out2.txt", "We have conflicts in the parsing table so we can't go further with the algorithm")
            else:
                print(parsing_table)

            word = read_sequence("Input_Output/Sequence.txt")
            lr_alg.parse(word, parsing_table, "Input_Output/Out1.txt")

        elif option == 8:
            grammar2 = Grammar()
            grammar2.load_from_file("Input_Output/G2.txt")
            lr_alg2 = LR(grammar2)
            canonical_collection2 = lr_alg2.canonical_collection()

            print("States")
            for i, state in enumerate(canonical_collection2.get_states()):
                print(f"{i} {state}")

            print("\nState transitions")
            for key, value in canonical_collection2.get_adjacency_list().items():
                print(f"{key} -> {value}")

            parsing_table2 = lr_alg2.get_parsing_table(canonical_collection2)
            if not parsing_table2.entries:
                print("We have conflicts in the parsing table so we can't go further with the algorithm")
                write_to_file("Input_Output/Out2.txt", "We have conflicts in the parsing table so we can't go further with the algorithm")
            else:
                print(parsing_table2)

            stop = False
            while not stop:
                print_menu_parser()
                option2 = int(input("Enter your option: "))

                if option2 == 1:
                    empty_file("Input_Output/Out2.txt")
                    scanner2 = MyScanner("Input_Output/p1.txt")
                    scanner2.scan()
                    print_to_file("Input_Output/p1PIF.txt", scanner2.get_pif())

                    word2 = read_first_elem_from_file("Input_Output/p1PIF.txt")
                    lr_alg2.parse(word2, parsing_table2, "Input_Output/Out2.txt")

                elif option2 == 2:
                    empty_file("Input_Output/Out2.txt")
                    scanner3 = MyScanner("Input_Output/p2.txt")
                    scanner3.scan()
                    print_to_file("Input_Output/p2PIF.txt", scanner3.get_pif())

                    word3 = read_first_elem_from_file("Input_Output/p2PIF.txt")
                    lr_alg2.parse(word3, parsing_table2, "Input_Output/Out2.txt")

                elif option2 == 3:
                    empty_file("Input_Output/Out2.txt")
                    scanner4 = MyScanner("Input_Output/p3.txt")
                    scanner4.scan()
                    print_to_file("Input_Output/p3PIF.txt", scanner4.get_pif())

                    word4 = read_first_elem_from_file("Input_Output/p3PIF.txt")
                    lr_alg2.parse(word4, parsing_table2, "Input_Output/Out2.txt")

                elif option2 == 4:
                    stop = True

        elif option == 10:
            test = Tests()
            test.run_all_closure_test()
            test.run_all_go_to_tests()
            test.run_all_canonical_tests()

    launch_app()


def read_sequence(filename):
    word_stack = []
    try:
        with open(filename, 'r') as file:
            line = file.readline()
            if line:
                word_stack.extend(line.strip()[::-1])
    except IOError as e:
        print(e)
    return word_stack


def read_from_file(filename):
    word_stack = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                word_stack.append(line.strip())
    except IOError as e:
        raise RuntimeError(e)
    return word_stack


def read_first_elem_from_file(filename):
    word_stack = []
    normal = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                split = line.split()
                normal.append(split[0])
        word_stack.extend(normal[::-1])
    except IOError as e:
        raise RuntimeError(e)
    return word_stack


def empty_file(file_path):
    with open(file_path, 'w'):
        pass


def write_to_file(file_path, line):
    with open(file_path, 'a') as file:
        file.write(line + '\n')


def launch_app():
    print("0. Exit")
    print("1. Grammar")
    option = int(input("Your option: "))

    if option == 1:
        run_grammar()
    elif option == 0:
        pass
    else:
        print("Invalid command!")


if __name__ == "__main__":
    launch_app()
