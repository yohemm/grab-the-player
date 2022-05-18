import socket
import pickle


def send(message):

    # message sent to server
    print(message)
    s.send(pickle.dumps(message))

    # message received from server
    data = s.recv(1024)
    dataDecode = pickle.loads(data)

    # print the received message
    # here it would be a reverse of sent message
    print('Received from the server :', str(dataDecode))
    if dataDecode == []:
        s.close()
# local host IP '127.0.0.1'
host = '192.168.1.15'

# Define the port on which you want to connect
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server on local computer
s.connect((host, port))
# message you send to server
# close the connection


if __name__ == '__main__':
    send('aka')