from enum import Enum

class GameStatus(Enum):
    NO_DEF = 'no_def'
    INIT = 'INIT'
    WAITING = 'waiting'
    STARTED = 'started'
    REQUEST_START = 'request_started'