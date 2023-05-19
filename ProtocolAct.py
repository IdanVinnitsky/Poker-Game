from enum import Enum

#
class ProtocolAct(Enum):
    NO_DEF = 'no_def'
    GAME = 'game'
    LOGIN = 'login'
    UPDATE_SCREEN = 'update_screen'
    WINNER = 'winner'
