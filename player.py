import pygame
import math
import basic
import clientUDP

class Player:
    def __init__(self,name='Player1', pos = [0,0], velocityMax = 5):
        self.doDict = {
            'imobile' : 0,
            'move' : 1,
            'grab' : 2,
            'cut' : 3,
            'dash' : 4
        }
        self.imageOrigin = pygame.transform.scale(pygame.image.load('src/player.png'), [100,100])
        self.image = self.imageOrigin
        self.name = name
        self.pos = pos
        self.angle = 0
        self.velocity = 0
        self.direction = 'forward'
        self.healthMax = 100
        self.health = self.healthMax
        self.touchInCut = []
        self.velocityMax = velocityMax
        self.do = 'imobile'
        self.manaMax = 100
        self.mana = self.manaMax
        self.manaTimer = 0
        self.harpon = None
        self.cutImg = None
        self.cutAnime = basic.Animation(7, 50,'src/cut/sprite_', '.png')

    def returnStat(self):
        stats = [self.name, self.pos, self.angle, self.velocity, self.direction, self.healthMax, self.health, self.mana ]
        return stats

    def changeAngle(self, angle):
        self.angle = angle%360

    def blit(self, screen):
        self.image = pygame.transform.rotate(self.imageOrigin,self.angle)
        screen.blit(self.image, [self.pos[0] - int(self.image.get_size()[0]/2), self.pos[1] - int(self.image.get_size()[1]/2)])
        if self.do == 'cut':
            self.cutImg = self.blitObjForward(screen,pygame.image.load(self.cutAnime.dossier + str(self.cutAnime.idImg) + self.cutAnime.sufix))
        else: self.cutImg = None
        if type(self.harpon) == Harpon:
            self.harpon.blit(screen)

        #HEALTH BAR
        pygame.draw.rect(screen, (120, 50, 50), pygame.rect.Rect([self.pos[0] - 50, self.pos[1] + 50], [100, 10]))
        pygame.draw.rect(screen, (50, 120, 50), pygame.rect.Rect([self.pos[0] - 50, self.pos[1] + 50],
                                                                     [100 * self.health / self.healthMax, 10]))

        #MANA BAR
        pygame.draw.rect(screen,(30, 30, 80) , pygame.rect.Rect([self.pos[0] - 50, self.pos[1] + 60], [100, 5]))
        pygame.draw.rect(screen,(100, 100, 150) , pygame.rect.Rect([self.pos[0] - 50, self.pos[1] + 60], [100*self.mana/self.manaMax, 5]))

    def harponSys(self, allPlayer):
        self.harpon.move(allPlayer)
        if type(self.harpon) == Harpon and self.harpon.verifyEnd():
            self.harpon = None

    def blitObjForward(self, screen, image):
        rect2 = [self.pos[0] - math.cos(math.radians((self.angle + 270) % 360)) * 50,
                 self.pos[1] + math.sin(math.radians((self.angle + 270) % 360)) * 50]
        newImg = pygame.transform.rotozoom(
            pygame.transform.scale(image, [100, image.get_height() * 100 / image.get_width()]), self.angle, 1)
        newImg.set_colorkey((0, 0, 0))
        screen.blit(newImg, [rect2[0] - newImg.get_size()[0] // 2, rect2[1] - newImg.get_size()[1] // 2])
        return newImg

    def createHarpon(self):
        if not type(self.harpon) == Harpon:
            if  self.changeMana(-50):self.harpon = Harpon(self, 300)


    def move(self, allPlayer:list,  direction: str = 'imobile'):
        dictDir = {
            'forward' : 270,
            'left' : 0,
            'backward' : 90,
            'right' : 180
        }
        if direction == 'imobile' and not self.do in ['cut', 'grab']:self.do = 'imobile'
        if self.do == 'move':
            if direction in dictDir :self.direction = direction
            if self.velocity == 0:
                self.velocity = 1
            if self.velocity > self.velocityMax:
                self.velocity = self.velocityMax
            elif self.velocity < self.velocityMax:
                self.velocity = self.velocity *1.05
        else:
            if self.velocity >=1:
                self.velocity = self.velocity / 1.05
            else: self.velocity = 0
        if self.do == 'cut':
            if self.cutAnime.disable:
                if not self.changeMana(-25): self.do = 'imobile'
            for ennemi in allPlayer:
                if pygame.rect.Rect([self.pos[0] - math.cos(math.radians((self.angle + 270) % 360)) * 50,
                 self.pos[1] + math.sin(math.radians((self.angle + 270) % 360)) * 50], self.cutImg.get_size()).colliderect(pygame.rect.Rect(ennemi.pos, ennemi.image.get_size())) and not ennemi == self and not ennemi in self.touchInCut:
                    self.touchInCut.append(ennemi)
                    ennemi.health -= 50

            if not self.cutAnime.changeImage():
                self.do = 'imobile'
                self.touchInCut = []
        elif self.do == 'grab':
            if self.harpon == None:
                self.do = 'imobile'
            else:
                self.harponSys(allPlayer)


        if self.velocity > 0 :
            self.pos = [self.pos[0] - math.cos(math.radians((self.angle + dictDir[self.direction]) % 360)) * self.velocity,
                        self.pos[1] + math.sin(math.radians((self.angle + dictDir[self.direction]) % 360)) * self.velocity]
        else:
            if self.do == 'imobile':
                if pygame.time.get_ticks() > self.manaTimer:
                    self.changeMana(1)
            elif self.mana < self.manaMax:
                self.manaTimer = pygame.time.get_ticks() + 2000

    def changeMana(self, mondifier):
        if self.mana < 0 : self.mana = 0
        elif self.mana > self.manaMax : self.mana = self.manaMax
        if 0 <= self.mana + mondifier <= self.manaMax:
            self.mana += mondifier
            return True
        else: return False

class Harpon:
    def __init__(self, player, distance):
        self.moveForward = True
        self.player = player
        self.angle = player.angle
        self.endPos = [player.pos[0] - math.cos(math.radians((self.angle + 270) % 360)) * 50,
                 player.pos[1] + math.sin(math.radians((self.angle + 270) % 360)) * 50]
        self.pos = self.endPos
        self.midlePos = [self.pos[0] - math.cos(math.radians((self.angle + 270) % 360)) * distance,
                 self.pos[1] + math.sin(math.radians((self.angle + 270) % 360)) * distance]
        self.chainList = []
        self.grabOrigin = pygame.transform.scale(pygame.image.load('src/harpon.png'), [50,50])
        self.grab = pygame.transform.scale(pygame.image.load('src/harpon.png'), [50,50])
        self.chain = pygame.transform.scale(pygame.image.load('src/harponHarms.png'), [50,50])
        self.distance = distance
        self.velocityMax = 8
        self.velocityMin = 5
        self.velocity = self.velocityMin
        self.target = None

    def move(self, allplayer):
        k = 1.1
        if self.moveForward:
            if self.velocity < self.velocityMax : self.velocity *= k
            elif self.velocity > self.velocityMax : self.velocity = self.velocityMax
            self.pos =[self.pos[0] - math.cos(math.radians((self.angle + 270) % 360)) * self.velocity,
                     self.pos[1] + math.sin(math.radians((self.angle + 270) % 360)) * self.velocity]
            if -5 < self.pos[0] - self.midlePos[0] < 5 and  -5 < self.pos[1] - self.midlePos[1] < 5:
                self.moveForward = False
        else:
            if self.velocityMin < self.velocity : self.velocity /= k
            elif self.velocityMin > self.velocity and self.moveForward: self.velocity = self.velocityMin
            self.pos =[self.pos[0] - math.cos(math.radians((self.angle + 90) % 360)) * self.velocity,
                     self.pos[1] + math.sin(math.radians((self.angle + 90) % 360)) * self.velocity]
            if not self.target == None:
                self.target.do = 'imobile'
                self.target.pos =[self.target.pos[0] - math.cos(math.radians((self.angle + 90) % 360)) * (self.velocity + 1),
                     self.target.pos[1] + math.sin(math.radians((self.angle + 90) % 360)) * (self.velocity + 1)]
        self.toucheEnnemi(allplayer)

    def toucheEnnemi(self, allPlayer):
        for player in allPlayer:
            if pygame.rect.Rect(self.pos, self.grab.get_size()).colliderect(pygame.rect.Rect(player.pos, player.image.get_size())) and not player ==  self.player:
                self.target = player
                self.moveForward = False


    def verifyEnd(self):
        if not self.moveForward and -5 < self.pos[0] - self.endPos[0] < 5 and  -5 < self.pos[1] - self.endPos[1] < 5:return True
        else:return False


    def blit(self, screen):
        self.grab = pygame.transform.rotate(self.grabOrigin, self.angle)
        screen.blit(self.grab, [self.pos[0] - self.grab.get_size()[0]//2, self.pos[1] - self.grab.get_size()[1]//2])


