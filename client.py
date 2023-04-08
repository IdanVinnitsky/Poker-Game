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


def client_login():
    print("")


stop_flag = False


def print_every_5_seconds(string):
    global stop_flag
    while not stop_flag:
        print(string)
        time.sleep(5)


def main(ip):
    n = Network(ip)
    # window = Tk()

    if n is None:
        print("ERR~4~ The network is empty , there is no network")
        return

    sock = n.get_client()
    gameMsg = n.getP()
    game = gameMsg.getGame()

    # Start a new thread to run the print_every_5_seconds function with a message as parameter
    msg = ""
    thread = threading.Thread(target=print_every_5_seconds, args=(msg,))
    thread.daemon = True  # Set daemon flag so the thread exits when the main program exits
    thread.start()

    while True:
        num_of_p = game.get_num_of_p()
        status = game.get_status()

        if num_of_p == 1:
            new_msg = status
            thread._args = (new_msg,)  # Set the new message as the argument for the thread
        elif num_of_p > 1:
            new_msg = status
            thread._args = (new_msg,)



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
