import pygame 

import random 

largura = 600

altura = 480 

tamanho = pygame.display.set_mode((largura,altura))



largura_barquinhos = 50

altura_barquinhos = 38 

navio_largura = 50 

navio_altura = 38




assets = {}
assets['fundo'] = pygame.image.load('').convert()
assets['barquinho'] = pygame.image.load('assets/img/meteorBrown_med1.png').convert_alpha()
assets['barquinho'] = pygame.transform.scale(assets['meteor_img'], (METEOR_WIDTH, METEOR_HEIGHT))
assets['navio'] = pygame.image.load('assets/img/playerShip1_orange.png').convert_alpha()
assets['navio'] = pygame.transform.scale(assets['ship_img'], (SHIP_WIDTH, SHIP_HEIGHT))
assets['bala'] = pygame.image.load('assets/img/laserRed16.png').convert_alpha()
explosion_anim = []
for i in range(9):
    # Os arquivos de animação são numerados de 00 a 08
    filename = 'assets/img/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img = pygame.transform.scale(img, (32, 32))
    explosion_anim.append(img)
assets["explosion_anim"] = explosion_anim
assets["score_font"] = pygame.font.Font('assets/font/PressStart2P.ttf', 28)

