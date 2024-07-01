import pygame
import random
import os

pygame.init()
pygame.font.init()
FONTE_TEMPO = pygame.font.SysFont("Lexend", 30)
FONTE_DERROTA = pygame.font.SysFont("Lexend", 60)


def buscar_path_imagem(filename):
        """Retorna o caminho absoluto para a imagem de fundo."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, '..', 'assets', filename)


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


def interpolar_cores(n, cor1=(0, 0, 0), cor2=(255, 255, 255)):
    """Dados duas cores cor1 e cor2, é retornado n tons entre elas.
    Se o parâmetro n for menor que 2, cor1 será retornada.

    Parâmetros:
        int n: quantidade de tons desejadas
        cor1: cor inicial em RGB
        cor2: cor final em RGB
    """
    cores = []
    if n < 2:
        cores.append(cor1)
        return cores
    for i in range(n):
        t = i / (n - 1)
        r = round((1 - t) * cor1[0] + t * cor2[0])
        g = round((1 - t) * cor1[1] + t * cor2[1])
        b = round((1 - t) * cor1[2] + t * cor2[2])
        cores.append((r, g, b))
    return cores