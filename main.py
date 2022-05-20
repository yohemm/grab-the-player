import pygame.event
import basic
import player
import pygame
import random
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
                    basic.Text('Bienvenue dans GrabThePlayer', 'src/font/SigmarOne.ttf', 32, pos=[screenSize[0]//2 - 200, 10] ),
                    basic.Text('préparer vous au combat Jeune Guerrier.\npartez a l\'aventure!', 'src/font/SigmarOne.ttf', 24, pos=[screenSize[0]//2 - 250, screenSize[1]//2])
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
        name = 'Owner'
        pos =[400,400]
        self.character = player.Player(name,  pos= pos)
        result = client.sendAndRecp({'connection' : [self.character.name]})
        self.character.changeStat(result['character'])
        self.playerList = []
        self.updatePlayerList(result['playerList'])
        self.MoussePosGame = [self.screen.get_size()[0]//2, self.screen.get_size()[1]//2]
        pygame.mouse.set_pos(self.MoussePosGame)
        self.mousseSensitivity = 0.5
        self.menu = ''
        self.inGame = True
        self.toSend = {}

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
                                self.character.do = 'grab'
                                self.character.createHarpon()
                            elif pygame.mouse.get_pressed()[2]:
                                self.character.do = 'cut'
                    elif self.menu == 'pause':
                        if pygame.mouse.get_pressed()[0]:
                            if menu.listBtn[0].click():
                                self.changeMenu('')
                            if menu.listBtn[1].click():
                                self.changeMenu('welcom')
                    elif self.menu == 'welcom':
                        if pygame.mouse.get_pressed()[0]:
                            if menu.listBtn[0].click():
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

            self.clock.tick(60)
            pygame.display.update()
            self.screen.fill((40, 40, 40))

    def gameLoop(self):
        direction = 'imobile'
        if self.menu == '':
            pygame.mouse.set_visible(0)
            if not pygame.mouse.get_pos()[0] == self.MoussePosGame[0] and not self.character.do == 'cut':
                self.character.changeAngle(
                    self.character.angle + (
                            self.MoussePosGame[0] - pygame.mouse.get_pos()[0]) * self.mousseSensitivity)
            pygame.mouse.set_pos(self.MoussePosGame)
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
        self.character.move(self.playerList, direction)

    def blitSys(self):
        for player in self.playerList:
            player.blit(self.screen)
        pygame.draw.rect(self.screen, (255,255,255), self.character.getRect())
        self.character.blit(self.screen)
