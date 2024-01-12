from Utils.pair import Pair
from State.state import State
from LR0.canonicalcollection import CanonicalCollection
from State.stateactiontype import StateActionType
from ParsingTable.parsingtable import ParsingTable
from ParsingTable.rowtable import RowTable
from ParsingTree.outputtree import OutputTree
from LR0.grammar import Grammar


class LR:
    def __init__(self, grammar):
        self.grammar = grammar
        self.working_grammar = grammar if grammar.get_is_enriched() else grammar.get_enriched_grammar()
        self.ordered_productions = grammar.get_ordered_productions()

    def get_non_terminal_preceded_by_dot(self, item):
        try:
            term = item.get_right_hand_side()[item.get_position_for_dot()]
            if term not in self.grammar.get_non_terminals():
                return None
            return term
        except Exception as e:
            return None

    def closure(self, item):
        old_closure = set()
        current_closure = {item}

        while old_closure != current_closure:
            old_closure = current_closure.copy()
            new_closure = current_closure.copy()
            for i in current_closure:
                non_terminal = self.get_non_terminal_preceded_by_dot(i)
                if non_terminal:
                    for prod in self.grammar.get_productions_for_non_terminal(non_terminal):
                        current_item = State.Item(non_terminal, prod, 0)
                        new_closure.add(current_item)
            current_closure = new_closure

        return State.State(current_closure)

    def go_to(self, state, elem):
        result = set()
        for i in state.get_items():
            try:
                non_terminal = i.get_right_hand_side()[i.get_position_for_dot()]
                if non_terminal == elem:
                    next_item = State.Item(i.get_left_hand_side(), i.get_right_hand_side(), i.get_position_for_dot() + 1)
                    new_state = self.closure(next_item)
                    result.update(new_state.get_items())
            except Exception as ignored:
                pass
        return State.State(result)

    def canonical_collection(self):
        canonical_collection = CanonicalCollection()
        canonical_collection.add_state(
            self.closure(
                State.Item(
                    self.working_grammar.get_starting_symbol(),
                    self.working_grammar.get_productions_for_non_terminal(self.working_grammar.get_starting_symbol())[0],
                    0
                )
            )
        )

        index = 0
        while index < len(canonical_collection.get_states()):
            for symbol in canonical_collection.get_states()[index].get_symbols_succeeding_the_dot():
                new_state = self.go_to(canonical_collection.get_states()[index], symbol)
                if len(new_state.get_items()) != 0:
                    index_state = canonical_collection.get_states().index(new_state)
                    if index_state == -1:
                        canonical_collection.add_state(new_state)
                        index_state = len(canonical_collection.get_states()) - 1
                    canonical_collection.connect_states(index, symbol, index_state)
            index += 1
        return canonical_collection

    def get_parsing_table(self, canonical_collection):
        parsing_table = ParsingTable()
        for i in range(len(self.canonical_collection().get_states())):
            state = self.canonical_collection().get_states()[i]
            row = RowTable()
            row.state_index = i
            row.action = state.get_state_action_type()
            row.shifts = []
            if state.get_state_action_type() == StateActionType.SHIFT_REDUCE_CONFLICT or state.get_state_action_type() == StateActionType.REDUCE_REDUCE_CONFLICT:
                for k2, v2 in canonical_collection.get_adjacency_list().items():
                    if v2 == row.state_index:
                        print("STATE INDEX ->", row.state_index)
                        self.write_to_file("Input_Output/Out2.txt", "STATE INDEX ->" + str(row.state_index))
                        print("SYMBOL ->", k2[1])
                        self.write_to_file("Input_Output/Out2.txt", "SYMBOL ->" + k2[1])
                        print("INITIAL STATE ->", k2[0])
                        self.write_to_file("Input_Output/Out2.txt", "INITIAL STATE ->" + str(k2[0]))
                        print(f"({k2[0]}, {k2[1]})", "->", row.state_index)
                        self.write_to_file("Input_Output/Out2.txt", f"({k2[0]}, {k2[1]}) -> {row.state_index}")
                        print("STATE ->", state)
                        self.write_to_file("Input_Output/Out2.txt", "STATE ->" + str(state))
                        break
                parsing_table.entries = []
                return parsing_table
            elif state.get_state_action_type() == StateActionType.REDUCE:
                item = next((item for item in state.get_items() if item.dot_is_last()), None)
                if item:
                    row.shifts = None
                    row.reduce_non_terminal = item.get_left_hand_side()
                    row.reduce_content = item.get_right_hand_side()
                else:
                    raise Exception("How did you even get here?")
            elif state.get_state_action_type() == StateActionType.ACCEPT:
                row.reduce_content = None
                row.reduce_non_terminal = None
                row.shifts = None
            elif state.get_state_action_type() == StateActionType.SHIFT:
                go_tos = []
                for k, v in canonical_collection.get_adjacency_list().items():
                    if k[0] == row.state_index:
                        go_tos.append(Pair.Pair(k[1], v))
                row.shifts = go_tos
                row.reduce_content = None
                row.reduce_non_terminal = None
            parsing_table.entries.append(row)
        return parsing_table

    def parse(self, input_stack, parsing_table, file_path):
        working_stack = []
        output_stack = []
        output_number_stack = []
        last_symbol = ""
        state_index = 0
        sem = True
        working_stack.append(Pair.Pair(last_symbol, state_index))
        last_row = None
        on_error_symbol = None

        try:
            while sem:
                if input_stack:
                    on_error_symbol = input_stack[-1]
                last_row = parsing_table.entries[state_index]
                entry = parsing_table.entries[state_index]
                if entry.action == StateActionType.SHIFT:
                    symbol = input_stack.pop()
                    state = next((state for state in entry.shifts if state.first == symbol), None)
                    if state:
                        state_index = state.second
                        last_symbol = symbol
                        working_stack.append(Pair.Pair(last_symbol, state_index))
                    else:
                        raise ValueError("Action is SHIFT but there are no matching states")
                elif entry.action == StateActionType.REDUCE:
                    reduce_content = entry.reduce_content.copy()
                    while working_stack and reduce_content and reduce_content[-1] == working_stack[-1].first:
                        reduce_content.pop()
                        working_stack.pop()
                    state = next((state for state in parsing_table.entries[working_stack[-1].second].shifts if state.first == entry.reduce_non_terminal), None)
                    state_index = state.second
                    last_symbol = entry.reduce_non_terminal
                    working_stack.append(Pair.Pair(last_symbol, state_index))
                    output_stack.append(entry.reduce_production_string())
                    index = Pair.Pair(entry.reduce_non_terminal, entry.reduce_content)
                    production_number = self.ordered_productions.index(index)
                    output_number_stack.append(production_number)
                else:
                    if entry.action == StateActionType.ACCEPT:
                        output = output_stack[::-1]
                        number_output = output_number_stack[::-1]
                        print("ACCEPTED")
                        self.write_to_file(file_path, "ACCEPTED")
                        print("Production strings:", output)
                        self.write_to_file(file_path, "Production strings:" + str(output))
                        print("Production number:", number_output)
                        self.write_to_file(file_path, "Production number:" + str(number_output))
                        output_tree = OutputTree(self.grammar)
                        output_tree.generate_tree_from_sequence(number_output)
                        print("The output tree:")
                        self.write_to_file(file_path, "The output tree:")
                        output_tree.print_tree(output_tree.get_root(), file_path)
                        sem = False
        except ValueError as e:
            print(f"ERROR at state {state_index} - before symbol {on_error_symbol}")
            print(last_row)
            self.write_to_file(file_path, f"ERROR at state {state_index} - before symbol {on_error_symbol}")
            self.write_to_file(file_path, str(last_row))

    def write_to_file(self, file, line):
        with open(file, "a") as file_writer:
            file_writer.write(line + "\n")

    def get_grammar(self):
        return self.grammar

    def get_working_grammar(self):
        return self.working_grammar
