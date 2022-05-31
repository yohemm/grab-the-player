import pickle
import socket
import player
import random
import object

host = '192.168.1.15'
firstport = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((host, firstport))
print('serveur ouvert')
playerDict = {

}
rooms = {0 : []}
srcObjs = ['src/bush.png']
objs = {i:[object.Object(src=random.choice(srcObjs), pos=[random.randint(-800, 800), random.randint(-600, 600)], size=random.randint(100, 250) ,z=1) for a in range(random.randint(8,10))] for i in rooms.keys()}

def findRoom(ip):
    for room in rooms.keys():
        if ip in rooms[room]:return room

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
    if type(data) == dict:
        if 'disconnection' in data.keys():
            del playerDict[addr[0]]
            message = {'disconnection' : True}
        if 'connection' in data.keys():
            rooms[0].append(addr[0])
            playerDict[addr[0]] = player.Player(data['connection'][0])
            message['character'] = playerDict[addr[0]].returnStat()
            message['playerList'] = getPlayerStatList()
            message['objs'] = [obj.returnStat() for obj in objs[findRoom(addr[0])]]
        if 'player' in data.keys():
            playerDict[addr[0]].setMove(data['player'])
            if playerDict[addr[0]].do == 'grab':
                if playerDict[addr[0]].harpon == None:
                    if playerDict[addr[0]].changeMana(-50):playerDict[addr[0]].createHarpon()
            message['playerList'] = getPlayerStatList(addr[0])
            message['character'] = playerDict[addr[0]].returnStat()
    else:
        message = "HARRA"
    sock.sendto(pickle.dumps(message), addr)
sock.close()
