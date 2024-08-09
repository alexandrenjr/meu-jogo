import pygame
import random
import os
from utils.tipos import *


def buscar_caminho_arquivo(nome_arquivo: str, pasta: str = "") -> str:
        """Retorna o caminho absoluto para a imagem de fundo."""
        return os.path.join(os.getcwd(), pasta, nome_arquivo)


def centralizar(objeto: Coordenadas2, janela: Coordenadas2) -> Coordenadas2:
    """Centraliza um objeto em um plano dado."""
    janela_largura, janela_altura = janela
    objeto_largura, objeto_altura = objeto
    return (janela_largura / 2 - objeto_largura / 2, janela_altura / 2 - objeto_altura / 2)


def centralizar_x(objeto_largura: int, janela_largura: int) -> int:
    """Centraliza no eixo x um objeto em uma superfície informada."""
    return janela_largura / 2 - objeto_largura / 2


def transitar_tela(superficie_principal: pygame.Surface, superficie: pygame.Surface, duracao: float = 0.001, aparecer_gradualmente: str = True) -> None:
    """Transita uma tela para uma tela preta ou vice-versa em um intervalo de tempo passado como parâmetro (duracao).
    O parâmetro aparecer_gradualmente define se a superfície passada como parâmetro deverá aparecer ou desaparacer gradualmente.
    """
    passo = 5
    atraso = int(duracao * 1000 / (255 // passo))

    if aparecer_gradualmente:
        intervalo_alfa = range(0, 256, passo)
    else:
        intervalo_alfa = range(255, -1, -passo)

    for alfa in intervalo_alfa:
        superficie.set_alpha(alfa)
        superficie_principal.fill((0, 0, 0))
        superficie_principal.blit(pygame.transform.scale(superficie, superficie_principal.get_size()), (0, 0))
        pygame.display.update()
        pygame.time.delay(atraso)


def obter_cor_aleatoria(n: int, cores: list[CorRGB]) -> list[int]:
    """Obtém n cores aleatórias num conjuto de cores passado como parâmetro."""
    indices = random.sample(range(len(cores)), n)
    return [cores[indice] for indice in indices]


def interpolar_cores(n: int=2, cor1: CorRGB=(0, 0, 0), cor2: CorRGB=(255, 255, 255)) -> list[CorRGB]:
    """Dado duas cores cor1 e cor2, em RGB, a função retorna n tons entre elas.
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