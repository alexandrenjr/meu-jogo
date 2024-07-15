import pygame
import time
import random
from jogo.jogo_config import JogoConfig
from jogo.paralaxe import Paralaxe
from jogador.jogador_config import JogadorConfig
from jogador.jogador import Jogador
from jogador.projetil_config import ProjetilConfig
from jogador.projetil import Projetil
from inimigo.inimigos_config import AlConfig, LulanosConfig
from inimigo.inimigos import Al, Lulanos
from utils.helpers import *
from utils.objeto import Objeto

class Jogo:
    def __init__(self) -> None:
        """Inicialização do Pygame e configurações gerais."""
        pygame.font.init()
        pygame.display.set_caption("Meu jogo")
        self.janela = pygame.display.set_mode((JogoConfig.JANELA_LARGURA, JogoConfig.JANELA_ALTURA))
        camadas_imagens_caminhos = [buscar_caminho_arquivo("layer1.png")]
        camadas_imagens_velocidades = [1, 3]
        self.paralaxe = Paralaxe(self.janela, camadas_imagens_caminhos, camadas_imagens_velocidades)
        self.jogador = Jogador(JogadorConfig)
        self.relogio = pygame.time.Clock()
        self.fonte_tempo = pygame.font.Font(None, 30)
        self.tempo_inicio = time.time()
        self.tempo_decorrido = 0
        self.als = []
        self.lulanos = []
        self.nave_projeteis = []
        self.inimigos_tempo_inc = 2000
        self.inimigos_quantidade = 0
        self.lulanos_tempo_inc = 3000
        self.lulanos_quantidade = 0
        self.nave_projetil_tempo = 150
        self.nave_projetil_quantidade = 0
        self.colisao = False


    def adicionar_al(self) -> None:
        """Adiciona os projéteis que vêm de cima (meteoros)."""
        numero_inimigos = random.randint(1, 4)
        for _ in range(numero_inimigos):
            al_x = random.randint(0, JogoConfig.JANELA_LARGURA - AlConfig.LARGURA)
            al = Al(al_x, -AlConfig.ALTURA, AlConfig.LARGURA, AlConfig.ALTURA, AlConfig.VELOCIDADE, AlConfig.COR)
            self.als.append(al)
        self.inimigos_tempo_inc = max(200, self.inimigos_tempo_inc - 50)
        self.inimigos_quantidade = 0

    def adicionar_lulanos(self) -> None:
        numero_lulanos = random.randint(1, 7)
        for _ in range(numero_lulanos):
            lulanos_x = random.randint(0, JogoConfig.JANELA_LARGURA - LulanosConfig.LARGURA)
            lulanos = Lulanos(lulanos_x, -LulanosConfig.ALTURA, LulanosConfig.LARGURA, LulanosConfig.ALTURA, LulanosConfig.VELOCIDADE, (255, 255, 255))
            self.lulanos.append(lulanos)
        self.lulanos_tempo_inc = max(200, self.lulanos_tempo_inc - 50)
        self.lulanos_quantidade = 0


    def adicionar_nave_projeteis(self) -> None:
        """Adiciona projéteis que saem da nave (tiros)."""
        projetil_x = self.jogador.rect.x + (JogadorConfig.LARGURA / 2) - (JogadorConfig.PROJETIL_LARGURA / 2)
        projetil = Projetil(projetil_x, self.jogador.rect.y + JogadorConfig.PROJETIL_ALTURA, JogadorConfig.PROJETIL_LARGURA, JogadorConfig.PROJETIL_ALTURA, JogadorConfig.PROJETIL_VELOCIDADE, (253, 0, 24))
        self.nave_projeteis.append(projetil)
        self.nave_projetil_quantidade = 0


    def checar_colisoes_nave(self, inimigos: Objeto) -> None:
        """Checa se um dos projéteis (meteoro) atingiu a nave."""
        inimigos_para_remover = []
        for inimigo in inimigos:
            try:
                inimigo.mover()
            except ValueError as e:
                print(e)
            if inimigo.rect.y > JogoConfig.JANELA_ALTURA:
                inimigos_para_remover.append(inimigo)
            else:
                for hitbox in self.jogador.hitboxes:
                    if inimigo.rect.colliderect(hitbox):
                        inimigos_para_remover.append(inimigo)
                        self.colisao = True
                if self.colisao:
                    break
        
        for inimigo_para_remover in inimigos_para_remover:
            if inimigo_para_remover in inimigos:
                inimigos.remove(inimigo_para_remover)


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
                for invasor in self.als:
                    if invasor.rect.colliderect(nave_projetil):
                        projeteis_para_remover.append(invasor)

        for projetil in projeteis_para_remover:
            if projetil in self.als:
                self.als.remove(projetil)

        for nave_projetil in nave_projeteis_para_remover:
            if nave_projetil in self.nave_projeteis:
                self.nave_projeteis.remove(nave_projetil)


    def desenhar(self) -> None:
        """Desenha o jogo."""
        self.janela.fill((0, 0, 0))
        self.paralaxe.rolar()
        self.jogador.desenhar(self.janela)
        self.fonte_tempo = FONTE_TEMPO.render(f"Tempo: {round(self.tempo_decorrido)}s", 1, "white")
        for al in self.als:
            al.desenhar(self.janela)
        for lulanos in self.lulanos:
            lulanos.desenhar(self.janela)
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
            self.inimigos_quantidade += tick
            self.lulanos_quantidade += tick
            self.tempo_decorrido = time.time() - self.tempo_inicio

            if self.inimigos_quantidade > self.inimigos_tempo_inc:
                self.adicionar_al()

            # if self.lulanos_quantidade > self.lulanos_tempo_inc:
            #     self.adicionar_lulanos()

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
            self.checar_colisoes_nave(self.als)
            # self.checar_colisoes_nave(self.lulanos)
            self.checar_colisoes_nave_projeteis()

            if self.colisao:
                self.mostrar_mensagem_derrota()
                break

            self.desenhar()