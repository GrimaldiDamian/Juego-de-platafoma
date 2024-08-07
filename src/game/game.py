import pygame
from config import *
from src.game.utils.utilidades import *

class Game():
    
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((ancho,alto),pygame.FULLSCREEN)
        pygame.display.set_caption("Plataformas")
        self.reloj = pygame.time.Clock()
        self.etapa = "nivel"
        self.runnig = True
        self.fuente = pygame.font.SysFont('Times New Roman', tamaño_letras)

    def manejo_evento(self):
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                self.runnig = False
            if eventos.type == pygame.KEYDOWN:
                if eventos.key == pygame.K_ESCAPE:
                    if self.etapa == "menu":
                        self.runnig = False
                    elif self.etapa == "pause":
                        self.etapa = "nivel"
                    else:
                        self.etapa = "pause"
                elif eventos.key == pygame.K_SPACE:
                    if self.etapa not in ["menu","game_over","pause"]:
                        arriba,_,_,_ =  jugador.colision_orientacion(jugador.nivel_actual.suelo_colision,"solidos")
                        if not jugador.en_salto and arriba:
                            jugador.posicion_inicial_salto = jugador.obtener_posicion_arriba(jugador.nivel_actual)
                            jugador.angulo = 0.1
                            jugador.en_salto = True
                if jugador.colision_puertas(jugador.nivel_actual):
                    if eventos.key == pygame.K_e:
                        siguiente_nivel = int(jugador.nivel)+1
                        if siguiente_nivel <= total_niveles:
                            jugador.nivel = f"{siguiente_nivel}"
                            jugador.resetear_variables()
                        else:
                            self.etapa = "menu"

    def dibujar(self):
        if self.etapa not in ["menu","game_over","pause"]:
            jugador.nivel_actual.dibujar(self.screen)
            jugador.dibujar(self.screen,self.fuente)
            jugador.siguiente_nivel(self.screen,self.fuente)

        pygame.display.flip()

    def mecanica_jugador(self):
        if self.etapa not in ["menu","game_over","pause"]:
            jugador.movimiento(pygame.key.get_pressed())

            # if jugador.game_over():
            #     self.etapa = "menu"

            jugador.colision_monedas(jugador.nivel_actual)
            jugador.perder_vida()

    def game(self):
        while self.runnig:
            self.manejo_evento()
            
            self.reloj.tick(60)

            self.mecanica_jugador()
            
            self.dibujar()