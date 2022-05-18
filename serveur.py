import socket
from threading import Thread

HOST = '192.168.1.15'
PORT = 6390

# Cretaion du socket

def send(client):
    while True:
        msg = input('->').encode('utf-8')
        client.send(msg)


def reception(client):
    while True:
        requete_client = client.recv(500).decode('utf-8')
        print(requete_client)
        if not requete_client:
            print('close')
            break


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.bind((HOST,PORT))
socket.listen(1)

#Attend la connection au client
client, ip = socket.accept()
print("Le client d'ip",ip,"s'est connecter")

envoi = Thread(target=send, args={client})
recep = Thread(target=reception, args={client})

envoi.start()
recep.start()

recep.join()

client.close()
socket.close()