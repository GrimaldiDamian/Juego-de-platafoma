import pygame
from config import *

class Game():
    
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((ancho,alto))
        pygame.display.set_caption("Plataformas")
        self.reloj = pygame.time.Clock()
        self.etapa = "level 1"
        self.runnig = True

    def manejo_evento(self):
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                self.runnig = False
            if eventos.type == pygame.KEYDOWN:
                if eventos.key == pygame.K_ESCAPE:
                    self.runnig = False
                elif eventos.key == pygame.K_SPACE:
                    arriba,_,_,_ =  jugador.colision_orientacion(jugador.nivel_actual)
                    if not jugador.en_salto and arriba:
                        jugador.posicion_inicial_salto = jugador.obtener_posicion_arriba(jugador.nivel_actual)
                        jugador.angulo = 0.1
                        jugador.en_salto = True

    def dibujar(self):
        if self.etapa == "level 1":
            lvl1.dibujar(self.screen)
            jugador.dibujar(self.screen)
        pygame.display.flip()

    def game(self):
        while self.runnig:
            self.manejo_evento()
            
            self.reloj.tick(60)

            jugador.movimiento(pygame.key.get_pressed())
            
            self.dibujar()