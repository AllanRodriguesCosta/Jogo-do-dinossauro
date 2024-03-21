import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

main_directory = os.path.dirname(__file__)
images_directory = os.path.join(main_directory, 'images')
songs_directory = os.path.join(main_directory, 'songs')


WIDTH = 640
HEIGHT = 480

BRANCO = (255, 255, 255)
PRETO = (0,0,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

screen.fill(BRANCO)

sprite_sheet = pygame.image.load(os.path.join(images_directory, 'spritesheet.png')).convert_alpha()

collision_song = pygame.mixer.Sound(os.path.join(songs_directory, 'death_sound.wav'))
collision_song.set_volume(0.2)

score_song = pygame.mixer.Sound(os.path.join(songs_directory, 'score_sound.wav'))
score_song.set_volume(0.2)

impact = False

obstacle_choice = choice([0, 1])

points = 0

game_speed = 10

def Points_exibition(msg, size, color):
    font = pygame.font.SysFont('comicsansms', size, True, False)
    message = f'{msg}'
    formatted_text = font.render(message, True, color)
    return formatted_text

def reset_game():
    global points, game_speed, impact, obstacle_choice
    points = 0
    game_speed = 10
    impact = False
    dino.rect.y = HEIGHT - 61 - 96//2
    dino.jump = False
    flying_dino.rect.x = WIDTH
    cactus.rect.x = WIDTH
    obstacle_choice = choice([0, 1])

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.jump_song = pygame.mixer.Sound(os.path.join(songs_directory, 'jump_sound.wav'))
        self.jump_song.set_volume(0.2)
        self.dino_images = []
        for i in range(3):
            img = sprite_sheet.subsurface((i*32, 0), (32,32))
            self.dino_images.append(img)
            self.image = self.dino_images[0]
            self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        
        self.index_list = 0
        self.image = self.dino_images[self.index_list]
        self.rect = self.image.get_rect()
        self.maks = pygame.mask.from_surface(self.image)
        self.pos_y_initial = HEIGHT - 61 - 96//2
        self.rect.center = (100,HEIGHT - 61)
        self.jump = False

    def jumping(self):
        self.jump = True
        self.jump_song.play()

        
    def update(self):
        if self.jump == True:
            if self.rect.y <=300:
                self.jump = False
            self.rect.y -= 10
        else:
            if self.rect.y < self.pos_y_initial:
                self.rect.y += 10
            else:
                self.rect.y = self.pos_y_initial
        if self.index_list > 2:
            self.index_list = 0
        self.index_list += 0.25
        self.image = self.dino_images[int(self.index_list)]
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = WIDTH - randrange(30, 300, 90)
    
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.y = randrange(50, 200, 50)
            self.rect.x = WIDTH 
        self.rect.x -= game_speed

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - 64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = WIDTH 
        self.rect.x -= 10

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*2.5, 32*2.5))
        self.rect = self.image.get_rect()
        self.maks = pygame.mask.from_surface(self.image)
        self.choice = obstacle_choice
        self.rect.center = (WIDTH, HEIGHT - 54)
        self.rect.x = WIDTH
    
    def update(self):
        if self.choice == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = WIDTH 
            self.rect.x -= game_speed

class Flying_dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dino_images = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i*32, 0), (32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.dino_images.append(img)

        self.index_lista = 0
        self.image = self.dino_images[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.choice = obstacle_choice
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, 300)
        self.rect.x = WIDTH

    def update(self):
        if self.choice == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = WIDTH 
            self.rect.x -= game_speed

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.dino_images[int(self.index_lista)]


all_sprites = pygame.sprite.Group()
dino = Dino()
all_sprites.add(dino)   

for i in range(4):
    cloud = Cloud()
    all_sprites.add(cloud)

    

for i in range(WIDTH//64+4):   
    floor = Floor(i) 
    all_sprites.add(floor)


cactus = Cactus()
all_sprites.add(cactus)

flying_dino = Flying_dino()
all_sprites.add(flying_dino)

impact = False

  

obstacles_group = pygame.sprite.Group()
obstacles_group.add(cactus)
obstacles_group.add(flying_dino)



clock = pygame.time.Clock()

pygame.display.set_caption("Jogo do dinossauro")



while True:
    clock.tick(30)
    screen.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()  

        if event.type == KEYDOWN:
            if event.key == K_SPACE and impact == False:
                if dino.rect.y != dino.pos_y_initial:
                    pass
                else: 
                    dino.jumping()
            if event.key == K_r and impact == True:
                reset_game()

    collisions = pygame.sprite.spritecollide(dino, obstacles_group, False, pygame.sprite.collide_mask)

    all_sprites.draw(screen)

    if cactus.rect.topright[0] <= 0 or flying_dino.rect.topright[0] <= 0:
        obstacle_choice = choice([0, 1])
        cactus.rect.x = WIDTH
        flying_dino.rect.x = WIDTH
        cactus.choice = obstacle_choice
        flying_dino.choice = obstacle_choice

    if collisions and impact == False:
        collision_song.play()
        impact = True

    if impact == True:
        if points % 100 == 0:
            points += 1
        game_over = Points_exibition('GAME OVER', 40 , (PRETO))
        screen.blit(game_over, (WIDTH//2, HEIGHT//2))
        restart_game = Points_exibition('Pressione "R" para reiniciar', 20, (PRETO))
        screen.blit(restart_game, (WIDTH//2-10, HEIGHT//3+150))

    else:
        points += 1
        all_sprites.update()
        points_text = Points_exibition(points, 40, (PRETO))

    if points % 100 == 0:
        score_song.play()
        if game_speed >= 23:
            game_speed += 0
        else:
            game_speed += 1

    screen.blit(points_text, (520, 30))

    pygame.display.flip()