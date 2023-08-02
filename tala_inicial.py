import pygame
from pygame.locals import *
import random

pygame.init()

largura = 1000
altura = 480
tam_tela = (largura, altura)
tela = pygame.display.set_mode(tam_tela)
pygame.display.set_caption('Highway Rush!')

# Importa imagens
BackMenu = pygame.image.load('assets\Menu.png').convert_alpha()
BackMenu = pygame.transform.scale(BackMenu, (900, 600))
rulesmenu = pygame.image.load('assets\Regras.png').convert_alpha()
rule_smenu = pygame.transform.scale(rulesmenu, (900, 600))

def tela_de_inicio():
    # Loop para exibir a tela de início
    inicio = True
    botao_jogar = None
    botao_exit = None
    botao_rules = None
    while inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se o clique foi no botão "Jogar"
                if botao_jogar.collidepoint(event.pos):
                    return 'jogar'
                # Verifica se o clique foi no botão "como jogar"
                if botao_rules.collidepoint(event.pos):
                    return 'como jogar'
                if botao_exit.collidepoint(event.pos):
                    return 'sair'

        # Desenha o fundo na tela
        tela.fill((0, 0, 0))
        tela.blit(BackMenu, (0, 0))

        # Configurações do botão "Jogar"
        cor_botao_jogar = (0, 0, 0, 0)  # preto
        largura_botao = 200
        altura_botao = 50
        x_botao = 60
        y_botao = 320
        botao_jogar = pygame.Rect(x_botao, y_botao, largura_botao, altura_botao)

        # Configurações do botão "Exit"
        cor_botao_exit = (255, 255, 255)  # branco
        largura_botao_exit = 150
        altura_botao_exit = 50
        x_botao_exit = 60
        y_botao_exit = 420
        botao_exit = pygame.Rect(x_botao_exit, y_botao_exit, largura_botao_exit, altura_botao_exit)


        # Atualiza a tela
        pygame.display.flip()

def tela_rules():
    # Loop para exibir a tela de início
    inicio = True
    botao_return = None
    while inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se o clique foi no botão "Return"
                if botao_return.collidepoint(event.pos):
                    return 'menu'
                
        # Desenha o fundo na tela
        tela.fill((0, 0, 0))
        tela.blit(rule_smenu, (0, 0))  

        # Configuração do botão "Return"
        cor_botao = (255, 255, 255)  # branco
        largura_botao_return = 200
        altura_botao_return = 50
        x_botao_return = 60
        y_botao_return = 520
        botao_return = pygame.Rect(x_botao_return, y_botao_return, largura_botao_return, altura_botao_return)  

        # Atualiza a tela
        pygame.display.flip()

# Inicialização de variáveis
jogando = True
Menu = True
Tela = 'menu'  # Estado inicial do jogo

while jogando:
    while Menu:
        if Tela == 'menu':
            Tela = tela_de_inicio()
            if Tela == 'como jogar':
                Tela = tela_rules()
        elif Tela == 'como jogar':
            # Loop para exibir a tela de instruções
            while Tela == 'como jogar':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                # Mostra o novo frame para o jogador
                pygame.display.update()
        elif Tela == 'sair':
            jogando = False
            Menu = False
            pygame.quit()
            quit()
        else:
            space_pressed = False
            jogando = True
            Menu = False