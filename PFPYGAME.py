import pygame 

import random 

pygame.init()


largura = 600

altura = 480 

tamanho = pygame.display.set_mode((largura,altura))




largura_barquinhos = 50

altura_barquinhos = 38 

navio_largura = 50 

navio_altura = 38




assets = {}
assets['fundo'] = pygame.image.load('img/mar-visto-a-partir-de-cima.jpg').convert()
assets['barquinho'] = pygame.image.load('img/pngwing.com.png').convert_alpha()
assets['barquinho'] = pygame.transform.scale(assets['barquinho'], (largura_barquinhos, altura_barquinhos))
assets['navio'] = pygame.image.load('img/navio-de-guerra.png').convert_alpha()
assets['navio'] = pygame.transform.scale(assets['navio'], (navio_largura, navio_altura))
assets['bala'] = pygame.image.load('img/laserRed16.png').convert_alpha()
explosion_anim = []
for i in range(9):
    filename = 'img/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img = pygame.transform.scale(img, (32, 32))
    explosion_anim.append(img)
assets["explosion_anim"] = explosion_anim
assets["score_font"] = pygame.font.Font('font/PressStart2P.ttf', 28)

class navio(pygame.sprite.Sprite):

    def __init__(self, groups, assets):
        pygame.sprite.Sprite.__init__(self)

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
        elapsed_ticks = now - self.last_shot

        # Se já pode atirar novamente...
        if elapsed_ticks > self.shoot_ticks:
            self.last_shot = now
            new_bullet = Bullet(self.assets, self.rect.top, self.rect.centerx)
            self.groups['all_sprites'].add(new_bullet)
            self.groups['all_bullets'].add(new_bullet)
            self.assets['pew_sound'].play()

    
class barquinho(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['barquinho']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura-largura_barquinhos)
        self.rect.y = random.randint(-100, -altura_barquinhos)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 9)

    def update(self):
        # Atualizando a posição do meteoro
        self.rect.x += self.speedx
        self.rect.y += self.speedy
       
        if self.rect.top > altura or self.rect.right < 0 or self.rect.left > largura:
            self.rect.x = random.randint(0, largura-largura_barquinhos)
            self.rect.y = random.randint(-100, -altura_barquinhos)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 9)


# Classe Bullet que representa os tiros
class Bullet(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, bottom, centerx):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['bullet_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedy = -10  # Velocidade fixa para cima

    def update(self):
        # A bala só se move no eixo y
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()




class Explosion(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, center, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.explosion_anim = assets['explosion_anim']

        
        self.frame = 0  # Armazena o índice atual na animação
        self.image = self.explosion_anim[self.frame]  # Pega a primeira imagem
        self.rect = self.image.get_rect()
        self.rect.center = center  # Posiciona o centro da imagem

        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 50

    def update(self):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update

        if elapsed_ticks > self.frame_ticks:
            self.last_update = now

            self.frame += 1

            if self.frame == len(self.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

tempo = pygame.time.Clock()
FPS = 30

all_sprites = pygame.sprite.Group()
sprite_barquinhos = pygame.sprite.Group()
sprite_projetil = pygame.sprite.Group()
groups = {}
groups['all_sprites'] = all_sprites
groups['sprite_barquinhos'] = sprite_barquinhos
groups['sprite_projetil'] = sprite_projetil

# Criando o jogador
player = navio(groups, assets)
all_sprites.add(player)
for i in range(8):
    barco = barquinho(assets)
    all_sprites.add(barco)
    sprite_barquinhos.add(barco)

DONE = 0
PLAYING = 1
EXPLODING = 2
state = PLAYING

keys_down = {}
score = 0
lives = 3

# ===== Loop principal =====

#pygame.mixer.music.play(loops=-1)
while state != DONE:
    tempo.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            state = DONE
        # Só verifica o teclado se está no estado de jogo
        if state == PLAYING:
            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade.
                keys_down[event.key] = True
                if event.key == pygame.K_LEFT:
                    player.speedx -= 8
                if event.key == pygame.K_RIGHT:
                    player.speedx += 8
                if event.key == pygame.K_SPACE:
                    player.shoot()
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key in keys_down and keys_down[event.key]:
                    if event.key == pygame.K_LEFT:
                        player.speedx += 8
                    if event.key == pygame.K_RIGHT:
                        player.speedx -= 8

    # ----- Atualiza estado do jogo
    # Atualizando a posição dos meteoros
    all_sprites.update()

    if state == PLAYING:
        hits = pygame.sprite.groupcollide(sprite_barquinhos, sprite_projetil, True, True, pygame.sprite.collide_mask)
        for meteor in hits: 
            assets['destroy_sound'].play()
            m = barco(assets)
            all_sprites.add(m)
            sprite_barquinhos.add(m)

            explosao = Explosion(meteor.rect.center, assets)
            all_sprites.add(explosao)

            score += 100
            if score % 1000 == 0:
                lives += 1

        hits = pygame.sprite.spritecollide(player, sprite_barquinhos, True, pygame.sprite.collide_mask)
        if len(hits) > 0:
            assets['boom_sound'].play()
            player.kill()
            lives -= 1
            explosao = Explosion(player.rect.center, assets)
            all_sprites.add(explosao)
            state = EXPLODING
            keys_down = {}
            explosion_tick = pygame.time.get_ticks()
            explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400
    elif state == EXPLODING:
        now = pygame.time.get_ticks()
        if now - explosion_tick > explosion_duration:
            if lives == 0:
                state = DONE
            else:
                state = PLAYING
                player = navio(groups, assets)
                all_sprites.add(player)

    tamanho.fill((0, 0, 0))  # Preenche com a cor branca
    tamanho.blit(assets['fundo'], (0, 0))
    # Desenhando meteoros
    all_sprites.draw(tamanho)

    text_surface = assets['score_font'].render("{:08d}".format(score), True, (255, 255, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (largura / 2,  10)
    tamanho.blit(text_surface, text_rect)

    text_surface = assets['score_font'].render(chr(9829) * lives, True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.bottomleft = (10, altura - 10)
    tamanho.blit(text_surface, text_rect)

    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados 