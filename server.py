import pickle
import socket
import threading

def logtcp(dir, byte_data):
    """
    log direction and all TCP byte array data
    return: void
    """
    if dir == 'sent':
        print(f'C LOG:Sent     >>>{byte_data}')
    else:
        print(f'C LOG:Recieved <<<{byte_data}')


def handle_client(sock, tid, addr, game):

    print(f'New Client number {tid} from {addr}')

    gameMsg = Data(game, tid)

    sock.send(pickle.dumps(gameMsg))

    current_game = game
    while True:
        try:
            data = pickle.loads(sock.recv(2048))

            if not data:
                print("Disconnected")
                print("ERR~2~the data is empty")
                break
            else:

                current_game.setPlayer(int(tid), data.getGame().getPlayer(int(tid)))
                current_game.getPlayer(int(tid)).setConnected()

                gameMsg = Data(game, tid)

                print("Received: ", data)
                print("Sending: ", gameMsg)

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

    game_counter = 0

    i = 0
    while True:
        print('\nMain thread: before accepting ...')
        cli_sock, addr = srv_sock.accept()
        t = threading.Thread(target=handle_client, args=(cli_sock, str(i), addr, games[game_counter]))
        t.start()
        i += 1
        threads.append(t)
        if i % 2 == 0:
            i = 0
            game_counter += 1

        if i > 100000000:
            print('\nMain thread: going down for maintenance')
            print("ERR~3~ too many clients")
            break

