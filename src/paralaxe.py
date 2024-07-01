import pygame

class Paralaxe:
    def __init__(self, janela, camadas_imagens_caminhos, camadas_imagens_velocidades) -> None:
        self.janela = janela
        self.camadas_imagens = [pygame.image.load(imagem_caminho).convert_alpha() for imagem_caminho in camadas_imagens_caminhos]
        self.camadas_imagens_alturas = [camada_imagem.get_height() for camada_imagem in self.camadas_imagens]
        self.camadas_imagens_y = [0 for _ in self.camadas_imagens]
        self.camadas_imagens_velocidades = camadas_imagens_velocidades

    def rolar(self) -> None:
        for i in range(len(self.camadas_imagens)):
            self.camadas_imagens_y[i] += self.camadas_imagens_velocidades[i]

            if self.camadas_imagens_y[i] >= self.camadas_imagens_alturas[i]:
                self.camadas_imagens_y[i] = 0

            self.janela.blit(self.camadas_imagens[i], (0, self.camadas_imagens_y[i]))
            self.janela.blit(self.camadas_imagens[i], (0, self.camadas_imagens_y[i] - self.camadas_imagens_alturas[i]))