from util import centralizar_x
from pygame import Color

class JogoConfig:
    """Configurações da janela do jogo."""
    JANELA_LARGURA = 1366
    JANELA_ALTURA = 768


class JogadorConfig:
    """Configurações do jogador."""
    LARGURA = 60
    ALTURA = 60
    PROJETIL_LARGURA = 3
    PROJETIL_ALTURA = 8
    X = centralizar_x(LARGURA, JogoConfig.JANELA_LARGURA)
    Y = JogoConfig.JANELA_ALTURA - ALTURA
    COR = (161, 254, 117)
    VELOCIDADE = 10
    PONTOS_MODULO_PRINCIPAL = [
        (0.3388 * LARGURA, ALTURA),
        (LARGURA / 2, 0.92126 * ALTURA),
        (0.6612 * LARGURA, ALTURA),
        (0.5055 * LARGURA, 0),
        (0.4944 * LARGURA, 0)
    ]
    PONTOS_ASAS = [
        (0.1555 * LARGURA, 0.9265 * ALTURA),
        (0.8445 * LARGURA, 0.9265 * ALTURA),
        (0.5889 * LARGURA, 0.4068 * ALTURA),
        (0.4111 * LARGURA, 0.4068 * ALTURA)
    ]
    PONTOS_FOQUETE_ESQUERDO = [
        (0, 0.9265 * ALTURA),
        (0.2055 * LARGURA, 0.9265 * ALTURA),
        (0.11 * LARGURA, 0.6955 * ALTURA),
        (0.1 * LARGURA, 0.6955 * ALTURA)
    ]
    PONTOS_FOQUETE_DIREITO = [
        (0.7945 * LARGURA, 0.9265 * ALTURA),
        (LARGURA, 0.9265 * ALTURA),
        (0.90 * LARGURA, 0.6955 * ALTURA),
        (0.89 * LARGURA, 0.6955 * ALTURA)
    ]

class ProjetilConfig:
    """Configurações do projetil"""
    LARGURA = 10
    ALTURA = 20
    VELOCIDADE = 3


class Cores:
    """Cores"""
    PROJETEIS = {
        0: "plum",
        1: "plum1",
        2: "plum2",
        3: "plum3",
        4: "plum4"
    }

class Config:
    jogo = JogoConfig()
    jogador = JogadorConfig()
    projetil = ProjetilConfig()
    cores = Cores()