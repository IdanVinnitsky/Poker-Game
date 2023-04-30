import pickle
import socket
import threading
from player import Player
from table import Table
from deck import Deck
from game import Game
from gamemsg import Data
import time

BUFFER_SIZE = 4096

table = Table(1)
deck = Deck()
game = Game(1, table, deck)



def logtcp(dir, byte_data):
    """
    log direction and all TCP byte array data
    return: void
    """
    if dir == 'sent':
        print(f'C LOG:Sent     >>>{byte_data}')
    else:
        print(f'C LOG:Received <<<{byte_data}')


def handle_request(request, player, table):
    req = request[0:4]
    money = request[4:]

    if req == "CHEK":
        return "OK", "CHEK"

    if req == "RAIS":
        player.sub_money(money)
        table.add_to_jackpot(money)
        table.update_money_in_the_pot()
        table.set_money_to_call(money)
        return "OK", "RAIS"

    if req == "CALL":
        to_call = table.money_to_call()
        player.sub_money(to_call)
        table.add_to_jackpot(to_call)
        return "OK", "CALL"

    if req == "CANR":
        to_call = table.money_to_call()
        player.sub_money(to_call)
        player.sub_money(money)
        return "OK", "CANR"

    if req == "PASS":
        return "OK", "PASS"

    return "", ""



before_the_round = True
threadLock = threading.Lock()
clients = []
counter = 0
end_round = True


def in_the_round(gameMsg, game, my_sock, player, tid):
    global threadLock
    global before_the_round
    global clients
    global BUFFER_SIZE
    global counter
    global end_round

    game.update_players()

    deck = game.get_deck()
    table = game.get_table()

    game.start_the_round()

    threadLock.acquire()

    if before_the_round:

        for player in game.get_players_in_the_round():
            player.get_cards(deck)

        deck.first_flop()

        flop = deck.get_flop()

        print(flop)
        before_the_round = False

    # Free lock to release next thread
    threadLock.release()

    flop = deck.get_flop()

    while len(deck.get_flop()) < 5:

        while counter < len(game.get_players_in_the_round()):

            if clients[counter][0] == my_sock:
                player.set_is_turn(True)
                request = ""
                answer = ("", "")
                while request == "" and answer[0] != "OK":
                    try:
                        my_sock.send(pickle.dumps(gameMsg))
                        # Receive data from client
                        request = pickle.loads(my_sock.recv(BUFFER_SIZE))
                        print(request)
                        answer = handle_request(request, player, table)


                    except Exception as e:
                        print(e)
                        break

                player.set_is_turn(False)
                threadLock.acquire()
                counter += 1
                print(str(counter) + "   tid:" + str(tid))
                threadLock.release()


            else:
                #print("its not your turn")
                time.sleep(5)

        threadLock.acquire()
        end_round = True
        if end_round:
            card = deck.get_card()
            flop.append(card)
            print ("len flop " + str(len(flop)))
            counter = 0
            print(str(counter) + " ipus  tid:" + str(tid))
            end_round = False
            deck.set_flop(flop)
            table.new_round()
            game.set_deck(deck)
            game.set_table(table)
            gameMsg.setGame(game)
            gameMsg.setPlayer(player)
        # Free lock to release next thread
        threadLock.release()

        time.sleep(2)

    print(flop)





def handle_client(sock, tid, addr):
    global BUFFER_SIZE
    global game
    global threadLock
    global clients

    print(f'New Client number {tid} from {addr}')
    player = Player("name"+str(tid))

    clients.append((sock, player))

    gameMsg = Data(game, player)

    game.add_player(player)

    sock.send(pickle.dumps(gameMsg))

    first1 = True
    first2 = True

    while True:
        try:
            # Receive data from client
            data = pickle.loads(sock.recv(BUFFER_SIZE))

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
                    time.sleep(2)

                    in_the_round(gameMsg, game, sock, player, tid)


                #logtcp("receive", data)
                #logtcp("sent", gameMsg)

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


    i = 1
    while True:
        print('\nMain thread: before accepting ...')
        try:
            cli_sock, addr = srv_sock.accept()
        except Exception as e:
            print(e)

        t = threading.Thread(target=handle_client, args=(cli_sock, str(i), addr))
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
