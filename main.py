import pygame.event
import basic
import player
import pygame
import random
import client

class Main:
    def __init__(self, screenSize):
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
                    #Btn
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
        ip = client.sendAndRecp({'connection' : None})
        self.character = player.Player(ip, pos= [400,400])
        self.playerList = [self.character]
        self.MoussePosGame = [self.screen.get_size()[0]//2, self.screen.get_size()[1]//2]
        pygame.mouse.set_pos(self.MoussePosGame)
        self.mousseSensitivity = 0.5
        self.menu = 'pause'
        self.inGame = True
        self.toSend = {}


    def mainLoop(self):
        while True:
            if not self.playerList[0].harpon == None:
                print(self.playerList[0].harpon.moveForward)
            self.toSend = {}
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.menu == 'pause':
                            self.menu = ''
                        elif self.menu == '':
                            self.menu = 'pause'

                    if event.key == pygame.K_SPACE:
                        if self.menu == '':
                            if not self.character.do in ['cut', 'grab']:
                                self.character.do = 'cut'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mouse.get_pressed()[0]
                    if self.menu == '':
                        if not self.character.do in ['cut', 'grab']:
                            if pygame.mouse.get_pressed()[0]:
                                self.character.do = 'grab'
                                self.character.createHarpon()
                            elif pygame.mouse.get_pressed()[2]:
                                self.character.do = 'cut'

            self.blitSys()
            inMenu = False
            for menu in self.menuList:
                if menu.name == self.menu:
                    inMenu = True
                    menu.blit(self.screen)
                    pygame.mouse.set_visible(True)
            if not inMenu:
                self.gameLoop()
            if self.inGame:
                self.character.returnStat()
                self.toSend['player'] = self.character.returnStat()
                result = client.sendAndRecp(self.toSend)
                if type(result) == dict:
                    self.playerList = []
                    for ip, playerstat in result.items():
                        ennemi = player.Player(ip)
                        ennemi.changeStat(playerstat['player'])
                        self.playerList.append(ennemi)
                if self.character.do == 'grab':
                    print(result)

            self.clock.tick(60)
            pygame.display.update()
            self.screen.fill((40, 40, 40))

    def gameLoop(self):
        for playerInGame in self.playerList:
            if playerInGame.health <= 0:
                self.playerList.remove(playerInGame)

        pygame.mouse.set_visible(0)
        direction = 'imobile'
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
                self.do = 'imobile'
        self.character.move(self.playerList, direction)
        if not pygame.mouse.get_pos()[0] == self.MoussePosGame[0] and not self.character.do == 'cut':
            self.character.changeAngle(
                self.character.angle + (self.MoussePosGame[0] - pygame.mouse.get_pos()[0]) * self.mousseSensitivity)
            pygame.mouse.set_pos(self.MoussePosGame)
        pygame.mouse.set_pos(self.MoussePosGame)

    def blitSys(self):
        for player in self.playerList:
            player.blit(self.screen)

