import pygame
import csv

class Niveles(pygame.sprite.Sprite):

    def __init__(self, nombre_mapa,fondo) -> None:
        super().__init__()
        self.mapa_nivel = nombre_mapa
        self.suelo = self.abrir_archivo()
        self.imagen = pygame.image.load("assets/imagenes/sprite mapa.png")
        self.fondo = pygame.image.load(fondo)
        self.sprites = self.carga_sprites()
        self.suelo_colision = self.bloques_colision(self.suelo)

    def bloques_colision(self,archivo):
        bloques_con_colision = {"solidos": [], "monedas": [], "llaves": [], "puerta": []}
        for y,filas in enumerate(archivo):
            for x,bloque in enumerate(filas):
                if int(bloque) in [0,1,2,3,10,11,12,13,20,21,22,23,30,31,32,33]:
                    rectangulo = pygame.Rect(x*32,y*32,32,32)
                    bloques_con_colision["solidos"].append(rectangulo)
        return bloques_con_colision

    def carga_sprites(self):
        """
        Se encarga de separar los sprites del nivel, y los guarda como tipo sprite
        """
        sprites = []
        for filas in range(10):
            lista_sprite = []
            for columnas in range(10):
                sprite = pygame.Rect(32 * columnas, 32 * filas,32,32)
                lista_sprite.append(self.imagen.subsurface(sprite))
            sprites.append(lista_sprite)
        return sprites

    def abrir_archivo(self):
        filas = []
        with open(self.mapa_nivel, newline= "") as file:
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
                tile_index = int(tiles)
                sprite_row = tile_index // 10
                sprite_col = tile_index % 10
                screen.blit(self.sprites[sprite_row][sprite_col], (x, y))
                x+=32
            y+=32

    def dibujar(self,screen):
        screen.blit(self.fondo,(0,0))
        self.dibujar_mapa(screen,self.suelo)