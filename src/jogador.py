import pygame
from config import Config

class Jogador:
    def __init__(self, config):
        self.rect = pygame.Rect(config.jogador.X,
                                config.jogador.Y,
                                config.jogador.LARGURA,
                                config.jogador.ALTURA
                            )
        self.cor = config.jogador.COR
        self.velocidade = config.jogador.VELOCIDADE
        self.janela_largura = config.jogo.JANELA_LARGURA
        self.pontos_modulo_principal = config.jogador.PONTOS_MODULO_PRINCIPAL
        self.pontos_asas = config.jogador.PONTOS_ASAS
        self.pontos_foquete_esquerdo = config.jogador.PONTOS_FOQUETE_ESQUERDO
        self.pontos_foquete_direito = config.jogador.PONTOS_FOQUETE_DIREITO
        # self.hitboxes = [
        #     pygame.Rect(x, y, largura-10, altura),
        #     pygame.Rect(x, y, largura-15, altura),
        #     pygame.Rect(x, y, largura-20, altura),
        #     pygame.Rect(x, y, largura-24, altura),
        # ]

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.x - self.velocidade >= 0:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.x + self.velocidade + self.rect.width <= self.janela_largura:
            self.rect.x += self.velocidade

        # for i, hitbox in enumerate(self.hitboxes):
        #     if teclas[pygame.K_LEFT] and self.rect.x - self.velocidade >= 0:
        #         hitbox.x -= self.velocidade
        #     if teclas[pygame.K_RIGHT] and self.rect.x + self.velocidade + self.rect.width <= self.janela_largura:
        #         hitbox.x += self.velocidade

    def desenhar(self, janela):
        pontos_modulo_principal_ajustados = [(self.rect.x + px, self.rect.y + py) for px, py in self.pontos_modulo_principal]
        pontos_asas_ajustados = [(self.rect.x + px, self.rect.y + py) for px, py in self.pontos_asas]
        pontos_foquete_esquerdo_ajustados = [(self.rect.x + px, self.rect.y + py) for px, py in self.pontos_foquete_esquerdo]
        pontos_foquete_direito_ajustados = [(self.rect.x + px, self.rect.y + py) for px, py in self.pontos_foquete_direito]

        # for i, hitbox in enumerate(self.hiboxes):
        #     pygame.draw.rect(janela, f"chartreuse{i + 1}", hitbox, 2)

        pygame.draw.polygon(janela, self.cor, pontos_asas_ajustados)
        pygame.draw.polygon(janela, self.cor, pontos_modulo_principal_ajustados)
        pygame.draw.polygon(janela, self.cor, pontos_foquete_esquerdo_ajustados)
        pygame.draw.polygon(janela, self.cor, pontos_foquete_direito_ajustados)
        # pygame.draw.rect(janela, "red", self.rect, 2)
