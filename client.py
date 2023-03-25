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
        print(f'C LOG:Recieved <<<{byte_data}')


def client_login():
    print("")


def main(ip):
    n = Network(ip)
    #window = Tk()

    if n is None:
        print("ERR~4~ The network is empty , there is no network")
        return

    sock = n.get_client()
    gameMsg = n.getP()
    game = gameMsg.getGame()

    while True:
        num_of_p = game.get_num_of_p()
        status = game.get_status()

        if num_of_p == 1:
            print(status)

            try:
                gameMsg = n.send(gameMsg)
            except Exception as e:
                print(e)
            time.sleep(1)
            continue


        try:
            game = gameMsg.getGame()
            gameMsg = n.send(gameMsg)
        except Exception as e:
            print(e)

    print('Bye')
    sock.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('127.0.0.1')
