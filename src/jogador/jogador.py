import pygame
from utils.objeto import Objeto
from jogo.jogo_config import JogoConfig
from jogador.jogador_config import JogadorConfig

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
        if teclas[pygame.K_LEFT] and self.rect.x - self.velocidade >= 0:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.x + self.velocidade + self.rect.width <= self.janela_largura:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] and self.rect.y - self.velocidade >= 0:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] and self.rect.y + self.velocidade + self.rect.height <= self.janela_altura:
            self.rect.y += self.velocidade

    def desenhar(self, janela) -> None:
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
