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

    
    def shoot(self):
        # Verifica se pode atirar
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde o último tiro.
        elapsed_ticks = now - self.last_shot

        # Se já pode atirar novamente...
        if elapsed_ticks > self.shoot_ticks:
            # Marca o tick da nova imagem.
            self.last_shot = now
            # A nova bala vai ser criada logo acima e no centro horizontal da nave
            new_bullet = Bullet(self.assets, self.rect.top, self.rect.centerx)
            self.groups['all_sprites'].add(new_bullet)
            self.groups['all_bullets'].add(new_bullet)
            self.assets['pew_sound'].play()

    
class Meteor(pygame.sprite.Sprite):
    def _init_(self, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite._init_(self)

        self.image = assets['barquinho']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura-largura_barquinho)
        self.rect.y = random.randint(-100, -altura_barquinho)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 9)

    def update(self):
        # Atualizando a posição do meteoro
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se o meteoro passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > largura:
            self.rect.x = random.randint(0, largura-largura_barquinho)
            self.rect.y = random.randint(-100, -altura_barquinho)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 9)