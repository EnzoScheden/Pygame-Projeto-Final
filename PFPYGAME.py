import pygame 

import pygame.mixer

import random 

pygame.init()

pygame.mixer.init()


largura = 1000

altura = 480 

tamanho = pygame.display.set_mode((largura,altura))




largura_barquinhos = 50

altura_barquinhos = 38 

navio_largura = 70

navio_altura = 46




assets = {}
assets['tiro_sound'] = pygame.mixer.Sound('sons/9mm-pistol-shot-6349.wav')
assets['fundo_sound'] = pygame.mixer.Sound('sons/harbour_seagulls_day_2-22341.wav')
assets['fundo'] = pygame.image.load('img/mar-visto-a-partir-de-cima.jpg').convert()
assets['barquinho'] = pygame.image.load('img/pngwing.com.png').convert_alpha()
assets['barquinho'] = pygame.transform.scale(assets['barquinho'], (largura_barquinhos, altura_barquinhos))
assets['navio'] = pygame.image.load('img/navio-de-guerra.png').convert_alpha()
assets['navio'] = pygame.transform.scale(assets['navio'], (navio_largura, navio_altura))
assets['bala'] = pygame.image.load('img/laserRed16.png').convert_alpha()
assets['bala'] = pygame.transform.scale(assets['bala'], (32,23.5))
assets['tela_inicio'] = pygame.image.load('img/tela inicial jogo pygame.png').convert()
assets['tela_inicio'] = pygame.transform.scale(assets['tela_inicio'], (1000, 480))

def tela_inicio():
    inicio = True
    while inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inicio = False

        tamanho.blit(assets['tela_inicio'],(0,0))
        

        pygame.display.update()

        if inicio:
            assets['fundo_sound'].play()


#função tela fim 
def tela_fim():
    assets['fundo_sound'].stop()
    fim = True
    while fim:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        tamanho.fill((0, 0, 0))
        game_over_text = assets['score_font'].render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (largura / 2, altura / 2)
        tamanho.blit(game_over_text, game_over_rect)

        pygame.display.update()


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
        self.rect.centerx = largura / 10
        self.rect.centery = altura /2  # Posição inicial no centro superior da tela
        self.speedy = 0  # Velocidade inicial vertical é zero (não se move no início)
        self.groups = groups
        self.assets = assets

        # Novos atributos para atirar
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500  # Ajuste o valor conforme necessário

    def update(self):
        # Atualiza posição vertical
        self.rect.y += self.speedy

        # Mantém o navio na tela verticalmente
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > altura:
            self.rect.bottom = altura

    def shoot(self):
        # Verifica se pode atirar
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_shot

        # Se já pode atirar novamente...
        if elapsed_ticks > self.shoot_ticks:
            self.last_shot = now
            new_bullet = Bullet(self.assets, self.rect.top, self.rect.centerx)
            self.groups['all_sprites'].add(new_bullet)
            self.groups['sprite_projetil'].add(new_bullet)
            assets['tiro_sound'].play()
            


    
class barquinho(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['barquinho']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = largura  
        self.rect.y = random.randint(0, altura - altura_barquinhos)  
        self.speedx = random.randint(-20,-14)  
        self.speedy = random.randint(-3,3) 


    def update(self):
        # Atualizando a posição do barquinho
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Verifica se o barquinho saiu da tela pela esquerda
        if self.rect.right < 0:
            self.rect.x = largura  
            self.rect.y = random.randint(0, altura - altura_barquinhos)  
            self.speedx = random.randint(-20, -14)  
            self.speedy = random.randint(-3,3)  


# Classe Bullet que representa os tiros
class Bullet(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, bottom, centerx):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['bala']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedx = 10  # Velocidade fixa para cima

    def update(self):
        # A bala só se move no eixo y
        self.rect.x += self.speedx

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
# ... (código existente)

# ===== Loop principal =====
#pygame.mixer.music.play(loops=-1)

tela_inicio()


while state != DONE:
    tempo.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # Verifica consequências
        if event.type == pygame.QUIT:
            state = DONE

        # Só verifica o teclado se está no estado de jogo
        if state == PLAYING:
            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade.
                keys_down[event.key] = True
                
                if event.key == pygame.K_w:  # Tecla "W" para mover para cima
                    player.speedy -= 8
                if event.key == pygame.K_s:  # Tecla "S" para mover para baixo
                    player.speedy += 8
                if event.key == pygame.K_SPACE:
                    player.shoot()

            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key in keys_down and keys_down[event.key]:
                  
                    if event.key == pygame.K_w:  # Tecla "W" solta para mover para cima
                        player.speedy += 8
                    if event.key == pygame.K_s:  # Tecla "S" solta para mover para baixo
                        player.speedy -= 8




    # ----- Atualiza estado do jogo
    # Atualizando a posição dos meteoros
    all_sprites.update()

    if state == PLAYING:
        hits = pygame.sprite.groupcollide(sprite_barquinhos, sprite_projetil, True, True, pygame.sprite.collide_mask)
        for meteor in hits: 
            #assets['destroy_sound'].play()
            m = barquinho(assets)
            all_sprites.add(m)
            sprite_barquinhos.add(m)

            explosao = Explosion(meteor.rect.center, assets)
            all_sprites.add(explosao)

            score += 100
            if score % 10000 == 0:
                lives += 1

        hits = pygame.sprite.spritecollide(player, sprite_barquinhos, True, pygame.sprite.collide_mask)
        if len(hits) > 0:
           
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

    if state == DONE:
        tela_fim()

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados 