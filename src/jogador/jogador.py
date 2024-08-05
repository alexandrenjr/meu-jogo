import pygame
from utils.objeto import Objeto
from jogo.jogo_config import JogoConfig
from jogador.jogador_config import JogadorConfig
import math

class Jogador(Objeto):
    def __init__(self, config: JogadorConfig) -> None:
        super().__init__(config.X, config.Y, config.LARGURA, config.ALTURA, config.VELOCIDADE, config.COR)
        self.janela_largura = JogoConfig.JANELA_LARGURA
        self.janela_altura = JogoConfig.JANELA_ALTURA
        self.pontos_modulo_principal = config.PONTOS_MODULO_PRINCIPAL
        self.pontos_asas = config.PONTOS_ASAS
        self.pontos_foquete_esquerdo = config.PONTOS_FOQUETE_ESQUERDO
        self.pontos_foquete_direito = config.PONTOS_FOQUETE_DIREITO
        self.pontos_hitboxes = [hitbox for hitbox in config.HITBOXES]
        self.hitboxes = [pygame.Rect(hitbox.x, hitbox.y, hitbox.largura, hitbox.altura) for hitbox in self.pontos_hitboxes]

    def mover(self, teclas) -> None:
        dx, dy = 0, 0
        
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy += 1

        if dx != 0 and dy != 0:
            dx *= self.velocidade / math.sqrt(2)
            dy *= self.velocidade / math.sqrt(2)
        else:
            dx *= self.velocidade
            dy *= self.velocidade

        if self.rect.x + dx >= 0 and self.rect.x + dx + self.rect.width <= self.janela_largura:
            self.rect.x += dx
        if self.rect.y + dy >= 0 and self.rect.y + dy + self.rect.height <= self.janela_altura:
            self.rect.y += dy

    def desenhar(self, janela: pygame.Surface) -> None:
        pontos_modulo_principal_ajustados = [(self.rect.x + px, self.rect.y + py) for px, py in self.pontos_modulo_principal]
        pontos_asas_ajustados = [(self.rect.x + px, self.rect.y + py) for px, py in self.pontos_asas]
        pontos_foquete_esquerdo_ajustados = [(self.rect.x + px, self.rect.y + py) for px, py in self.pontos_foquete_esquerdo]
        pontos_foquete_direito_ajustados = [(self.rect.x + px, self.rect.y + py) for px, py in self.pontos_foquete_direito]

        # pygame.draw.rect(janela, self.cor, self.rect, 2)
        pygame.draw.polygon(janela, self.cor, pontos_modulo_principal_ajustados)
        pygame.draw.polygon(janela, self.cor, pontos_asas_ajustados)
        pygame.draw.polygon(janela, self.cor, pontos_foquete_esquerdo_ajustados)
        pygame.draw.polygon(janela, self.cor, pontos_foquete_direito_ajustados)
        # cores = interpolar_cores(len(self.hitboxes), (255, 0, 255), (255, 0, 0))
        for i, hitbox in enumerate(self.hitboxes):
            hitbox.x = self.rect.x + self.pontos_hitboxes[i].x
            hitbox.y = self.rect.y + self.pontos_hitboxes[i].y
            # pygame.draw.rect(janela, cores[i], hitbox, 2)
