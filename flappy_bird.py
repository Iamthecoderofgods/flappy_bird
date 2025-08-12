import pygame
import os
from pygame.locals import *
pygame.init()

WIDTH = 800
HEIGHT = 850

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.update()
ground_scroll = -100
scroll_speed = 0.25

Backround = pygame.image.load("images/flappy_backround.png")
ground = pygame.image.load("images/flapply_ground.png")
pipes = pygame.image.load("images/Flappy_pipe.png")
#flappy2 = pygame.image.load("image/Flappy_bird1.png")
Backround_image1 = pygame.transform.scale(Backround,(900,850))

class Bird(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.flappy_images = []
        self.index = 0
        for e in range(1,4):
            Flappy_bird = pygame.image.load(f"images/Flappy_bird_{e}.png")
            self.flappy_images.append(Flappy_bird)
        self.image = self.flappy_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.clicked = False
        self.velocity = 0
        print("doing creation")
Birdgroup = pygame.sprite.Group()
flappy = Bird(400,400)

Birdgroup.add(flappy)
Running = True

while Running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            Running = False
    screen.blit(Backround_image1,(0,0))
    screen.blit(ground,(ground_scroll,800))
    Birdgroup.draw(screen)
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 50:
        ground_scroll = 0
    pygame.display.update()

    