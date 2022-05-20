import pickle
import socket
import player

host = '192.168.1.34'
firstport = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((host, firstport))
print('serveur ouvert')
playerDict = {

}
rooms = {0 : []}
def getPlayerStatList(ipBlackList:list=[]):
    list = []
    for key in playerDict.keys():
        if not key in ipBlackList:
            list.append(playerDict[key].returnStat())
    return list

while True:
    for key in playerDict.keys():
        playerDict[key].move([playerDict[key] for key in playerDict.keys()])
    message = {}
    data, addr = sock.recvfrom(2048)
    data = pickle.loads(data)
    print(data)
    if type(data) == dict:
        if 'connection' in data.keys():
            rooms[0].append(addr)
            playerDict[addr[0]] = player.Player(data['connection'][0])
            message['character'] = playerDict[addr[0]].returnStat()
            message['playerList'] = getPlayerStatList()
        if 'player' in data.keys():
            playerDict[addr[0]].setMove(data['player'])
            if playerDict[addr[0]].do == 'grab':
                if playerDict[addr[0]].harpon == None:
                    playerDict[addr[0]].createHarpon()
                print(playerDict[addr[0]].harpon)
            print('et oe')
            message['playerList'] = getPlayerStatList(addr[0])
            message['character'] = playerDict[addr[0]].returnStat()
    else:
        message = "HARRA"

    print(message)
    sock.sendto(pickle.dumps(message), addr)

sock.close()
