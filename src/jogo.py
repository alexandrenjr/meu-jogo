import pygame
import time
import random
from jogador import Jogador
from projetil import Projetil
from util import *
from config import *

class Jogo:
    def __init__(self) -> None:
        """Inicialização do Pygame e configurações gerais."""
        pygame.font.init()
        pygame.display.set_caption("Meu jogo")
        self.janela = pygame.display.set_mode((Config.jogo.JANELA_LARGURA, Config.jogo.JANELA_ALTURA))
        self.plano_de_fundo = pygame.transform.scale(pygame.image.load(buscar_path_imagem()), (Config.jogo.JANELA_LARGURA, Config.jogo.JANELA_ALTURA))
        self.jogador = Jogador(Config)
        self.relogio = pygame.time.Clock()
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
        """Adiciona os projéteis que vem de cima."""
        for indice in obter_cor_aleatoria(random.randint(1, 4), Config.cores.PROJETEIS):
                projetil_x = random.randint(0, Config.jogo.JANELA_LARGURA - Config.projetil.LARGURA)
                cor = Config.cores.PROJETEIS.get(indice, "red")
                projetil = Projetil(projetil_x, -Config.projetil.ALTURA, Config.projetil.LARGURA, Config.projetil.ALTURA, Config.projetil.VELOCIDADE, cor)
                self.projeteis.append(projetil)
        self.projetil_tempo_inc = max(200, self.projetil_tempo_inc - 50)
        self.projetil_quantidade = 0


    def adicionar_nave_projeteis(self) -> None:
        """Adiciona projéteis que saem da nave (tiros)."""
        projetil_x = self.jogador.rect.x + (Config.jogador.LARGURA / 2) - (Config.jogador.PROJETIL_LARGURA / 2)
        projetil = Projetil(projetil_x, self.jogador.rect.y + Config.jogador.PROJETIL_ALTURA, Config.jogador.PROJETIL_LARGURA, Config.jogador.PROJETIL_ALTURA, Config.jogador.VELOCIDADE, "orange")
        self.nave_projeteis.append(projetil)
        self.nave_projetil_quantidade = 0


    def checar_colisoes(self) -> None:
        """Checa se um dos projéteis (meteoro) atingiu a nave."""
        projeteis_para_remover = []
        for projetil in self.projeteis:
            try:
                projetil.mover("baixo")
            except ValueError as e:
                print(e)
            if projetil.rect.y > Config.jogo.JANELA_ALTURA:
                projeteis_para_remover.append(projetil)
            else:
                for hitbox in self.jogador.hitboxes:
                    if projetil.rect.colliderect(hitbox):
                        projeteis_para_remover.append(projetil)
                        self.colisao = True
                
                if self.colisao:
                    break;
        
        for projetil in projeteis_para_remover:
            if projetil in self.projeteis:
                self.projeteis.remove(projetil)

        nave_projeteis_para_remover = []
        for nave_projetil in self.nave_projeteis[:]:
            try:
                nave_projetil.mover("cima")
            except ValueError as e:
                print(e)
            if nave_projetil.rect.y < 0:
                nave_projeteis_para_remover.append(nave_projetil)

        for nave_projetil in nave_projeteis_para_remover:
            if nave_projetil in self.nave_projeteis:
                self.nave_projeteis.remove(nave_projetil)


    def desenhar(self) -> None:
        """Desenha o jogo."""
        self.janela.fill((0, 0, 0))
        self.janela.blit(self.plano_de_fundo, (0, 0))
        self.jogador.desenhar(self.janela)
        self.fonte_tempo = FONTE_TEMPO.render(f"Tempo: {round(self.tempo_decorrido)}s", 1, "white")
        for projetil in self.projeteis:
            projetil.desenhar(self.janela)
        for nave_projetil in self.nave_projeteis:
            nave_projetil.desenhar(self.janela)
        pygame.display.update()


    def mostrar_mensagem_derrota(self) -> None:
        """Mostra a mensagem de derrota."""
        texto_derrota = FONTE_DERROTA.render("Você perdeu!", 1, "white")
        self.janela.blit(texto_derrota, centralizar((texto_derrota.get_width(), texto_derrota.get_height()), (Config.jogo.JANELA_LARGURA, Config.jogo.JANELA_ALTURA)))
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
            self.checar_colisoes()

            if self.colisao:
                self.mostrar_mensagem_derrota()
                break

            self.desenhar()