import pygame
import math
from config import *

class Player(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.posicion_inicial_nivel = {"1" : (0,584)}
        self.nivel = "1"
        x,y = self.posicion_inicial_nivel[self.nivel]
        self.corazones = pygame.image.load("assets/imagenes/corazones.png")
        self.corazones_sprite = self.sprite(self.corazones)
        self.rectangulo = pygame.Rect(x,y,16,24)
        self.angulo = 0
        self.vidas = 3
        self.coins = 0
        self.nivel_actual = None
        self.posicion_inicial_salto = 320
        self.en_salto = False

    def sprite(self,imagen):
        ancho,alto = imagen.get_size()
        cantidad_filas = alto // tamaño_sprite
        cantidad_columnas = ancho // tamaño_sprite
        sprites = []
        for fila in range(cantidad_filas):
            lista_sprite = []
            for columnas in range(cantidad_columnas):
                sprite = pygame.Rect(tamaño_sprite * columnas, tamaño_sprite * fila,tamaño_sprite,tamaño_sprite)
                lista_sprite.append(imagen.subsurface(sprite))
            sprites.append(lista_sprite)
        return sprites

    def movimiento(self,key):
        arriba, abajo, izquierda, derecha = self.colision_orientacion(self.nivel_actual)
        if key[pygame.K_d] and not derecha:
            self.rectangulo.x += velocidad
        if key[pygame.K_a] and not izquierda:
            self.rectangulo.x -= velocidad

        if self.en_salto:
            self.salto()
        else:
            if arriba:
                self.rectangulo.y = min(self.obtener_posicion_arriba(self.nivel_actual), self.rectangulo.y)
            else:
                self.rectangulo.y += gravedad

        self.rectangulo.x = max(0, min(self.rectangulo.x, ancho - self.rectangulo.width))
        self.rectangulo.y = min(alto - self.rectangulo.height, self.rectangulo.y)

        if derecha:
            self.rectangulo.x = min(self.obtener_posicion_derecha(self.nivel_actual), self.rectangulo.x)
        if izquierda:
            self.rectangulo.x = max(self.obtener_posicion_izquierda(self.nivel_actual), self.rectangulo.x)

    def salto(self):
        self.rectangulo.y = self.posicion_inicial_salto - (math.sin(self.angulo) * (tamaño_sprite*2.2))
        arriba,abajo,_,_ = self.colision_orientacion(self.nivel_actual)
        if self.angulo > 0:
            self.angulo += 0.1
        if self.angulo >= math.pi:
            self.angulo = 0
            self.en_salto = False
        elif self.angulo < math.pi/2:
            if abajo:
                self.angulo = math.pi - self.angulo
        else:
            if arriba:
                self.angulo = 0
                self.en_salto = False

    def colision_orientacion(self, nivel):
        arriba, abajo, izquierda, derecha = False, False, False, False

        for suelo in nivel.suelo_colision["solidos"]:
            x, y = suelo

            # Detectar si el jugador está justo encima del bloque
            if (self.rectangulo.y + self.rectangulo.height >= y and 
                self.rectangulo.y + self.rectangulo.height <= y + gravedad) and (
                self.rectangulo.x + self.rectangulo.width > x and 
                self.rectangulo.x < x + tamaño_sprite):
                arriba = True

            # Detectar si el jugador está justo debajo del bloque
            if (self.rectangulo.y <= y + tamaño_sprite and 
                self.rectangulo.y >= y + tamaño_sprite - gravedad) and (
                self.rectangulo.x + self.rectangulo.width > x and 
                self.rectangulo.x < x + tamaño_sprite):
                abajo = True
            
            # Detectar colisiones a la izquierda
            if (self.rectangulo.x <= x + tamaño_sprite and 
                self.rectangulo.x >= x + tamaño_sprite - velocidad) and (
                self.rectangulo.y + self.rectangulo.height > y and 
                self.rectangulo.y < y + tamaño_sprite):
                izquierda = True

            # Detectar colisiones a la derecha
            if (self.rectangulo.x + self.rectangulo.width >= x and 
                self.rectangulo.x + self.rectangulo.width <= x + velocidad) and (
                self.rectangulo.y + self.rectangulo.height > y and 
                self.rectangulo.y < y + tamaño_sprite):
                derecha = True

        return arriba, abajo, izquierda, derecha

    def obtener_posicion_arriba(self,nivel):
        for suelo in nivel.suelo_colision["solidos"]:
            x,y = suelo
            if (self.rectangulo.y + self.rectangulo.height >= y and 
                self.rectangulo.y + self.rectangulo.height <= y + gravedad) and (
                self.rectangulo.x + self.rectangulo.width > x and 
                self.rectangulo.x < x + tamaño_sprite):
                return y - self.rectangulo.height
        return self.rectangulo.y

    def obtener_posicion_izquierda(self, nivel):
        for suelo in nivel.suelo_colision["solidos"]:
            x, y = suelo
            if (self.rectangulo.x <= x + tamaño_sprite and 
                self.rectangulo.x >= x + tamaño_sprite - velocidad) and (
                self.rectangulo.y + self.rectangulo.height > y and 
                self.rectangulo.y < y + tamaño_sprite):
                return x + tamaño_sprite
        return self.rectangulo.x

    def obtener_posicion_derecha(self, nivel):
        for suelo in nivel.suelo_colision["solidos"]:
            x, y = suelo
            if (self.rectangulo.x + self.rectangulo.width >= x and 
                self.rectangulo.x + self.rectangulo.width <= x + velocidad) and (
                self.rectangulo.y + self.rectangulo.height > y and 
                self.rectangulo.y < y + tamaño_sprite):
                return x - self.rectangulo.width
        return self.rectangulo.x

    def colision_monedas(self,nivel):
        for monedas in nivel.colision_monedas["monedas"]:
            x,y = monedas
            rect = pygame.rect.Rect(x,y,tamaño_sprite,tamaño_sprite)
            if self.rectangulo.colliderect(rect):
                self.coins +=5
                nivel.colision_monedas["monedas"].remove((x,y))
                matriz_x = x // tamaño_sprite
                matriz_y = y // tamaño_sprite
                nivel.monedas[matriz_y][matriz_x] = -1

    def resetear_nivel(self):
        x,y = self.posicion_inicial_nivel[self.nivel]
        self.rectangulo.x = x
        self.rectangulo.y = y

    def perder_vida(self):
        if self.rectangulo.y == alto - self.rectangulo.height:
            self.vidas -=1
            self.resetear_nivel()

    def game_over(self):
        return self.vidas == 0

    def dibujar_corazones(self,screen):
        tamaño_sprite = self.corazones_sprite[0][0].get_width()
        espacio = tamaño_sprite * 1.2

        for i in range(3):
            if i < self.vidas:
                sprite = self.corazones_sprite[0][1]
            else:
                sprite = self.corazones_sprite[0][0]
            screen.blit(sprite, (i * espacio, 0))
    
    def dibujar_coins(self,screen,texto,fuente):
        texto = fuente.render(texto,True,(255,255,255))
        screen.blit(texto,(ancho//2, 0))

    def dibujar(self,screen,fuente):
        pygame.draw.rect(screen,"red",self.rectangulo)
        self.dibujar_corazones(screen)
        self.dibujar_coins(screen,f"Puntos: {self.coins}",fuente)