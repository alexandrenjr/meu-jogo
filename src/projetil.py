import pygame
from tipos import *

class Projetil:
    def __init__(self, x: float, y: float, largura: float, altura: float, velocidade: float, cor: CorRGB) -> None:
        self.rect = pygame.Rect(x, y, largura, altura)
        self.velocidade = velocidade
        self.cor = cor

    def mover(self, sentido: str="baixo") -> None:
        """Move um projétil a uma velocidade pré-determinada e a um sentido informado ("cima" ou "baixo")."""
        if sentido == "baixo":
            self.rect.y += self.velocidade
        elif (sentido == "cima"):
            self.rect.y -= self.velocidade
        else:
            raise ValueError(f"Valor invalido para sentido: {sentido}, Deve ser 'cima' ou 'baixo'.")

    def desenhar(self, janela) -> None:
        pygame.draw.rect(janela, self.cor, self.rect)
