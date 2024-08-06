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
    """Centraliza um objeto no eixo x."""
    return janela_largura / 2 - objeto_largura / 2


def obter_cor_aleatoria(i: int, cores: list[CorRGB]) -> list[int]:
    """Obtém i cores aleatórias num conjuto de cores."""
    indices = random.sample(range(len(cores)), i)
    return [cores[indice] for indice in indices]


def interpolar_cores(n: int=2, cor1: CorRGB=(0, 0, 0), cor2: CorRGB=(255, 255, 255)) -> list[CorRGB]:
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