import pygame
from config import *
from src.game.utils.utilidades import *

class Game():
    
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((ancho,alto),pygame.FULLSCREEN)
        pygame.display.set_caption("Plataformas")
        self.reloj = pygame.time.Clock()
        self.etapa = "menu"
        self.runnig = True
        self.fuente = pygame.font.SysFont('Times New Roman', tamaño_letras)

    def manejo_evento(self):
        """
        Se encarga de manejar los eventos del juego
        """
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                self.runnig = False
            #aca se encarga de manejar si se ha precionado una vez las teclas
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
                        #Aca verifica si el jugador esta arriba de un bloque para poder saltar
                        arriba,_,_,_ =  jugador.colision_orientacion(jugador.nivel_actual.suelo_colision,"solidos")
                        if not jugador.en_salto and arriba:
                            jugador.posicion_inicial_salto = jugador.obtener_posicion(jugador.nivel_actual,"arriba")
                            # jugador.angulo = 0.1
                            jugador.tiempo = 0
                            jugador.en_salto = True
                #Este if, se encarga de ver si esta en la puerta y si toca la e, cambia de nivel.
                if self.etapa == "nivel":
                    if jugador.colision_puertas(jugador.nivel_actual):
                        if eventos.key == pygame.K_e:
                            siguiente_nivel = int(jugador.nivel)+1
                            if siguiente_nivel <= total_niveles:
                                jugador.nivel = f"{siguiente_nivel}"
                                jugador.resetear_variables()
                                jugador.nivel_actual = obtener_nivel_actual()
                            else:
                                self.etapa = "menu"
            if eventos.type == pygame.MOUSEBUTTONDOWN:
                #sirve para el menu, dependiendo a que boton se este tocando, va a ejercer una accion u otra
                click = eventos.button
                if self.etapa == "menu":
                    self.funcion_botones(click,0,2)
                elif self.etapa == "pause":
                    self.funcion_botones(click,1,3)

    def funcion_botones(self,click,inicio,fin):
        for boton in menu.botones[inicio:fin]:
            boton.accion(pygame.mouse,click,self)

    def dibujar(self):
        """
        Se encarga de dibujar los escenarios, ya sea pausa, menu, o los niveles
        """
        if self.etapa not in ["menu","game_over","pause"]:
            jugador.nivel_actual.dibujar(self.screen)
            jugador.dibujar(self.screen,self.fuente)
            jugador.interaccion_puerta(self.screen,self.fuente)
        elif self.etapa in ["menu","pause"]:
            menu.dibujar(self,self.fuente,pygame.mouse)

        pygame.display.flip()

    def mecanica_jugador(self):
        """
        Se encarga de los movimientos, colisiones y del game over del personaje
        """
        if self.etapa not in ["menu","game_over","pause"]:
            jugador.movimiento(pygame.key.get_pressed())

            if jugador.game_over():
                self.etapa = "menu"

            jugador.colision_monedas(jugador.nivel_actual)
            jugador.perder_vida()

    def game(self):
        """
        Bucle principal del juego
        """
        while self.runnig:
            self.manejo_evento()
            
            self.reloj.tick(60)

            self.mecanica_jugador()
            
            self.dibujar()