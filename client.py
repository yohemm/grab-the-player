from threading import Thread
import socket

def send(client):
    while True:
        msg = input('->').encode('utf-8')
        socket.send(msg)
def reception(client):
    while True:
        requete_serveur = socket.recv(500).decode ('utf-8')
        print(requete_serveur)

HOST = '192.168.1.15'
PORT = 6390

# Cretaion du socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect((HOST,PORT))

envoi = Thread(target=send, args={socket})
recep = Thread(target=reception, args={socket})

envoi.start()
recep.start()