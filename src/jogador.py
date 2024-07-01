import pygame
from config import Config
from util import interpolar_cores

class Jogador:
    def __init__(self, config):
        self.rect = pygame.Rect(config.jogador.X, config.jogador.Y, config.jogador.LARGURA, config.jogador.ALTURA)
        self.cor = config.jogador.COR
        self.velocidade = config.jogador.VELOCIDADE
        self.janela_largura = config.jogo.JANELA_LARGURA
        self.janela_altura = config.jogo.JANELA_ALTURA
        self.pontos_modulo_principal = config.jogador.PONTOS_MODULO_PRINCIPAL
        self.pontos_asas = config.jogador.PONTOS_ASAS
        self.pontos_foquete_esquerdo = config.jogador.PONTOS_FOQUETE_ESQUERDO
        self.pontos_foquete_direito = config.jogador.PONTOS_FOQUETE_DIREITO
        self.pontos_hitboxes = [hitbox for hitbox in Config.jogador.HITBOXES]
        self.hitboxes = [pygame.Rect(hitbox.x, hitbox.y, hitbox.largura, hitbox.altura) for hitbox in self.pontos_hitboxes]

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.x - self.velocidade >= 0:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.x + self.velocidade + self.rect.width <= self.janela_largura:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] and self.rect.y - self.velocidade >= 0:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] and self.rect.y + self.velocidade + self.rect.height <= self.janela_altura:
            self.rect.y += self.velocidade

    def desenhar(self, janela):
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
        #     pygame.draw.rect(janela, cores[i], hitbox, 2)
