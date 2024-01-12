from typing import List


class RowTable:
    def __init__(self):
        self.state_index = 0
        self.action = None
        self.reduce_non_terminal = ""
        self.reduce_content = []
        self.shifts = []

    def reduce_production_string(self):
        return f"{self.reduce_non_terminal} -> {self.reduce_content}"

    def __str__(self):
        return (
            f"Row: stateIndex= {self.state_index}, action='{self.action}', "
            f"reduceNonTerminal='{self.reduce_non_terminal}', reduceContent = {self.reduce_content}, "
            f"shifts = {self.shifts}"
        )
