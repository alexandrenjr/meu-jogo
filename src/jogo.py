import pygame
import time
import random
from jogador import Jogador
from projetil import Projetil
from util import *
from config import *

# Inicialização do Pygame e configurações gerais
pygame.font.init()
pygame.display.set_caption("Meu jogo")
JANELA = pygame.display.set_mode((Config.jogo.JANELA_LARGURA, Config.jogo.JANELA_ALTURA))
PLANO_DE_FUNDO = pygame.transform.scale(pygame.image.load(buscar_path_imagem()), (Config.jogo.JANELA_LARGURA, Config.jogo.JANELA_ALTURA))


def adicionar_projeteis(tempo_inc, projeteis):
    for indice in obter_cor_aleatoria(random.randint(1, 4), Config.cores.PROJETEIS):
            projetil_x = random.randint(0, Config.jogo.JANELA_LARGURA - Config.projetil.LARGURA)
            cor = Config.cores.PROJETEIS.get(indice, "red")
            projetil = Projetil(projetil_x, -Config.projetil.ALTURA, Config.projetil.LARGURA, Config.projetil.ALTURA, Config.projetil.VELOCIDADE, cor)
            projeteis.append(projetil)
    return (projeteis, max(200, tempo_inc - 50), 0)


def adicionar_nave_projeteis(jogador_x, nave_projeteis):
    projetil_x = jogador_x + (Config.jogador.LARGURA / 2)
    projetil = Projetil(projetil_x, Config.jogo.JANELA_ALTURA - Config.jogador.ALTURA - Config.jogador.PROJETIL_ALTURA, Config.jogador.PROJETIL_LARGURA, Config.jogador.PROJETIL_ALTURA, Config.jogador.VELOCIDADE, "orange")
    nave_projeteis.append(projetil)
    return nave_projeteis, 0


def executar_jogo():
    executar = True
    jogador = Jogador(Config)
    relogio = pygame.time.Clock()
    tempo_inicio = time.time()
    tick = 0
    projetil_tempo_inc = 2000
    projetil_quantidade = 0
    projeteis = []
    nave_projetil_tempo = 500
    nave_projetil_quantidade = 0
    nave_projeteis = []
    colisao = False

    while executar:
        tick = relogio.tick(60)
        nave_projetil_quantidade += tick
        projetil_quantidade += tick
        tempo_decorrido = time.time() - tempo_inicio

        if projetil_quantidade > projetil_tempo_inc:
            projeteis, projetil_tempo_inc, projetil_quantidade = adicionar_projeteis(projetil_tempo_inc, projeteis)

        if nave_projetil_quantidade > nave_projetil_tempo:
            nave_projeteis, nave_projetil_quantidade = adicionar_nave_projeteis(jogador.rect.x, nave_projeteis)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                executar = False
                break

        jogador.mover(pygame.key.get_pressed())

        for projetil in projeteis[:]:
            try:
                projetil.mover("baixo")
            except ValueError as e:
                print(e)
            if projetil.rect.y > Config.jogo.JANELA_ALTURA:
                projeteis.remove(projetil)
            elif projetil.rect.colliderect(jogador.rect):
                projeteis.remove(projetil)
                colisao = True
                break

        for nave_projetil in nave_projeteis[:]:
            try:
                nave_projetil.mover("cima")
            except ValueError as e:
                print(e)
            if nave_projetil.rect.y < 0:
                nave_projeteis.remove(nave_projetil)

        if colisao:
            texto_derrota = FONTE_DERROTA.render("Você perdeu!", 1, "white")
            JANELA.blit(texto_derrota, centralizar((texto_derrota.get_width(), texto_derrota.get_height()), (Config.jogo.JANELA_LARGURA, Config.jogo.JANELA_ALTURA)))
            pygame.display.update()
            pygame.time.delay(3000)
            break

        desenhar_jogo(JANELA, PLANO_DE_FUNDO, jogador, tempo_decorrido, projeteis, nave_projeteis)

    pygame.quit()
