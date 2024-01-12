from typing import List
from dataclasses import dataclass
from itertools import chain

@dataclass
class Item:
    left_hand_side: str
    right_hand_side: List[str]
    position_for_dot: int

    def get_left_hand_side(self) -> str:
        return self.left_hand_side

    def get_right_hand_side(self) -> List[str]:
        return self.right_hand_side

    def get_position_for_dot(self) -> int:
        return self.position_for_dot

    def dot_is_last(self) -> bool:
        return self.position_for_dot == len(self.right_hand_side)

    def __str__(self) -> str:
        right_hand_side1 = "".join(self.right_hand_side[:self.position_for_dot])
        right_hand_side2 = "".join(self.right_hand_side[self.position_for_dot:])
        return f"{self.left_hand_side} -> {right_hand_side1}.{right_hand_side2}"

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Item)
            and self.left_hand_side == other.left_hand_side
            and self.right_hand_side == other.right_hand_side
            and self.position_for_dot == other.position_for_dot
        )

    def __hash__(self) -> int:
        return hash((self.left_hand_side, tuple(self.right_hand_side), self.position_for_dot))
