import pygame.event
import basic
import player
import pygame
import object
import client

class Main:
    def __init__(self, screenSize):
        self.menuPath=[]
        self.menuList=[
            basic.Menu('welcom',
                [
                    basic.Button(basic.Image('src/MenuGold.png', size=[400,200]), basic.Text(text='Jouer', font='src/font/Sriracha.ttf', size=24),  [screenSize[0]//2 - 200, screenSize[1]//2], [400,200])
                ],
                [
                    basic.Text('Bienvenue dans GrabThePlayer', 'src/font/SigmarOne.ttf', 32, pos=[screenSize[0]//2 - 300, 10] ),
                    basic.Text('préparer vous au combat Jeune Guerrier.\npartez a l\'aventure!', 'src/font/SigmarOne.ttf', 24, pos=[screenSize[0]//2 - 250, screenSize[1]//3])
                ],
                [
                    #IMG
                ]),

            basic.Menu('pause',
                [
                    basic.Button(basic.Image('src/MenuGold.png', size=[200,100]), basic.Text(text='play', font='src/font/Sriracha.ttf', size=20),  [screenSize[0]//2 - 100, screenSize[1]//3-50], [200,100]),
                    basic.Button(basic.Image('src/MenuGold.png', size=[200,100]), basic.Text(text='leave the party', font='src/font/Sriracha.ttf', size=20),  [screenSize[0]//2 - 100, screenSize[1]//3*2-50], [200,100])
                ],
                [
                    #TEXT
                ],
                [
                    #IMG
                ]),

            basic.Menu('settings',
                [
                    #Btn
                ],
                [
                    #TEXT
                ],
                [
                    #IMG
                ]),

            basic.Menu('settings-sound',
                [
                    #Btn
                ],
                [
                    #TEXT
                ],
                [
                    #IMG
                ])

        ]
        pygame.init()
        pygame.display.set_caption('GarbThePlayer')
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(screenSize)
        self.player = None
        self.playerList = []
        self.MoussePosGame = [self.screen.get_size()[0]//2, self.screen.get_size()[1]//2]
        pygame.mouse.set_pos(self.MoussePosGame)
        self.mousseSensitivity = 0.5
        self.menu = 'welcom'
        self.inGame = True
        self.toSend = {}
        self.map = {}
        self.objs = {
            -1: [],
            0: [],
            1: [],
            2: [],

        }
        self.getTicksLastFrame = pygame.time.get_ticks()

    def updatePlayerList(self, playerStatList):
        while not len(playerStatList) == len(self.playerList):
            if len(playerStatList) > len(self.playerList):
                self.playerList.append(player.Player())
            if len(playerStatList) < len(self.playerList):
                self.playerList = self.playerList[:len(self.playerList) - 2]

        for idStat in range(len(playerStatList)):
            self.playerList[idStat].changeStat(playerStatList[idStat])

    def changeMenu(self, newMenu):
        if newMenu == '':
            self.menuPath = []
            self.menu = newMenu
        else:
            if newMenu in self.menuPath:
                newPath = []
                for menu in self.menuPath:
                    if menu == newMenu:
                        break
                    else:
                        newPath.append(menu)
                self.menuPath = newPath
            else:self.menuPath.append(self.menu)
            self.menu = newMenu


    def disconnection(self):
        client.sendAndRecp({'disconnection': None})
        self.inGame = False
        self.changeMenu('welcom')

    def mainLoop(self):
        while True:
            if 'welcom' in self.menuPath or 'welcom' in self.menu:self.inGame = False
            else: self.inGame = True
            for menu in self.menuList:
                if menu.name == self.menu:
                    pygame.mouse.set_visible(1)
                    break
            self.toSend = {}
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.menu == 'pause':
                            self.changeMenu('')
                        elif self.menu == '':
                            self.changeMenu('pause')

                    if event.key == pygame.K_SPACE:
                        if self.menu == '':
                            if not self.character.do in ['cut', 'grab']:
                                self.character.do = 'cut'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu == '':
                        if not self.character.do in ['cut', 'grab']:
                            if pygame.mouse.get_pressed()[0]:
                                if self.character.mana >= 50:
                                    self.character.do = 'grab'
                                    self.character.createHarpon()
                            elif pygame.mouse.get_pressed()[2]:
                                self.character.do = 'cut'
                    elif self.menu == 'pause':
                        if pygame.mouse.get_pressed()[0]:
                            if menu.listBtn[0].click():
                                self.changeMenu('')
                            if menu.listBtn[1].click():
                                self.disconnection()
                    elif self.menu == 'welcom':
                        if pygame.mouse.get_pressed()[0]:
                            if menu.listBtn[0].click():
                                name = 'Owner'
                                self.character = player.Player(name)
                                result = client.sendAndRecp({'connection': [self.character.name]})
                                self.character.changeStat(result['character'])
                                self.updatePlayerList(result['playerList'])
                                for objStat in result['objs']:
                                    self.objs[objStat[2]].append(object.Object(objStat[0],objStat[1],objStat[2],objStat[3]))
                                self.changeMenu('')

            if not('welcom' in self.menuPath or 'welcom' in self.menu):
                self.gameLoop()
                self.blitSys()
            if self.inGame:
                self.character.returnStat()
                self.toSend['player'] = self.character.getMove()
                result = client.sendAndRecp(self.toSend)
                if type(result) == dict:
                    self.updatePlayerList(result['playerList'])
                    self.character.changeStat(result['character'])
                for p in self.playerList:
                    p.move(self.playerList)
            menu.blit(self.screen)

            t = pygame.time.get_ticks()
            # deltaTime in seconds.
            self.deltaTime = (t - self.getTicksLastFrame) / 1000.0
            self.getTicksLastFrame = t
            self.clock.tick(60)
            #print(self.clock.get_fps(), '   ', self.clock.tick(), '   ', self.deltaTime)
            pygame.display.update()
            self.screen.fill((40, 40, 40))

    def gameLoop(self):
        self.shift = [- self.character.pos[i] + self.screen.get_size()[i]//2 for i in range(len(self.screen.get_size()))]
        direction = 'imobile'
        if self.menu == '':
            pygame.mouse.set_visible(0)
            if not pygame.mouse.get_pos()[0] == self.MoussePosGame[0] and not self.character.do == 'cut' and not self.character.do == 'grab':
                self.character.changeAngle(
                    self.character.angle + (
                            self.MoussePosGame[0] - pygame.mouse.get_pos()[0]) * self.mousseSensitivity)
                self.character.changeAngle(
                    self.character.angle + (
                            self.MoussePosGame[1] - pygame.mouse.get_pos()[1]) * self.mousseSensitivity)
            pygame.mouse.set_pos(self.MoussePosGame)
            if self.character.health <=0 : self.disconnection()
            if not self.character.do == 'cut' and not self.character.do == 'grab':
                if pygame.key.get_pressed()[pygame.key.key_code('z')]:
                    direction = 'forward'
                    self.character.do = 'move'
                elif pygame.key.get_pressed()[pygame.key.key_code('q')]:
                    direction = 'left'
                    self.character.do = 'move'
                elif pygame.key.get_pressed()[pygame.key.key_code('s')]:
                    direction = 'backward'
                    self.character.do = 'move'
                elif pygame.key.get_pressed()[pygame.key.key_code('d')]:
                    direction = 'right'
                    self.character.do = 'move'
                else:
                    self.character.do = 'imobile'
        self.character.move(self.playerList, direction, self.deltaTime)

    def blitSys(self):
        for z in self.objs.keys():
            for obj in self.objs[z]:
                if z > 0:
                    self.blitEntity(obj.blit(pygame.rect.Rect(self.character.getRect()).colliderect([obj.pos, obj.size])))
                    self.blitBar(self.character.getRect(),self.character.mana/self.character.manaMax,(40,40,200), 10, 30)
                    self.blitBar(self.character.getRect(),self.character.health/self.character.healthMax,(40,200,40), 20)
                    #pygame.draw.rect(self.screen,(40,40,200),pygame.rect.Rect(self.character.getRect()[0]+self.shift[0], self.character.getRect()[1] + self.character.getRect()[3]+self.shift[1],  self.character.getRect()[2], 50))
            if z == 0:
                for player in self.playerList:
                    self.blitEntity((player.blit()))
                    pygame.draw.rect(self.screen,(40,40,200), pygame.rect.Rect(player.getRect()[0], player.getRect()[1] + player.getRect()[3],  player.getRect()[2], 50))
                self.blitEntity(self.character.blit())


    def blitBar(self, playerRect, valuePercent, colorVal, height, shiftV = 0):
        colorBack = []
        for id in range(len((colorVal))):
            if colorVal[id] > 100:color = colorVal[id] - 100
            else: color = 0
            colorBack.append(color)
        pygame.draw.rect(self.screen, colorBack, pygame.rect.Rect(playerRect[0] + self.shift[0],
                                                                      playerRect[1] +
                                                                      playerRect[3] + self.shift[1] + shiftV,
                                                                      playerRect[2], height))
        pygame.draw.rect(self.screen, colorVal, pygame.rect.Rect(playerRect[0] + self.shift[0],
                                                                      playerRect[1] +
                                                                      playerRect[3] + self.shift[1] + shiftV,
                                                                      playerRect[2]*valuePercent, height))

    def blitEntity(self, entity):
        for image in entity.keys():
            self.screen.blit(image, [entity[image][0] + self.shift[0], entity[image][1] + self.shift[1]])
