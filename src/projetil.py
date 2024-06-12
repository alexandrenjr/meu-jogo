import pygame

class Projetil:
    def __init__(self, x, y, largura, altura, velocidade, cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.velocidade = velocidade
        self.cor = cor

    def mover(self, sentido="baixo"):
        """Move um projétil a uma velocidade pré-determinada e a um sentido informado ("cima" ou "baixo")."""
        if sentido == "baixo":
            self.rect.y += self.velocidade
        elif (sentido == "cima"):
            self.rect.y -= self.velocidade
        else:
            raise ValueError(f"Valor invalido para sentido: {sentido}, Deve ser 'cima' ou 'baixo'.")

    def desenhar(self, janela):
        pygame.draw.rect(janela, self.cor, self.rect)
