from enum import Enum

# Bet - Place an initial bet if no one else has yet
# Check - Say "check" to avoid betting.
# Call -  Say "call" to match the bet someone else has made.
# Raise - Say "raise" to add more money to the betting pool.
# If you "raise," the other players will go around in a circle and
# choose to either "call" your new bet or fold.
# Fold - Say "fold" if someone else has bet, and you don't want to match their bet
class HandAct(Enum):
    NO_DEF = 'no_def'
    BET = 'bet'
    CALL = 'call'
    CHECK = 'check'
    RAISE = 'raise'
    FOLD = 'fold'


