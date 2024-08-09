import pygame
from utils.objeto import Objeto
from utils.tipos import *

class Projetil(Objeto):
    def __init__(self, x: float, y: float, largura: float, altura: float, velocidade: float, cor: CorRGB) -> None:
        super().__init__(x, y, largura, altura, velocidade, cor)

    def mover(self, sentido: str="baixo") -> None:
        """Move um projétil a uma velocidade pré-determinada e a um sentido informado ("cima" ou "baixo")."""
        if sentido == "baixo":
            self.rect.y += self.velocidade
        elif (sentido == "cima"):
            self.rect.y -= self.velocidade
        else:
            raise ValueError(f"Valor invalido para sentido: {sentido}, Deve ser 'cima' ou 'baixo'.")

    def desenhar(self, superficie_principal: pygame.Surface) -> None:
        super().desenhar(superficie_principal)
