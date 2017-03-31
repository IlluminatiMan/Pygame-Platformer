import pygame, time

def sign(num):
    if num == 0: return 0
    return abs(num)/num

class Player(object):
    def __init__(self, pos):
        self.img = pygame.image.load('mario.jpg')
        self.setPos(pos)
        self.xvel = 0
        self.yvel = 0
        self.onground = False
        self.up = -1
        self.jumping = True
        #-1 is can jump
        #0 is holding

    

    def getPos(self):
        return (self.rect.x, self.rect.y)

    def setPos(self, pos):
        x, y = pos
        self.rect = pygame.Rect(x, y, 20, 20)

        
    def draw(self, surf, camera):
        rect = camera.shiftRect(self.rect)
        if rect.colliderect(surf.get_rect()):
            img = pygame.transform.scale(self.img, (self.rect.w, self.rect.h))
            surf.blit(img, rect.topleft)


    def move(self, blocks):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.up == -1:
                self.up == 0
                if self.onground:
                    self.yvel = 200
                    self.jumping = True

        if keys[pygame.K_RIGHT]:
            self.xvel += 5
        if keys[pygame.K_LEFT]:
            self.xvel -= 5

        #self.yvel -= 1

        x, y = self.getPos()
        x += self.xvel / 60
        y += self.yvel / 60
        self.xvel *= .6 ** (1/60)
        self.setPos((x, y))

    def tick(self, blocks):
        self.move(blocks)



class Camera():
    def __init__(self):
        self.pos = (0,0)
        self.zoom = 1

    def setData(self, pos, zoom):
        self.pos = pos
        self.zoom = zoom
    
    def shiftRect(self, rect):
        x, y = self.shiftPoint((rect.x, rect.y))
        w = rect.w * self.zoom
        h = rect.h * self.zoom
        return pygame.Rect(x, y, w, h)

    def shiftPoint(self, point):
        x = (point[0] - self.pos[0]) * self.zoom
        y = (point[1] - self.pos[1]) * self.zoom
        return (x, y)

class Block(object):
    size = 20
    def __init__(self, coord):
        self.coord = coord
        self.rect = pygame.Rect(self.coord[0] * self.size, self.coord[0] * self.size, self.size, self.size)


    def draw(self, surf, camera):
        newRect = camera.shiftRect(self.rect)
        pygame.draw.rect(surf, (0, 0, 0), newRect, 0)

class Level():
    def __init__(self, size):
        self.camera = Camera()
        self.run = True
        self.surf = pygame.Surface(size)
        self.blocks = [Block((0, 0))]
        self.player = Player((0, 20))

    def changeCam(self):
        x, y = self.player.getPos()
        newx = x - self.surf.get_width() / 2
        newy = y - self.surf.get_height() / 2
        self.camera.setData((newx, newy), 1)
    
    def tick(self):
        self.player.tick(self.blocks)
        self.changeCam()
        for block in self.blocks:
            self.surf.fill((255, 255, 255))
            block.draw(self.surf, self.camera)
            self.player.draw(self.surf, self.camera)
        self.player.draw(self.surf, self.camera)

class Client():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 750))
        self.level = Level((800, 600))
        self.run = True
        self.inlevel = True
        self.events = []
        self.clock = pygame.time.Clock()

    def gameloop(self):
        while self.run:
            self.tick()

    def tick(self):

        t = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                
        if self.inlevel:
            self.level.tick()
        
        self.screen.fill((255, 255, 255))

        if self.inlevel:
            self.screen.blit(self.level.surf, (0, 0))
        pygame.display.update()
        self.clock.tick(60)

        
        
def main():
    client = Client()
    client.gameloop()

main()
