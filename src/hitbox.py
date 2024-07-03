import pygame

class Hitbox:
    def __init__(self, x: float, y: float, largura: float, altura: float) -> None:
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y