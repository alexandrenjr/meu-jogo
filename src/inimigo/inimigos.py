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

    def desenhar(self, superficie_principal: pygame.Surface, explodiu: bool = False) -> None:
        if explodiu:
            pygame.draw.rect(superficie_principal, (255, 0, 0), self.rect)

        for i, hitbox in enumerate(self.hitboxes):
            hitbox.x = self.rect.x + self.pontos_hitboxes[i].x
            hitbox.y = self.rect.y + self.pontos_hitboxes[i].y
            pygame.draw.rect(superficie_principal, self.cor, hitbox)

class Lulanos(Objeto):
    def __init__(self, x: float, y: float, largura: float, altura: float, velocidade: float, cores: list[CorRGB]) -> None:
        super().__init__(x, y, largura, altura, velocidade, (0, 0, 0))
        self.pontos_cabeca = LulanosConfig.PONTOS_CABECA
        self.pontos_joias = LulanosConfig.PONTOS_JOIAS
        self.pontos_tentaculos = LulanosConfig.PONTOS_TENTACULOS
        self.hitboxes_cabeca = [pygame.Rect(hitbox.x, hitbox.y, hitbox.largura, hitbox.altura) for hitbox in self.pontos_cabeca]
        self.hitboxes_joias = [pygame.Rect(hitbox.x, hitbox.y, hitbox.largura, hitbox.altura) for hitbox in self.pontos_joias]
        self.hitboxes_tentaculos = [pygame.Rect(hitbox.x, hitbox.y, hitbox.largura, hitbox.altura) for hitbox in self.pontos_tentaculos]
        self.hitboxes = self.hitboxes_cabeca + self.hitboxes_joias + self.hitboxes_tentaculos;
        self.cores = cores

    def mover(self) -> None:
        self.rect.y += self.velocidade

    def _desenhar(self, superficie_principal: pygame.Surface, cor: CorRGB, hitboxes: list[any], pontos_hitboxes: list[Hitbox]) -> None:
        for i, hitbox in enumerate(hitboxes):
            hitbox.x = self.rect.x + pontos_hitboxes[i].x
            hitbox.y = self.rect.y + pontos_hitboxes[i].y
            pygame.draw.rect(superficie_principal, cor, hitbox)

    def desenhar(self, superficie_principal: pygame.Surface) -> None:
        self._desenhar(superficie_principal, self.cores[0], self.hitboxes_cabeca, self.pontos_cabeca)
        self._desenhar(superficie_principal, self.cores[1], self.hitboxes_joias, self.pontos_joias)
        self._desenhar(superficie_principal, self.cores[2], self.hitboxes_tentaculos, self.pontos_tentaculos)