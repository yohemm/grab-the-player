import pygame
pygame.init()
class Animation():
    def __init__(self, nbImg:int, cooldown:int, dossier:str, sufix:str):
        self.nbImg = nbImg
        self.dossier = dossier
        self.sufix = sufix
        self.idImg = 0
        self.disable = False
        self.timer = 0
        self.cooldown = cooldown

    def __repr__(self):
        return self.getStat()
    def getStat(self):
        return [self.nbImg, self.dossier, self.sufix, self.idImg, self.disable, self.timer, self.cooldown]

    def setStat(self, list):
        self.nbImg = list[0]
        self.dossier = list[1]
        self.sufix = list[2]
        self.idImg = list[3]
        self.disable = list[4]
        self.timer = list[5]
        self.cooldown = list[6]


    def changeImage(self):
        if self.disable:
            self.timer = pygame.time.get_ticks()
            self.disable = False
        elif self.timer + self.cooldown < pygame.time.get_ticks():
            self.idImg += 1
            self.timer = pygame.time.get_ticks()
            if self.idImg >= self.nbImg:
                self.idImg = 0
                self.disable = True
                return False
        return True
class Image():
    def __init__(self, src:str, pos:list = [0,0], size:list = [100,100]):
        self.change(src, pos, size)

    def change(self, src:str = None, pos:list=None, size:list=None):
        if not src == None: self.src = src
        if not pos == None: self.pos = pos
        if not size == None: self.size = size
        self.image = pygame.transform.scale(pygame.image.load(src), size)


    def blit(self, screen):
        screen.blit(self.image, self.pos)

class Text():
    def __init__(self, text:str, font:str, size:int, color:list = (0,0,0), pos:list = [0,0]):
        print(font, size, color)
        self.carSize = size
        self.font = pygame.font.Font(font, size)
        self.pos = pos
        self.refreshRenderers(text, color)

    def blit(self, screen):
        pos = self.pos
        for renderer in self.renderers:
            screen.blit(renderer, pos)
            pos = [pos[0], pos[1] + renderer.get_size()[1]]

    def refreshRenderers(self,text:str = None , color:list=None):
        if not text == None: self.text = text
        if not color == None: self.color = color
        self.renderers = []
        size = [0,0]
        for line in self.text.splitlines():
            self.renderers.append(self.font.render(line, True, self.color))
            if size[0] < self.renderers[-1].get_size()[0]:
                size = [self.renderers[-1].get_size()[0], size[1] + self.renderers[-1].get_size()[1]]
        self.size = size

class Button():
    def __init__(self, image:Image = None, text:Text = None, pos:list=[0,0], size:list=[100,100]):
        self.image = image
        self.text = text
        if not self.text == None:
            self.text.pos = [pos[0] + size[0]//2 - self.text.size[0]//2,pos[1] + size[1]//2 - self.text.size[1]//2]
        if not self.image == None:
            self.image.pos = [pos[0] + size[0]//2 - self.image.size[0]//2,pos[1] + size[1]//2 - self.image.size[1]//2]
        self.pos = pos
        self.size = size

    def blit(self, screen):
        if not self.image == None:
            self.image.blit(screen)
        if not self.text == None:
            self.text.blit(screen)

    def click(self):
        return self.pos[0] < pygame.mouse.get_pos()[0] < self.pos[0] + self.size[0] and self.pos[1] < pygame.mouse.get_pos()[1] < self.pos[1] + self.size[1]
class Menu():
    def __init__(self, name ,listBtn, listText, listImg):
        self.listBtn = listBtn
        self.listImg = listImg
        self.listText = listText
        self.name = name

    def blit(self, screen):
        for btn in self.listBtn:
            btn.blit(screen)
        for text in self.listText:
            text.blit(screen)
        for img in self.listImg:
            img.blit(screen)

