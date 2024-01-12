from enum import Enum


class StateActionType(Enum):
    REDUCE = 1
    SHIFT = 2
    ACCEPT = 3
    SHIFT_REDUCE_CONFLICT = 4
    REDUCE_REDUCE_CONFLICT = 5
