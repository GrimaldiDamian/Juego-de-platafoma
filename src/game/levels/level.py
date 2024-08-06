import pygame
import csv
from config import *

class Niveles(pygame.sprite.Sprite):

    def __init__(self, nombre_mapa,monedas,fondo) -> None:
        super().__init__()
        self.mapa_nivel = nombre_mapa
        self.mapa_monedas = monedas
        self.suelo = self.abrir_archivo(self.mapa_nivel)
        self.monedas = self.abrir_archivo(self.mapa_monedas)
        self.imagen = pygame.image.load("assets/imagenes/sprite mapa.png")
        self.fondo = pygame.image.load(fondo)
        self.sprites = self.carga_sprites()
        self.suelo_colision = self.bloques_colision(self.suelo,"solidos")
        self.colision_monedas = self.bloques_colision(self.monedas,"monedas")

    def bloques_colision(self,archivo,tipo_objeto):
        bloques_con_colision = {tipo_objeto: []}
        for y,filas in enumerate(archivo):
            for x,bloque in enumerate(filas):
                if bloque in ["0","1","2","3","10","11","12","13","20","21","22","23","30","31","32","33"]:
                    posiciones = (x*tamaño_sprite,y*tamaño_sprite)
                    bloques_con_colision[tipo_objeto].append(posiciones)
                elif bloque in ["4"]:
                    posiciones = (x*tamaño_sprite,y*tamaño_sprite)
                    bloques_con_colision[tipo_objeto].append(posiciones)
        return bloques_con_colision

    def carga_sprites(self):
        """
        Se encarga de separar los sprites del nivel, y los guarda como tipo sprite
        """
        sprites = []
        for filas in range(10):
            lista_sprite = []
            for columnas in range(10):
                sprite = pygame.Rect(tamaño_sprite * columnas, tamaño_sprite * filas,tamaño_sprite,tamaño_sprite)
                lista_sprite.append(self.imagen.subsurface(sprite))
            sprites.append(lista_sprite)
        return sprites

    def abrir_archivo(self,nombre_archivo):
        filas = []
        with open(nombre_archivo, newline= "") as file:
            archivo = csv.reader(file,delimiter=",")
            for fila in archivo:
                filas.append(fila)

        return filas

    def dibujar_mapa(self,screen,archivo):
        """
        Esta funcion sirve para dibujar todos los elementos del mapa, a traves de una matriz.
        """
        y = 0
        for filas in archivo:
            x = 0
            for tiles in filas:
                if tiles !="-1":
                    tile_index = int(tiles)
                    sprite_row = tile_index // 10
                    sprite_col = tile_index % 10
                    screen.blit(self.sprites[sprite_row][sprite_col], (x, y))
                x+=tamaño_sprite
            y+=tamaño_sprite

    def dibujar(self,screen):
        screen.blit(self.fondo,(0,0))
        self.dibujar_mapa(screen,self.suelo)
        self.dibujar_mapa(screen,self.monedas)