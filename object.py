import pygame.image

class Object:
    def __init__(self, src ,pos:list=[0,0], z:int=0, size=0, typ:str=''):
        self.src = src
        if not size == 0:
            if type(size) == int:
                self.size = [size,size]
            else:
                self.size = size
        print(self.size)
        self.image = pygame.transform.scale(pygame.image.load(src), self.size)
        self.pos = pos
        self.z = z
        self.type = typ

    def blit(self, playerUnder = False):
        image = self.image.copy()
        if playerUnder:
            image.set_alpha(128)
        return {image: self.pos}

    def returnStat(self):
        return self.src, self.pos, self.z, self.size, self.type



