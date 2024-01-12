from typing import List, Tuple
from Utils.pair import Pair


class Grammar:
    def __init__(self):
        self.ELEMENT_SEPARATOR = " "
        self.SEPARATOR_OR_TRANSITION = "\\|"
        self.TRANSITION_CONCATENATION = " "
        self.EPSILON = "EPS"
        self.SEPARATOR_LEFT_RIGHT_HAND_SIDE = "->"

        self.non_terminals = set()
        self.terminals = set()
        self.productions = dict()
        self.starting_symbol = ""
        self.is_CFG = False
        self.is_enriched = False
        self.enriched_starting_grammar_symbol="S0"

    def get_enriched_starting_grammar_symbol(self):
        return self.enriched_starting_grammar_symbol

    def process_production(self, production: str) -> None:
        left_and_right_hand_side = production.split(self.SEPARATOR_LEFT_RIGHT_HAND_SIDE)
        split_lhs = left_and_right_hand_side[0].split(self.TRANSITION_CONCATENATION)
        split_rhs = left_and_right_hand_side[1].split(self.SEPARATOR_OR_TRANSITION)

        self.productions.setdefault(tuple(split_lhs), [])
        for rhs in split_rhs:
            self.productions[tuple(split_lhs)].append(rhs.split(self.TRANSITION_CONCATENATION))

    def load_from_file(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as file:
                lines = file.read().splitlines()
                self.non_terminals = set(lines[0].split(self.ELEMENT_SEPARATOR))
                self.terminals = set(lines[1].split(self.ELEMENT_SEPARATOR))
                self.starting_symbol = lines[2]

                for line in lines[3:]:
                    self.process_production(line)

                self.is_CFG = self.check_if_CFG()
                self.is_enriched = False
        except FileNotFoundError as e:
            print(e)

    def check_if_CFG(self) -> bool:
        if self.starting_symbol not in self.non_terminals:
            return False

        for lhs, rhs in self.productions.items():
            if len(lhs) != 1 or lhs[0] not in self.non_terminals:
                return False

            for possible_next_moves in rhs:
                for move in possible_next_moves:
                    if move not in self.non_terminals and move not in self.terminals and move != self.EPSILON:
                        return False

        return True

    def get_enriched_grammar(self) -> 'Grammar':
        if self.is_enriched:
            raise Exception("The Grammar is already enriched!")

        enriched_grammar = Grammar()
        enriched_grammar.non_terminals = self.non_terminals.copy()
        enriched_grammar.terminals = self.terminals.copy()
        enriched_grammar.productions = self.productions.copy()
        enriched_grammar.starting_symbol = "S0"

        enriched_grammar.non_terminals.add("S0")
        enriched_grammar.productions.setdefault(("S0",), []).append((self.starting_symbol,))

        enriched_grammar.is_enriched = True
        return enriched_grammar

    def get_ordered_productions(self) -> List[Tuple[str, List[str]]]:
        result = []
        for lhs, rhs in self.productions.items():
            for prod in rhs:
                result.append((lhs[0], prod))  # Assuming Pair is a tuple
        return result

    def get_productions_for_non_terminal(self, non_terminal: str) -> List[List[str]]:
        return self.productions.get((non_terminal,), [])
