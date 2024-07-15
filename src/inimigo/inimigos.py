import pygame
from utils.objeto import Objeto
from utils.tipos import *
from inimigo.inimigos_config import AlConfig, LulanosConfig
from utils.hitbox import Hitbox

class Al(Objeto):
    def __init__(self, x: float, y: float, largura: float, altura: float, velocidade: float, cor: CorRGB) -> None:
        super().__init__(x, y, largura, altura, velocidade, cor)
        self.pontos_hitboxes = [hitbox for hitbox in AlConfig.HITBOXES]
        self.hitboxes = [pygame.Rect(hitbox.x, hitbox.y, hitbox.largura, hitbox.altura) for hitbox in self.pontos_hitboxes]

    def mover(self) -> None:
        self.rect.y += self.velocidade

    def desenhar(self, janela) -> None:
        for i, hitbox in enumerate(self.hitboxes):
            hitbox.x = self.rect.x + self.pontos_hitboxes[i].x
            hitbox.y = self.rect.y + self.pontos_hitboxes[i].y
            pygame.draw.rect(janela, self.cor, hitbox)

class Lulanos(Objeto):
    def __init__(self, x: float, y: float, largura: float, altura: float, velocidade: float, cor: CorRGB) -> None:
        super().__init__(x, y, largura, altura, velocidade, cor)
        self.pontos_cabeca = LulanosConfig.PONTOS_CABECA
        self.pontos_joias = LulanosConfig.PONTOS_JOIAS
        self.pontos_tentaculos = LulanosConfig.PONTOS_JOIAS
        hitboxes = self.pontos_cabeca + self.pontos_joias + self.pontos_tentaculos
        self.pontos_hitboxes = [hitbox for hitbox in hitboxes]
        self.hitboxes = [pygame.Rect(hitbox.x, hitbox.y, hitbox.largura, hitbox.altura) for hitbox in self.pontos_hitboxes]

    def mover(self) -> None:
        self.rect.y += self.velocidade

    def _desenhar(self, janela, hitboxes: Hitbox) -> None:
        for hitbox in hitboxes:
            hitbox.x = self.rect.x + self.pontos_hitboxes[i].x
            hitbox.y = self.rect.y + self.pontos_hitboxes[i].y
            pygame.draw.rect(janela, self.cor, hitbox)

    def desenhar(self, janela) -> None:
        self._desenhar(janela, self.pontos_cabeca)
        pygame.draw.rect(janela, (255, 255, 255), self.rect, 2)