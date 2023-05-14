from enum import Enum

class HandAct(Enum):
    NO_DEF = 'no_def'
    BET = 'bet'
    CALL = 'call'
    CHECK = 'check'
    RAISE = 'raise'
    FOLD = 'fold'