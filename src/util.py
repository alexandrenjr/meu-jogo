import pygame
import random
import os

pygame.init()
pygame.font.init()
FONTE_TEMPO = pygame.font.SysFont("Lexend", 30)
FONTE_DERROTA = pygame.font.SysFont("Lexend", 60)


def desenhar_jogo(janela, plano_de_fundo, jogador, tempo_decorrido, projeteis, nave_projeteis):
    janela.blit(plano_de_fundo, (0, 0))
    fonte_tempo = FONTE_TEMPO.render(f"Tempo: {round(tempo_decorrido)}s", 1, "white")
    janela.blit(fonte_tempo, (10, 10))
    jogador.desenhar(janela)
    for projetil in projeteis:
        projetil.desenhar(janela)
    for nave_projetil in nave_projeteis:
        nave_projetil.desenhar(janela)
    pygame.display.update()


def buscar_path_imagem():
        """Retorna o caminho absoluto para a imagem de fundo."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, '..', 'assets', 'bg.jpg')


def centralizar(objeto, janela):
    """Centraliza um objeto em um plano dado."""
    janela_largura, janela_altura = janela
    objeto_largura, objeto_altura = objeto
    return (janela_largura / 2 - objeto_largura / 2, janela_altura / 2 - objeto_altura / 2)


def centralizar_x(objeto_largura, janela_largura):
    """Centraliza um objeto no eixo x."""
    return janela_largura / 2 - objeto_largura / 2


def obter_cor_aleatoria(i, cores):
    """Obtém i cores aleatórias num conjuto de cores."""
    return random.sample(range(len(cores)), i)