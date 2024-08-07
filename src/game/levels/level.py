import pygame
import csv
from config import *

class Niveles(pygame.sprite.Sprite):

    def __init__(self, nombre_mapa,monedas,puertas,fondo) -> None:
        super().__init__()
        self.x = 0
        self.x_relativa = 0

        #archivos necesarios
        self.mapa_nivel = nombre_mapa
        self.mapa_monedas = monedas
        self.mapa_puertas = puertas
        self.suelo = self.abrir_archivo(self.mapa_nivel)
        self.monedas = self.abrir_archivo(self.mapa_monedas)
        self.puertas = self.abrir_archivo(self.mapa_puertas)

        #sprites
        self.imagen = pygame.image.load("assets/imagenes/sprite mapa.png")
        self.fondo = pygame.image.load(fondo)
        self.sprites = self.carga_sprites()

        #colisiones
        self.suelo_colision = self.bloques_colision(self.suelo,"solidos")
        self.colision_monedas = self.bloques_colision(self.monedas,"monedas")
        self.colision_puertas = self.bloques_colision(self.puertas,"puertas")

    def bloques_colision(self,archivo,tipo_objeto):
        bloques_con_colision = {tipo_objeto: []}
        for y,filas in enumerate(archivo):
            for x,bloque in enumerate(filas):
                if bloque !="-1":
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

    def dibujar_elementos_nivel(self,screen,archivo):
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
        self.x_relativa = self.x % ancho
        screen.blit(self.fondo,(self.x_relativa - ancho,0))
        self.x -=1
        if self.x_relativa < ancho:
            screen.blit(self.fondo,(self.x_relativa,0))
        self.dibujar_elementos_nivel(screen,self.suelo)
        self.dibujar_elementos_nivel(screen,self.monedas)
        self.dibujar_elementos_nivel(screen,self.puertas)