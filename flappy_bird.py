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
flying = False
game_over = False
pipegap = 150
pipe_frequency = 1500 
last_pipe = pygame.time.get_ticks()-pipe_frequency


Backround = pygame.image.load("images/flappy_backround.png")
ground = pygame.image.load("images/flapply_ground.png")
pipes = pygame.image.load("images/Flappy_pipe.png")
#flappy2 = pygame.image.load("image/Flappy_bird1.png")
Backround_image1 = pygame.transform.scale(Backround,(900,850))

class pipe(pygame.sprite.Sprite):
    def __init__(self, x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Flappy_pipe.png")
        self.Rect = self.image.get_rect()
        if position == 1:#top pipe
            self.image = pygame.transform.flip(self.image,False,True)
            self.Rect.bottomleft = [x,y-int(pipegap/2)]
        elif position == -1:
            self.Rect.topleft = [x,y+int(pipegap/2)]
            




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
        self.counter = 0
    def update(self):
        if flying == True:
            self.velocity += 0.5
            if self.velocity > 1:
                self.velocity = 1
        
            if self.rect.bottom < 850:
                self.rect.y += (int(self.velocity))
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity -=10
            if self.velocity > 5:
                self.velocity = 5
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            flap_cool_down = 5
            self.counter += 1
            if self.counter > flap_cool_down:
                self.counter = 0
                self.index +=1
                print(self.flappy_images)
                print(self.counter)
                if self.index >= len(self.flappy_images):
                    self.index = 0
                self.image = self.flappy_images[self.index]

            self.image = pygame.transform.rotate(self.flappy_images[self.index],self.velocity*-2)
        else:
            self.image = pygame.transform.rotate(self.flappy_images[self.index],-90)

Birdgroup = pygame.sprite.Group()
pipegroup = pygame.sprite.Group()
flappy = Bird(400,400)

Birdgroup.add(flappy)
Running = True

while Running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            Running = False
        if e.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    if flying == True and game_over == False:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            bottom_pipe = pipe()
    screen.blit(Backround_image1,(0,0))
    screen.blit(ground,(ground_scroll,800))
    Birdgroup.draw(screen)
    Birdgroup.update()
    pipegroup.draw(screen)
    pipegroup.update()
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 50:
        ground_scroll = 0
    pygame.display.update()

    