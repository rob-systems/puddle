import pygame, sys
from pygame.locals import *
import random

pygame.init()
FPS = 30
FramePerSec = pygame.time.Clock()
screen_width = 800
screen_height = 800
DS = pygame.display.set_mode((screen_width,screen_height))
DS.fill((0,0,0))
pygame.display.set_caption("Game")

chars = [0,1,2,3,4,5,6,7,8,9]

#def char_creator(char):
#    if char == 0:
#        return 

class Cell():
    def __init__(self, data):
        self.value = data["val"]
        self.x = data["x"]
        self.y = data["y"]
        self.width = data["width"]
        self.height = data["height"]
        self.iter = data["iter"]
        #print(self.x, self.y)
        a = "{0:b}".format(self.value)
        self.binary_array = [c for c in a]
        self.surf = pygame.Surface((self.width,self.height))
        self.is_target = False
        self.was_target = False
        
    def fill(self):
        for x, item in enumerate(self.binary_array):
            if item == '1':
                a = pygame.Surface((5, 20))
                a.fill((255,255,255))
                self.surf.blit(a, (x * 10,0))
            else:
                a = pygame.Surface((5,20))
                a.fill((0,0,0))
                self.surf.blit(a, (x * 10, 0))

    def draw_char(self, value):
        if value == 0:
            pygame.draw.rect(self.surf, (0,0,0), (5, 5, 5, 5))
        elif value == 1:
            #print(self.x * 20, self.y * 5)
            pygame.draw.rect(self.surf,
                             (200 if self.is_target or self.value == 9 else 0,255,200 if self.is_target else 0),
                             pygame.Rect(0, 0, self.width, self.value * 5))
            self.draw_cover_rect()

    def draw_cover_rect(self):
        pygame.draw.rect(self.surf,
                         (0,0,0),
                         (0,self.value * 5,20,45 - self.value * 5))

    def max_out(self):
        self.value = 9

    def update(self, mouse_pos):
        if self.value > 1:
            self.value -= 1
        self.was_target = self.is_target
        self.is_target = (mouse_pos[0] > self.x * self.width and
                          mouse_pos[0] < self.x * self.width + self.width and
                          mouse_pos[1] > self.y * self.height and
                          mouse_pos[1] < self.y * self.height + self.height)
        if self.was_target and not self.is_target:
            print("poop")

class Grid():
    def __init__(self):
        self.grid = []
        self.cell_width = 20
        self.cell_height = 45

    def form(self):
        for y in range(round(screen_height / self.cell_height)):
            #print(y)
            for x in range(round(screen_width / self.cell_width)):
                #print(x)
                new_cell = Cell({
                    "val": 1,
                    "x": x,
                    "y": y,
                    "width": self.cell_width,
                    "height": self.cell_height,
                    "iter": x + y * round(screen_height / self.cell_height) + 1
                    })
                self.grid.append(new_cell)

    def drawish(self):
        for i, item in enumerate(self.grid):
            item.draw_char(1)
            #print((i // screen_height/cell_height) * 40, (i // screen_height/cell_height) * 5)
            #5print((item.x * self.cell_width, item.y * self.cell_height))
            
            DS.blit(item.surf, (item.x * self.cell_width , item.y * self.cell_height))

    def update(self, mp):
        for i,x in enumerate(self.grid):
            #print(i)
            if x.value == 9:
                #ripple
                #x.y * 
                #print(x.x + 1,)
                #print("gay")
                self.grid[x.iter - 1].value = 9
                self.grid[x.iter + 1].value = 9
                #if not i < screen_width / self.cell_width:
                    #self.grid[i - round(screen_width / self.cell_width)].value = 9
            x.update(mp)

    def on_click(self):
        for x in self.grid:
            if x.is_target:
                x.max_out()

meGrid = Grid()

meGrid.form()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            meGrid.on_click()

    mouse_pos = pygame.mouse.get_pos()
    meGrid.update(mouse_pos)
    meGrid.drawish()
    pygame.display.update()
    FramePerSec.tick(FPS)
