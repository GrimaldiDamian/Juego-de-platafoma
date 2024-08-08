import pygame
from config import *
import src.game.utils.utilidades as utilidades

class Boton():
    
    def __init__(self,posicion_x,posicion_y, valor):
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.valor = valor

    def renderizar_texto(self,screen,fuente):
        ancho_palabra, _ = fuente.size(self.valor)
        texto = fuente.render(self.valor,True,"black")
        posicion = self.posicion_x + ((ancho_boton - 10 ) / 2)- ancho_palabra//2, self.posicion_y + 5 + ((alto_boton - 10 ) /2 - (tamaño_letras / 2))
        screen.blit(texto,posicion)
    
    def comprobacion(self,mouse):
        mouse_posicion = mouse.get_pos()
        if (ancho_boton + self.posicion_x >= mouse_posicion[0] >= self.posicion_x) and (alto_boton + self.posicion_y >= mouse_posicion[1] >= self.posicion_y):
            return True
        return False

    def accion(self,mouse,click,screen):
        if self.comprobacion(mouse):
            if click == 1:
                if self.valor == "JUGAR":
                    utilidades.jugador.nivel = "1"
                    utilidades.jugador.resetear_variables()
                    utilidades.jugador.vidas = 3
                    utilidades.jugador.coins = 0
                    utilidades.jugador.nivel_actual = utilidades.obtener_nivel_actual()
                    screen.etapa = "nivel"
                elif self.valor == "SALIR":
                    screen.runnig = False

    def dibujar(self,screen,fuente,mouse):

        pygame.draw.rect(screen, "white", (self.posicion_x,self.posicion_y,ancho_boton,alto_boton))

        if self.comprobacion(mouse):
            pygame.draw.rect(screen, color_activo, (self.posicion_x+5,self.posicion_y+5,ancho_boton - 10,alto_boton - 10))

        else:
            pygame.draw.rect(screen, color_inactivo, (self.posicion_x+5,self.posicion_y+5,ancho_boton - 10,alto_boton - 10))

        self.renderizar_texto(screen,fuente)