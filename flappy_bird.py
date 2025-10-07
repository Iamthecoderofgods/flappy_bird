import pygame
import os
from pygame.locals import *
import random
pygame.init()

WIDTH = 800
HEIGHT = 850

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.update()
pass_pipe = False
clock = pygame.time.Clock()
Fps = 60
ground_scroll = -100
scroll_speed = 5
flying = False
game_over = False
pipegap = 150
pipe_frequency = 1500 
last_pipe = pygame.time.get_ticks()-pipe_frequency
font = pygame.font.SysFont("Times New Roman",36)
score = 0

button_img = pygame.image.load("images/restart.png")
Backround = pygame.image.load("images/flappy_backround.png")
ground = pygame.image.load("images/flapply_ground.png")
pipes = pygame.image.load("images/Flappy_pipe.png")
#flappy2 = pygame.image.load("image/Flappy_bird1.png")
Backround_image1 = pygame.transform.scale(Backround,(900,850))

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Flappy_pipe.png")
        self.rect = self.image.get_rect()
        if position == 1:#top pipe
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y-int(pipegap/2)]
        elif position == -1:
            self.rect.topleft = [x,y+int(pipegap/2)]
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
        pygame.display.update()


    
        
            




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
      
        self.velocity += 1
        if self.velocity > 3:
            self.velocity = 3
        
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
class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.Rect = self.image.get_rect()
        self.Rect.topleft = (x,y)
    def Draw(self):
        action = False
        if self.Rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]==1:
                action = True
        screen.blit(self.image,(self.Rect.x,self.Rect.y))
        return action

def reset_game():
    Pipegroup.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(HEIGHT / 2)
    score = 0
    return score


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
        

Birdgroup = pygame.sprite.Group()
Pipegroup = pygame.sprite.Group()
flappy = Bird(400,400)

Birdgroup.add(flappy)
Running = True
button = Button(WIDTH // 2 - 50, HEIGHT // 2 - 100, button_img)

while Running:
    clock.tick(Fps)
    #draw background
    screen.blit(Backround_image1, (0,0))
    Pipegroup.draw(screen)
    Birdgroup.draw(screen)
    Birdgroup.update()
    #draw and scroll the ground
    screen.blit(ground, (ground_scroll, 768))
    pygame.display.update()
    #check the score
    if len(Pipegroup) > 0:
        if Birdgroup.sprites()[0].rect.left > Pipegroup.sprites()[0].rect.left\
            and Birdgroup.sprites()[0].rect.right < Pipegroup.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if Birdgroup.sprites()[0].rect.left > Pipegroup.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    draw_text(str(score), font, "white", int(WIDTH / 2), 20)

    #look for collision
    if pygame.sprite.groupcollide(Birdgroup, Pipegroup, False, False) or flappy.rect.top < 0:
        game_over = True
    #once the bird has hit the ground it's game over and no longer flying
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if flying == True and game_over == False:
        print(flying,game_over)
        
        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            print("yes")
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, 1)
            Pipegroup.add(btm_pipe)
            Pipegroup.add(top_pipe)
            last_pipe = time_now
        Pipegroup.update()
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
              #check for game over and reset
        pygame.display.update()
    if game_over == True:
        if button.Draw():
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if flying == False and game_over == False:
                flying = True
            elif game_over:
                if button.Rect.collidepoint(event.pos):
                    game_over == False
                    score = reset_game
                
        
        
    pygame.display.update()
pygame.quit()