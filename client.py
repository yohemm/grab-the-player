import pickle
import socket
import time

host = '192.168.1.15'
firstport = 12345
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clientSock.settimeout(1)

def sendAndRecp(message):
    start = time.time()
    clientSock.connect_ex((host, firstport))
    clientSock.sendto(pickle.dumps(message), (host, firstport))
    try:
        data, serveur = clientSock.recvfrom(2048)
        dataUncode = pickle.loads(data)
        elapsed = time.time() - start

        if __name__ == '__main__':
            print('serveur says:' + str(dataUncode) + ' in ' + str(elapsed) + 'ms')
        return dataUncode
    except TimeoutError:
        print('REQUEST TIMED OUT')

if __name__ == '__main__':
    sendAndRecp([4,9,12])
