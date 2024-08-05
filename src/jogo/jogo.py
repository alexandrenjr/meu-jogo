import pygame
import time
import random
from jogo.jogo_config import JogoConfig
from jogo.paralaxe import Paralaxe
from jogador.jogador_config import JogadorConfig
from jogador.jogador import Jogador
from jogador.projetil import Projetil
from inimigo.inimigos_config import AlConfig, LulanosConfig
from inimigo.inimigos import Al, Lulanos
from utils.helpers import *
from utils.objeto import Objeto

class Jogo:
    def __init__(self) -> None:
        """Inicialização do Pygame e configurações gerais."""
        pygame.init()
        self.configurar_tela()
        self.configurar_plano_fundo()
        self.configurar_sons()
        self.inicializar_objetos_jogo()
        self.inicializar_estado_jogo()


    def configurar_tela(self) -> None:
        """Configura as propriedades da tela do jogo."""
        dimensoes_sistema_atual = pygame.display.Info()
        self.sistema_largura, self.sistema_altura = dimensoes_sistema_atual.current_w, dimensoes_sistema_atual.current_h
        self.janela = pygame.display.set_mode((self.sistema_largura, self.sistema_altura), pygame.FULLSCREEN | pygame.RESIZABLE)
        self.largura, self.altura = JogoConfig.JANELA_LARGURA, JogoConfig.JANELA_ALTURA
        self.superficie = pygame.Surface((self.largura, self.altura))
        pygame.display.set_caption("Meu jogo")


    def configurar_plano_fundo(self) -> None:
        """Carrega e configura o plano de fundo do jogo."""
        camadas_imagens_caminhos = [buscar_caminho_arquivo("layer1.png", "assets/images")]
        camadas_imagens_velocidades = [1, 3]
        self.paralaxe = Paralaxe(self.superficie, camadas_imagens_caminhos, camadas_imagens_velocidades)


    # def transicao_tela(self, ) -> None:
    #     self.superficie_transicao = pygame.Surface(su)


    def configurar_sons(self) -> None:
        """Carrega e inicia os sons do jogo."""
        pygame.mixer.init()
        # self.musica_fundo = pygame.mixer.Sound(buscar_caminho_arquivo("8 Bit Eye of the Tiger - Survivor.wav", "assets/sounds"))
        self.som_tiro = pygame.mixer.Sound(buscar_caminho_arquivo("mixkit-short-laser-gun-shot-1670.wav", "assets/sounds"))
        self.som_tiro.set_volume(0.3)
        self.som_derrota = pygame.mixer.Sound(buscar_caminho_arquivo("mixkit-arcade-space-shooter-dead-notification-272.wav", "assets/sounds"))
        self.som_derrota.set_volume(0.3)
        self.som_inimigo_abatido = pygame.mixer.Sound(buscar_caminho_arquivo("mixkit-space-coin-win-notification-271.wav", "assets/sounds"))
        self.som_inimigo_abatido.set_volume(0.3)


    def inicializar_objetos_jogo(self) -> None:
        """Inicializa os objetos e entidades do jogo."""
        self.jogador = Jogador(JogadorConfig)
        self.als = []
        self.lulanos = []
        self.nave_projeteis = []


    def inicializar_estado_jogo(self) -> None:
        """Inicializa as variáveis de estado do jogo."""
        self.relogio = pygame.time.Clock()
        self.pontos = 0
        self.texto_tempo = pygame.font.Font(None, 30)
        self.texto_derrota = pygame.font.Font(None, 30)
        self.texto_pontos = pygame.font.Font(None, 30)
        self.tempo_inicio = time.time()
        self.tempo_decorrido = 0
        self.al_tempo_inc = 2000
        self.al_quantidade = 0
        self.lulanos_tempo_inc = 3000
        self.lulanos_quantidade = 0
        self.nave_projetil_tempo = 150
        self.nave_projetil_quantidade = 0
        self.colisao = False


    def adicionar_al(self) -> None:
        """Adiciona um inimigo tipo Al."""
        numero_als = random.randint(1, 4)
        for _ in range(numero_als):
            al_x = random.randint(0, JogoConfig.JANELA_LARGURA - AlConfig.LARGURA)
            al = Al(al_x, -AlConfig.ALTURA, AlConfig.LARGURA, AlConfig.ALTURA, AlConfig.VELOCIDADE, AlConfig.COR)
            self.als.append(al)
        self.al_tempo_inc = max(200, self.al_tempo_inc - 50)
        self.al_quantidade = 0

    def adicionar_lulanos(self) -> None:
        """Adiciona um inimigo tipo Lulanos."""
        numero_lulanos = random.randint(1, 3)
        for _ in range(numero_lulanos):
            lulanos_x = random.randint(0, JogoConfig.JANELA_LARGURA - LulanosConfig.LARGURA)
            cores = [(169, 208, 253), (38, 183, 116), (230, 215, 162)]
            lulanos = Lulanos(lulanos_x, -LulanosConfig.ALTURA, LulanosConfig.LARGURA, LulanosConfig.ALTURA, LulanosConfig.VELOCIDADE, cores)
            self.lulanos.append(lulanos)
        self.lulanos_tempo_inc = max(200, self.lulanos_tempo_inc - 50)
        self.lulanos_quantidade = 0


    def adicionar_nave_projeteis(self) -> None:
        """Adiciona projéteis disparados pela nave."""
        projetil_x = self.jogador.rect.x + (JogadorConfig.LARGURA / 2) - (JogadorConfig.PROJETIL_LARGURA / 2)
        projetil = Projetil(projetil_x, self.jogador.rect.y + JogadorConfig.PROJETIL_ALTURA, JogadorConfig.PROJETIL_LARGURA, JogadorConfig.PROJETIL_ALTURA, JogadorConfig.PROJETIL_VELOCIDADE, (253, 0, 24))
        self.nave_projeteis.append(projetil)
        self.nave_projetil_quantidade = 0
        self.som_tiro.play()


    def checar_colisoes_nave(self, inimigos: Objeto) -> None:
        """Checa colisões entre a nave e os inimigos."""
        inimigos_para_remover = []
        for inimigo in inimigos:
            try:
                inimigo.mover()
            except ValueError as e:
                print(e)
            if inimigo.rect.y > JogoConfig.JANELA_ALTURA:
                inimigos_para_remover.append(inimigo)
            else:
                for inimigo_hitbox in inimigo.hitboxes:
                    for hitbox in self.jogador.hitboxes:
                        if inimigo_hitbox.colliderect(hitbox):
                            inimigos_para_remover.append(inimigo)
                            self.colisao = True
                    if self.colisao:
                        break
        
        for inimigo_para_remover in inimigos_para_remover:
            if inimigo_para_remover in inimigos:
                inimigos.remove(inimigo_para_remover)


    def checar_colisoes_nave_projeteis(self) -> None:
        """Checa colisões entre os projéteis da nave e os inimigos."""
        inimigos_para_remover = []
        nave_projeteis_para_remover = []
        
        for nave_projetil in self.nave_projeteis:
            try:
                nave_projetil.mover("cima")
            except ValueError as e:
                print(e)
            
            if nave_projetil.rect.y < 0:
                nave_projeteis_para_remover.append(nave_projetil)
            else:
                for al in self.als:
                    if al.rect.colliderect(nave_projetil):
                        al.desenhar(self.janela, True)
                        al.atingido = True
                        inimigos_para_remover.append(al)
                        self.pontos += 1

                for lulano in self.lulanos:
                    if lulano.rect.colliderect(nave_projetil):
                        inimigos_para_remover.append(lulano)
                        self.pontos += 1

        for inimigo in inimigos_para_remover:
            if inimigo in self.als:
                self.als.remove(inimigo)
                self.som_inimigo_abatido.play()
            elif inimigo in self.lulanos:
                self.lulanos.remove(inimigo)
                self.som_inimigo_abatido.play()

        for nave_projetil in nave_projeteis_para_remover:
            if nave_projetil in self.nave_projeteis:
                self.nave_projeteis.remove(nave_projetil)


    def desenhar(self) -> None:
        """Desenha o jogo."""
        self.superficie.fill((0, 0, 0))
        self.janela.fill((0, 0, 0))
        self.paralaxe.rolar()
        self.jogador.desenhar(self.superficie)
        for al in self.als:
            al.desenhar(self.superficie)
        for lulanos in self.lulanos:
            lulanos.desenhar(self.superficie)
        for nave_projetil in self.nave_projeteis:
            nave_projetil.desenhar(self.superficie)
        
        self.janela.blit(pygame.transform.scale(self.superficie, self.janela.get_size()), (0, 0))
        
        self.texto_tempo = TEXTO_TEMPO.render(f"Tempo: {round(self.tempo_decorrido)}s", 1, "white")
        self.texto_pontos = TEXTO_PONTOS.render(f"Pontos: {self.pontos}", 1, "white")
        texto_tempo_coordenadas = (10, 10)
        texto_pontos_coordenadas = (centralizar_x(self.texto_pontos.get_width(), self.janela.get_width()), 10)
        self.janela.blit(self.texto_tempo, texto_tempo_coordenadas)
        self.janela.blit(self.texto_pontos, texto_pontos_coordenadas)
        
        pygame.display.flip()


    def mostrar_mensagem_derrota(self) -> None:
        """Mostra a mensagem de derrota."""
        # self.musica_fundo.stop()
        self.som_derrota.play()
        self.texto_derrota = TEXTO_DERROTA.render("Você perdeu!", 1, "white")
        x_medio_janela = (self.texto_derrota.get_width(), self.texto_derrota.get_height())
        y_medio_janela = (self.sistema_largura, self.sistema_altura)
        texto_derrota_coordenadas = centralizar(x_medio_janela, y_medio_janela)
        self.janela.blit(self.texto_derrota, texto_derrota_coordenadas)
        pygame.display.update()
        pygame.time.delay(3000)


    def executar(self) -> None:
        """Execução do jogo."""
        # self.musica_fundo.play(-1)
        while True:
            tick = self.relogio.tick(60)
            self.nave_projetil_quantidade += tick
            self.al_quantidade += tick
            self.lulanos_quantidade += tick
            self.tempo_decorrido = time.time() - self.tempo_inicio

            if self.al_quantidade > self.al_tempo_inc:
                self.adicionar_al()

            if self.lulanos_quantidade > self.lulanos_tempo_inc:
                self.adicionar_lulanos()

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
            self.checar_colisoes_nave(self.lulanos)
            self.checar_colisoes_nave_projeteis()

            if self.colisao:
                self.mostrar_mensagem_derrota()
                break

            self.desenhar()