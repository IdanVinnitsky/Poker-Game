from enum import Enum

#
class ProtocolAct(Enum):
    NO_DEF = 'no_def'
    GAME = 'game'
    LOGIN = 'login'
    SIGNIN = 'signin'
    UPDATE_SCREEN = 'update_screen'
    WINNER = 'winner'
    REQUEST_START = 'request_game'
    MESSAGE = 'message'
