import threading
import time
from network import Network
from tkinter import *
import sys
from signpage import Page, SignPage


def logtcp(dir, byte_data):
    """
    log direction and all TCP byte array data
    return: void
    """
    if dir == 'sent':
        print(f'C LOG:Sent     >>>{byte_data}')
    else:
        print(f'C LOG:Received <<<{byte_data}')


def making_request_2():
    print('''
    It's your turn.
    You have 3 options:
    1. Call
    2. call & Raise
    3.Pass
    ''')
    num = input("Enter a number between 1-3: ")
    if num == 1:
        return "CALL"
    if num == 2:
        money = input("How much?")
        return "CANR" + str(money)
    if num == 3:
        return "PASS"


def making_request_1():
    print('''
    It's your turn.
    What would you like to do?
    1. Chek
    2. Raise
    3. Pass                                    
    ''')
    num = int(input("Enter a number between 1-3: "))  # to Liya
    if num == 1:
        return "CHEK"
    if num == 2:
        money = input("How much?")
        return "RAIS" + str(money)
    if num == 3:
        return "PASS"

def main(ip):
    n = Network(ip)

    if n is None:
        print("ERR~4~ The network is empty , there is no network")
        return

    sock = n.get_client()
    gameMsg = n.getP()
    game = gameMsg.getGame()
    player = gameMsg.getPlayer()


    first1 = True
    first2 = True

    while True:
        game = gameMsg.getGame()
        player = gameMsg.getPlayer()

        num_of_p = game.get_num_of_p()
        status = game.get_status()

        logtcp("receive", status)

        in_the_round = game.get_in_round()
        logtcp("receive", str("in_the_round ") + str(in_the_round))
        table = game.get_table()

        while in_the_round:

            player = gameMsg.getPlayer()
            data = ""

            logtcp("receive", str("player.get_is_turn() ") + str(player.get_is_turn()))
            if player.get_is_turn():

                logtcp("receive", str("get_money_in_the_pot ") + str(table.get_money_in_the_pot()))
                if table.get_money_in_the_pot():
                    data = making_request_2()
                else:
                    data = making_request_1()
                #time.sleep(5)

                try:
                    n.send(data)
                except Exception as e:
                    print(e)

            else:
                time.sleep(1)

            try:
                gameMsg = n.receive()
            except Exception as e:
                print(e)


        try:
            n.send(gameMsg)
            gameMsg = n.receive()
        except Exception as e:
            print(e)

    print('Bye')
    sock.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('127.0.0.1')
