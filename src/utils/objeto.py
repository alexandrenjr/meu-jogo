import pygame
from utils.tipos import CorRGB

class Objeto:
    def __init__(self, x: float, y: float, largura: float, altura: float, velocidade: float, cor: CorRGB) -> None:
        self.rect = pygame.Rect(x, y, largura, altura)
        self.velocidade = velocidade
        self.cor = cor


    def mover(self) -> None:
        pass


    def desenhar(self, janela: pygame.Surface) -> None:
        pygame.draw.rect(janela, self.cor, self.rect)