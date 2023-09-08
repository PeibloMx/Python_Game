import socket
from _thread import *
import sys

''' Poner direccion ip en la que esta conectado esta pc ipconfig IPv4'''
server = "10.31.141.174"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Esperando una conexion, servidor inicializado")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(0,0),(100,100)]
def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try: 
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Desconectado")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                    
                print("Recibido", data)
                print("Enviando", reply)
            
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Conexion perdida")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Conectado a:",addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1