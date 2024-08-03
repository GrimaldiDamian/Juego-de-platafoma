import pygame
import csv

class Niveles(pygame.sprite.Sprite):

    def __init__(self,nombre_mapa,fondo) -> None:
        self.mapa_nivel = nombre_mapa
        self.archivo = self.abrir_archivo()
        self.imagen = pygame.image.load("assets/imagenes/sprite mapa.png")
        self.fondo = pygame.image.load(fondo)
        self.imagen = self.sprite.subsurface(self.sprite.get_clip())

    def carga_sprites(self):
        pass

    def abrir_archivo(self):

        filas = []
        with open(self.mapa_nivel, newline= "") as file:
            archivo = csv.reader(file,delimiter=",")
            for fila in archivo:
                filas.append(fila)

        return filas

    def dibujar(self,screen):
        screen.blit(self.fondo,(0,0))