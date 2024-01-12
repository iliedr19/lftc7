from LR0.lr import LR
from LR0.grammar import Grammar
from State.state import State
from State.item import Item


class Tests:
    def __init__(self):
        self.grammar1 = Grammar()
        self.grammar1.load_from_file("Input_Output/GTest.txt")
        try:
            self.lr_alg = LR(self.grammar1)
        except Exception as e:
            raise RuntimeError(e)

    def run_closure_test(self):
        self.lr_alg.canonical_collection()
        result = self.lr_alg.closure(
            Item(
                self.lr_alg.get_working_grammar().get_starting_symbol(),
                self.lr_alg.get_working_grammar().get_productions_for_non_terminal(
                    self.lr_alg.get_grammar().get_starting_symbol()
                )[0],
                0
            )
        ).get_items()
        assert len(result) == 1
        assert result[0] == Item("S0", ["a", "A"], 0)
        print("Closure test 1 successful")

    def run_closure_test2(self):
        self.grammar1 = Grammar()
        self.grammar1.load_from_file("Input_Output/GTest2.txt")
        self.lr_alg = LR(self.grammar1)
        self.lr_alg.canonical_collection()
        result = self.lr_alg.closure(
            Item(
                self.lr_alg.get_working_grammar().get_starting_symbol(),
                self.lr_alg.get_working_grammar().get_productions_for_non_terminal(
                    self.lr_alg.get_grammar().get_starting_symbol()
                )[0],
                0
            )
        ).get_items()
        assert len(result) == 1
        assert result[0] == Item("S0", ["a"], 0)
        print("Closure test 2 successful")

    def run_closure_test3(self):
        self.grammar1 = Grammar()
        self.grammar1.load_from_file("Input_Output/GTest3.txt")
        self.lr_alg = LR(self.grammar1)
        self.lr_alg.canonical_collection()
        result = self.lr_alg.closure(
            Item(
                self.lr_alg.get_working_grammar().get_starting_symbol(),
                self.lr_alg.get_working_grammar().get_productions_for_non_terminal(
                    self.lr_alg.get_grammar().get_starting_symbol()
                )[0],
                0
            )
        ).get_items()
        assert len(result) == 3
        assert result[1] == Item("A", ["S"], 0)
        print("Closure test 3 successful")

    def run_all_closure_test(self):
        self.run_closure_test()
        self.run_closure_test2()
        self.run_closure_test3()

    def run_go_to_test1(self):
        self.grammar1 = Grammar()
        self.grammar1.load_from_file("Input_Output/GTest.txt")
        self.lr_alg = LR(self.grammar1)
        self.lr_alg.canonical_collection()
        state = self.lr_alg.closure(
            Item(
                self.lr_alg.get_working_grammar().get_starting_symbol(),
                self.lr_alg.get_working_grammar().get_productions_for_non_terminal(
                    self.lr_alg.get_grammar().get_starting_symbol()
                )[0],
                0
            )
        )
        result = self.lr_alg.go_to(state, state.get_symbols_succeeding_the_dot()[0])
        assert len(result.get_items()) == 2
        assert result.get_items()[1] == Item("A", ["a", "b"], 0)
        print("Go To Test 1 Successful")

    def run_go_to_test2(self):
        self.grammar1 = Grammar()
        self.grammar1.load_from_file("Input_Output/GTest2.txt")
        self.lr_alg = LR(self.grammar1)
        self.lr_alg.canonical_collection()
        state = self.lr_alg.closure(
            Item(
                self.lr_alg.get_working_grammar().get_starting_symbol(),
                self.lr_alg.get_working_grammar().get_productions_for_non_terminal(
                    self.lr_alg.get_grammar().get_starting_symbol()
                )[0],
                0
            )
        )
        result = self.lr_alg.go_to(state, state.get_symbols_succeeding_the_dot()[0])
        assert len(result.get_items()) == 1
        assert result.get_items()[1] == Item("S0", ["a"], 1)
        print("Go To Test 2 Successful")

    def run_all_go_to_tests(self):
        self.run_go_to_test1()
        self.run_go_to_test2()

    def run_all_canonical_tests(self):
        self.run_get_canonical_collection_test1()
        self.run_get_canonical_collection_test2()

    def run_get_canonical_collection_test1(self):
        self.grammar1 = Grammar()
        self.grammar1.load_from_file("Input_Output/GTest.txt")
        self.lr_alg = LR(self.grammar1)
        result = self.lr_alg.canonical_collection().get_states()
        assert len(result) == 6
        assert result[-1].get_items()[0] == Item("A", ["a", "b"], 2)
        print("Canonical Test 1 Successful")

    def run_get_canonical_collection_test2(self):
        self.grammar1 = Grammar()
        self.grammar1.load_from_file("Input_Output/GTest3.txt")
        self.lr_alg = LR(self.grammar1)
        result = self.lr_alg.canonical_collection().get_states()
        assert len(result) == 1
        assert result[0].get_items()[0] == Item("A", ["a"], 1)
        print("Canonical Test 2 Successful")
