import socket
from _thread import *
import numpy as np
import sys
import pickle

from player import Player
from circle import Circle

server = "192.168.0.59"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection, Server started")


width, height = 800, 600
circles = [players, ball] = [
    [
        Player(8, np.array([width / 2 - 50, height / 2]), 25, (200, 30, 30), 1.5, 2, 0.3, 0.98, 3.3),
        Player(8, np.array([width / 2 + 50, height / 2]), 25, (30, 30, 200), 1.5, 2, 0.3, 0.98, 3.3)
    ],
    Circle(1, np.array([width / 2, height / 2]), 15, (255, 255, 255), 30, 2, 0, 0.99)
]

def threaded_client(connection, player_id):
    global players, ball, circles
    connection.send(pickle.dumps([players[player_id], [[players[i] for i in range(len(players)) if i != player_id], ball]]))

    reply = ""
    while True:
        try:
            data = pickle.loads(connection.recv(2048))
            player = players[player_id] = data

            # resolve collisions
            for i in range(len(players)):
                for j in range(i + 1, len(players)):
                    players[i].collide(players[j])
                players[i].collide(ball)
                players[i].shoot(ball)

            ball.update(np.zeros(2), width, height)

            # display and bounce circles
            for circle in [ball] + players:
                circle.bounce(width, height)

            if not data:
                print("Disconnected")
                break
            else:
                reply = [player, [players[i] for i in range(len(players)) if i != player_id], ball]

                # print("Received", data)
                # print("Sending", reply)
            
            connection.sendall(pickle.dumps(reply))
        except:
            print("THREADED CLIENT ERROR")
            break

    print("Lost connection")
    connection.close()

current_players = 0
while True:
    conn, addr = s.accept()
    print("Connected to", addr)

    start_new_thread(threaded_client, (conn, current_players))
    current_players += 1