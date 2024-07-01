import pygame

class Hitbox:
    def __init__(self, x, y, largura, altura):
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y