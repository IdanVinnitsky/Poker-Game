import pickle
import socket
import threading
from player import Player
from table import Table
from deck import Deck
from game import Game
from gamemsg import Data
import time

def logtcp(dir, byte_data):
    """
    log direction and all TCP byte array data
    return: void
    """
    if dir == 'sent':
        print(f'C LOG:Sent     >>>{byte_data}')
    else:
        print(f'C LOG:Received <<<{byte_data}')


stop_flag = False


def print_every_5_seconds(string):
    global stop_flag
    while not stop_flag:
        print(string)
        time.sleep(5)


def handle_client(sock, tid, addr, game):
    print(f'New Client number {tid} from {addr}')

    gameMsg = Data(game, tid)

    game = gameMsg.getGame()
    curr_palyer = gameMsg.getPlayer()

    game.add_player(curr_palyer)

    sock.send(pickle.dumps(gameMsg))

    # Start a new thread to run the print_every_5_seconds function with a message as parameter
    msg = ""
    thread1 = threading.Thread(target=print_every_5_seconds, args=(msg,))
    thread1.daemon = True  # Set daemon flag so the thread exits when the main program exits
    thread1.start()

    thread2 = threading.Thread(target=print_every_5_seconds, args=(msg,))
    thread2.daemon = True  # Set daemon flag so the thread exits when the main program exits
    thread2.start()

    while True:
        try:
            data = pickle.loads(sock.recv(2048))

            if not data:
                print("Disconnected")
                print("ERR~2~the data is empty")
                break
            else:
                num_of_p = game.get_num_of_p()
                players = game.get_players()
                deck = game.get_deck()

                if num_of_p == 1:
                    status = "Waiting for players....."
                    game.update_status(status)
                elif num_of_p > 1:
                    status = "player/s joined"
                    game.update_status(status)
                    #for player in players:
                    #    player.get_cards(deck)

                time.sleep(4)
                thread1._args = (logtcp("receive", data),)
                thread2._args = (logtcp("sent", gameMsg),)

            sock.sendall(pickle.dumps(gameMsg))
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    sock.close


def main():
    server = "0.0.0.0"
    port = 5555

    threads = []

    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        srv_sock.bind((server, port))

    except socket.error as e:
        print("ERR~1~ error in connecting/binding")
        print(str(e))

    srv_sock.listen()
    print("Waiting for a connection, Server Started")
    table = Table(1)
    deck = Deck()
    game = Game(1, table, deck)

    i = 1
    while True:
        print('\nMain thread: before accepting ...')
        cli_sock, addr = srv_sock.accept()
        t = threading.Thread(target=handle_client, args=(cli_sock, str(i), addr, game))
        t.start()
        i += 1
        threads.append(t)

        if i > 100000000:
            print('\nMain thread: going down for maintenance')
            print("ERR~3~ too many clients")
            break

    print('Main thread: waiting to all clients to die')
    for t in threads:
        t.join()
    srv_sock.close()
    print('Bye ..')


if __name__ == '__main__':
    main()
