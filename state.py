from collections import namedtuple
from LR0.grammar import Grammar

# Define a named tuple to represent an Item
Item = namedtuple("Item", ["left_hand_side", "right_hand_side", "position_for_dot"])


class State:
    def __init__(self, states):
        self.items = states
        self.set_action_for_state()

    def get_items(self):
        return self.items

    def get_state_action_type(self):
        return self.state_action_type

    def get_symbols_succeeding_the_dot(self):
        symbols = set()

        for i in self.items:
            if i.position_for_dot < len(i.right_hand_side):
                symbols.add(i.right_hand_side[i.position_for_dot])

        return list(symbols)

    def set_action_for_state(self):
        if (
            len(self.items) == 1
            and self.items[0].right_hand_side[self.items[0].position_for_dot]
            == len(self.items[0].right_hand_side)
            and self.items[0].left_hand_side == Grammar.get_enriched_starting_grammar_symbol()
        ):
            self.state_action_type = "ACCEPT"
        elif len(self.items) == 1 and self.items[0].right_hand_side[self.items[0].position_for_dot] == len(
            self.items[0].right_hand_side
        ):
            self.state_action_type = "REDUCE"
        elif len(self.items) >= 1 and all(
            len(i.right_hand_side) > i.position_for_dot for i in self.items
        ):
            self.state_action_type = "SHIFT"
        elif len(self.items) > 1 and all(
            len(i.right_hand_side) == i.position_for_dot for i in self.items
        ):
            self.state_action_type = "REDUCE_REDUCE_CONFLICT"
        else:
            self.state_action_type = "SHIFT_REDUCE_CONFLICT"

    def __hash__(self):
        return hash(tuple(self.items))

    def __eq__(self, other):
        return isinstance(other, State) and self.items == other.get_items()

    def __str__(self):
        return f"{self.state_action_type} - {self.items}"
