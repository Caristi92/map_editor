import pygame
from glob import glob
import sys
from pygame.locals import *
import os
import pickle


pygame.init()
W, H = w, h = WSIZE = ((928, 512))
screen = pygame.display.set_mode((w, h))
display = pygame.Surface((w // 2, h // 2))

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Sprite, self).__init__()
        self.x = x
        self.y = y
        self.dogwalking = glob("dog/Walk*.png")
        self.dogidling = glob("dog/Idle*.png")
        self.load_images()

    def load(self, x):
        return pygame.image.load(x).convert_alpha()

    def flip(self, x):
        return pygame.transform.flip(self.load(x), 1, 0)

    def load_images(self):
        self.list = [self.load(f) for f in self.dogwalking]
        self.listflip = [self.flip(f) for f in self.dogwalking]
        self.list_idle = [self.load(f) for f in self.dogidling]
        self.list_idleflip = [self.flip(f) for f in self.dogidling]
        self.counter = 0
        self.image = self.list[0]
        self.rect = self.image.get_rect()
        self.dir = ""
        self.prov = ""
        g.add(self)

    def update_counter(self, vel, img_list):
        self.counter += vel
        if self.counter >= len(img_list):
            self.counter = 0
        self.image = img_list[int(self.counter)]

    def update(self):
        if moveRight:
            self.update_counter(.1, self.list)
            self.prov = self.dir

        if moveLeft:
            self.update_counter(.1, self.listflip)
            # self.image = self.listflip[int(self.counter)]
            self.prov = self.dir

        if self.dir == "":
            self.update_counter(.1, self.list_idle)

            if moveRight:
                self.image = self.list_idle[int(self.counter)]

            else:
                self.image = self.list_idleflip[int(self.counter)]


g = pygame.sprite.Group()
player = Sprite(100, 100)
clock = pygame.time.Clock()

moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 1

def load_images(folder: str) -> list:
    "Load tiles from a folder... with a number at the end"
    listtiles2 = [x for x in glob(folder + "2\\*.png")]
    tile2 = [pygame.image.load(x) for x in listtiles2]
    return tile2


def load_map(filename: str, mp1: list):
    "Resume a list with the data (letter) for the tiles to be displayed on display surface"
    if filename in os.listdir():
        with open(filename, "rb") as file:
            mp = pickle.load(file)
    else:
        mp = mp1
    return mp


def showmap(mp1):
    "Take the map list with letters and blit them as tiles on the display surface"
    for y, line in enumerate(mp1):
        for x, c in enumerate(line):
            for n, l in enumerate(letters):
                if c == l:
                    display.blit(tile[n], (x * 16, y * 16))


# calls the function to load tiles from imgs2/
tile = load_images("imgs")
# create a list of all letters corrisponding to the tiles with images from imgs2 folder
alphab = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm.,:;@#°^[]<>()&%$£€ABC1234567890òàèéù+-ì={}§!?/|"
letters = [x for x in alphab[0:len(tile)]]
map2 = []
# Stores a list with letters = tiles from pkl file (created with pygame map editor)
map2 = load_map("last_map2.pkl", map2)
# bg = pygame.Surface((W, H))



while True:
# Check for events.
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # Change the keyboard variables.
            if event.key == K_s:
                pygame.image.save(screen, "screenshot.png")
            if event.key == K_LEFT or event.key == K_a:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
                # player.image = player.list[int(player.counter)]
            if event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True

        # KEYUP

        if event.type == KEYUP:
            player.counter = 0
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False

# Draw the white background onto the surface.
    # screen.fill((255, 255, 255))

    # Move the player.
    if moveDown and player.rect.bottom < h:
        player.rect.top += MOVESPEED
    if moveUp and player.rect.top > 0:
        player.rect.top -= MOVESPEED
    if moveLeft and player.rect.left > -35:
        player.rect.left -= MOVESPEED
        try:
            player.counter += .1
            player.image = pygame.transform.flip(player.list[int(player.counter)], True, False)
        except:
            player.counter = 0
            player.image = pygame.transform.flip(player.list[int(player.counter)], True, False)
    if moveRight and player.rect.right < w + 35:
        player.rect.right += MOVESPEED
        try:
            player.counter -= .1
            player.image = player.list[int(player.counter)]
        except:
            player.counter = 0
            player.image = player.list[int(player.counter)]

    # Draw the player onto the surface.
    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(display, (w, h)), (0, 0))
    showmap(map2)
    g.draw(screen)

    g.update()
    # Draw the window onto the screen.
    pygame.display.update()
    clock.tick(120)

pygame.quit()