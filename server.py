import socket
from _thread import *
import sys
from player import Player
import pickle

# server = "10.11.250.207"
server = "192.168.0.104"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("Waiting for a connection, Server Started")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 255, 0))]


def threaded_client(conn, player):

    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data
            if not data:
                print("Disconected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Recived :", data)
                print("Sending :", reply)
            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost connection")
    conn.close()


currentplayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentplayer))
    currentplayer += 1
