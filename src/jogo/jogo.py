import pygame
import time
import random
from jogo.jogo_config import JogoConfig
from jogo.paralaxe import Paralaxe
from jogador.jogador_config import JogadorConfig
from jogador.jogador import Jogador
from jogador.projetil_config import ProjetilConfig
from jogador.projetil import Projetil
from utils.helpers import *

class Jogo:
    def __init__(self) -> None:
        """Inicialização do Pygame e configurações gerais."""
        pygame.font.init()
        pygame.display.set_caption("Meu jogo")
        self.janela = pygame.display.set_mode((JogoConfig.JANELA_LARGURA, JogoConfig.JANELA_ALTURA))
        camadas_imagens_caminhos = [buscar_caminho_arquivo("layer1.png")]
        camadas_imagens_velocidades = [0.5, 2]
        self.paralaxe = Paralaxe(self.janela, camadas_imagens_caminhos, camadas_imagens_velocidades)
        self.jogador = Jogador(JogadorConfig)
        self.relogio = pygame.time.Clock()
        self.fonte_tempo = pygame.font.Font(None, 30)
        self.tempo_inicio = time.time()
        self.tempo_decorrido = 0
        self.projeteis = []
        self.nave_projeteis = []
        self.projetil_tempo_inc = 2000
        self.projetil_quantidade = 0
        self.nave_projetil_tempo = 150
        self.nave_projetil_quantidade = 0
        self.colisao = False


    def adicionar_projeteis(self) -> None:
        """Adiciona os projéteis que vêm de cima (meteoros)."""
        for cor in interpolar_cores(random.randint(1, 4), (218, 165, 32), (202, 31, 123)):
            projetil_x = random.randint(0, JogoConfig.JANELA_LARGURA - ProjetilConfig.LARGURA)
            projetil = Projetil(projetil_x, -ProjetilConfig.ALTURA, ProjetilConfig.LARGURA, ProjetilConfig.ALTURA, ProjetilConfig.VELOCIDADE, cor)
            self.projeteis.append(projetil)
        self.projetil_tempo_inc = max(200, self.projetil_tempo_inc - 50)
        self.projetil_quantidade = 0


    def adicionar_nave_projeteis(self) -> None:
        """Adiciona projéteis que saem da nave (tiros)."""
        projetil_x = self.jogador.rect.x + (JogadorConfig.LARGURA / 2) - (JogadorConfig.PROJETIL_LARGURA / 2)
        projetil = Projetil(projetil_x, self.jogador.rect.y + JogadorConfig.PROJETIL_ALTURA, JogadorConfig.PROJETIL_LARGURA, JogadorConfig.PROJETIL_ALTURA, JogadorConfig.PROJETIL_VELOCIDADE, (253, 0, 24))
        self.nave_projeteis.append(projetil)
        self.nave_projetil_quantidade = 0


    def checar_colisoes_nave(self) -> None:
        """Checa se um dos projéteis (meteoro) atingiu a nave."""
        projeteis_para_remover = []
        for projetil in self.projeteis:
            try:
                projetil.mover("baixo")
            except ValueError as e:
                print(e)
            if projetil.rect.y > JogoConfig.JANELA_ALTURA:
                projeteis_para_remover.append(projetil)
            else:
                for hitbox in self.jogador.hitboxes:
                    if projetil.rect.colliderect(hitbox):
                        projeteis_para_remover.append(projetil)
                        self.colisao = True
                if self.colisao:
                    break
        
        for projetil in projeteis_para_remover:
            if projetil in self.projeteis:
                self.projeteis.remove(projetil)


    def checar_colisoes_nave_projeteis(self) -> None:
        """Checa se um dos projéteis da nave (tiro) atingiu algum projétil (meteoro)."""
        projeteis_para_remover = []
        nave_projeteis_para_remover = []
        for nave_projetil in self.nave_projeteis:
            try:
                nave_projetil.mover("cima")
            except ValueError as e:
                print(e)
            
            if nave_projetil.rect.y < 0:
                nave_projeteis_para_remover.append(nave_projetil)
            else:
                for projetil in self.projeteis:
                    if projetil.rect.colliderect(nave_projetil):
                        projeteis_para_remover.append(projetil)

        for projetil in projeteis_para_remover:
            if projetil in self.projeteis:
                self.projeteis.remove(projetil)

        for nave_projetil in nave_projeteis_para_remover:
            if nave_projetil in self.nave_projeteis:
                self.nave_projeteis.remove(nave_projetil)


    def desenhar(self) -> None:
        """Desenha o jogo."""
        self.janela.fill((0, 0, 0))
        self.paralaxe.rolar()
        self.jogador.desenhar(self.janela)
        self.fonte_tempo = FONTE_TEMPO.render(f"Tempo: {round(self.tempo_decorrido)}s", 1, "white")
        for projetil in self.projeteis:
            projetil.desenhar(self.janela)
        for nave_projetil in self.nave_projeteis:
            nave_projetil.desenhar(self.janela)
        self.janela.blit(self.fonte_tempo, (10, 10))
        pygame.display.update()


    def mostrar_mensagem_derrota(self) -> None:
        """Mostra a mensagem de derrota."""
        texto_derrota = FONTE_DERROTA.render("Você perdeu!", 1, "white")
        self.janela.blit(texto_derrota, centralizar((texto_derrota.get_width(), texto_derrota.get_height()), (JogoConfig.JANELA_LARGURA, JogoConfig.JANELA_ALTURA)))
        pygame.display.update()
        pygame.time.delay(3000)


    def executar(self) -> None:
        """Execução do jogo."""
        while True:
            tick = self.relogio.tick(60)
            self.nave_projetil_quantidade += tick
            self.projetil_quantidade += tick
            self.tempo_decorrido = time.time() - self.tempo_inicio

            if self.projetil_quantidade > self.projetil_tempo_inc:
                self.adicionar_projeteis()

            if self.nave_projetil_quantidade > self.nave_projetil_tempo:
                self.adicionar_nave_projeteis()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                        return

            self.jogador.mover(pygame.key.get_pressed())
            self.checar_colisoes_nave()
            self.checar_colisoes_nave_projeteis()

            if self.colisao:
                self.mostrar_mensagem_derrota()
                break

            self.desenhar()