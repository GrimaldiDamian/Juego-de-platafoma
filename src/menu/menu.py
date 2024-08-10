import pygame
from config import *
from src.menu.boton import *

class Menu():
    def __init__(self) -> None:
        self.fondo = pygame.image.load("./assets/imagenes/MENU.png")
        self.opciones = [("JUGAR", (ancho//2 - ancho_boton//2, alto//2 - alto_boton//2 - 50)),
                         ("SALIR", (ancho//2 - ancho_boton//2, alto//2 - alto_boton//2 + 50)),
                         ("REANUDAR", (ancho//2 - ancho_boton//2, alto//2 - alto_boton//2 - 50))]
        self.botones = []
        for texto, posicion in self.opciones:
            x,y = posicion
            boton = Boton(x,y,texto)
            self.botones.append(boton)

    def dibujar_botones(self,screen,fuente,mouse,inicio,fin):
        for botones in self.botones[inicio:fin]:
            botones.dibujar(screen.screen,fuente,mouse)

    def dibujar(self, screen, fuente, mouse):
        screen.screen.blit(self.fondo, (0, 0))
        if screen.etapa == "menu":
            self.dibujar_botones(screen,fuente,mouse,0,2)
        else:
            self.dibujar_botones(screen,fuente,mouse,1,3)