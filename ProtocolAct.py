from enum import Enum


#
class ProtocolAct(Enum):
    NO_DEF = 'no_def'
    GAME = 'game'
    LOGIN = 'login'
    SIGNUP = 'signup'
    UPDATE_SCREEN = 'update_screen'
    WINNER = 'winner'
    REQUEST_START = 'request_game'
    MESSAGE = 'message'
