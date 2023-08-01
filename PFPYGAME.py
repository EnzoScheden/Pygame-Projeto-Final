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
assets['barquinho'] = pygame.image.load('img/pngwing.com.png').convert_alpha()
assets['barquinho'] = pygame.transform.scale(assets['barquinho'], (largura_barquinhos, altura_barquinhos))
assets['navio'] = pygame.image.load('img/navio-de-guerra.png').convert_alpha()
assets['navio'] = pygame.transform.scale(assets['navio'], (navio_largura, navio_altura))
assets['bala'] = pygame.image.load('img/laserRed16.png').convert_alpha()
explosion_anim = []
for i in range(9):
    # Os arquivos de animação são numerados de 00 a 08
    filename = 'assets/img/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img = pygame.transform.scale(img, (32, 32))
    explosion_anim.append(img)
assets["explosion_anim"] = explosion_anim
assets["score_font"] = pygame.font.Font('assets/font/PressStart2P.ttf', 28)

class barco(pygame.sprite.Sprite):

    def init(self, groups, assets):
        pygame.sprite.Sprite.init(self)

        self.image = assets['navio']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect() 
        self.rect.centerx = largura / 2 
        self.rect.bottom  = altura  - 10 
        self.speedx = 0
        self.groups = groups 
        self.assent = assets  

    def update(self):
    #atualiza posição
        self.rect.x += self.speedx 

    #fica na tela pff
        if self.rect.right > largura:
            self.rect.right = largura 

        if self.rect.left < 0:
            self.rect.left = 0