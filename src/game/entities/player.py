import pygame
import math
from config import *

class Player(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()

        #nivel inicial
        self.nivel = "1"
        
        #carga de imagenes
        self.corazones = pygame.image.load("./assets/imagenes/corazones.png")
        self.personaje = pygame.image.load("./assets/imagenes/SPRITE PERSONAJE.png")
        self.en_movimiento = False
        self.direccion = 0
        self.sprite_actual = 0

        #carga de sprite
        self.corazones_sprite = self.sprite(self.corazones)
        self.personaje_sprite = self.sprite(self.personaje)

        #bitbox
        x,y = posicion_inicial_nivel[self.nivel]
        self.rectangulo = pygame.Rect(x,y,ancho_jugador,alto_jugador)

        self.angulo = 0
        self.tiempo = 0
        self.vidas = 3
        self.coins = 0
        self.nivel_actual = None
        self.posicion_inicial_salto = 320
        self.en_salto = False

    def sprite(self,imagen):
        """
        Obtiene los sprite necesarios para ejecutar la animacion del jugador
        """
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
        """
        Cumple la funcion de que el personaje se mueva en todo el mapa
        """
        arriba, _, izquierda, derecha = self.colision_orientacion(self.nivel_actual.suelo_colision,"solidos")
        self.en_movimiento = False
        if key[pygame.K_d] and not derecha:
            self.rectangulo.x += velocidad
            self.direccion = 0
            self.sprite_actual += 1
            self.en_movimiento = True
        if key[pygame.K_a] and not izquierda:
            self.rectangulo.x -= velocidad
            self.direccion = 1
            self.sprite_actual += 1
            self.en_movimiento = True

        if self.en_salto:
            self.salto()
        else:
            if arriba:
                self.rectangulo.y = min(self.obtener_posicion(self.nivel_actual,"arriba"), self.rectangulo.y)
            else:
                self.rectangulo.y += gravedad

        self.rectangulo.x = max(0, min(self.rectangulo.x, ancho - self.rectangulo.width))
        self.rectangulo.y = min(alto - self.rectangulo.height, self.rectangulo.y)

        if derecha:
            self.rectangulo.x = min(self.obtener_posicion(self.nivel_actual,"derecha"), self.rectangulo.x)
        if izquierda:
            self.rectangulo.x = max(self.obtener_posicion(self.nivel_actual,"izquierda"), self.rectangulo.x)

    # def salto(self):
    #     """
    #     Mecanica de salto
    #     """
    #     self.rectangulo.y = self.posicion_inicial_salto - (math.sin(self.angulo) * (tamaño_sprite*2.2))
    #     arriba,abajo,_,_ = self.colision_orientacion(self.nivel_actual.suelo_colision,"solidos")
    #     if self.angulo > 0:
    #         self.angulo += 0.1
    #     if self.angulo >= math.pi:
    #         self.angulo = 0
    #         self.en_salto = False
    #     elif self.angulo < math.pi/2:
    #         if abajo:
    #             self.angulo = math.pi - self.angulo
    #     else:
    #         if arriba:
    #             self.angulo = 0
    #             self.en_salto = False

    def salto(self):
        self.rectangulo.y = self.posicion_inicial_salto - 26.46 * self.tiempo + (gravedad/2 * (self.tiempo**2))
        self.tiempo += 0.35
        arriba,abajo,_,_ = self.colision_orientacion(self.nivel_actual.suelo_colision,"solidos")
        if self.tiempo > 10.58:
            self.en_salto = False
        if self.tiempo < 5.29:
            if abajo:
                self.tiempo = 10.12 - self.tiempo
        else:
            if arriba:
                self.tiempo = 0
                self.en_salto = False

    def colision_orientacion(self, archivo, objeto):
        """
        Se obtiene en que direccion del bloque esta haciendo contacto el jugador.
        Se espera recibir, uno de los 3 archivos que existen para cada nivel, el suelo, las monedas o el de la puerta y como objeto, el tipo de bloque que es
        """
        arriba, abajo, izquierda, derecha = False, False, False, False

        for suelo in archivo[objeto]:
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

    def obtener_posicion(self, nivel, direccion):
        """
        Obtiene la posición del bloque según la dirección especificada.
        
        dirección: Puede ser 'arriba', 'izquierda', o 'derecha'.
        """
        for suelo in nivel.suelo_colision["solidos"]:
            x, y = suelo
            
            if direccion == 'arriba':
                if (self.rectangulo.y + self.rectangulo.height >= y and 
                    self.rectangulo.y + self.rectangulo.height <= y + gravedad) and (
                    self.rectangulo.x + self.rectangulo.width > x and 
                    self.rectangulo.x < x + tamaño_sprite):
                    return y - self.rectangulo.height
            
            elif direccion == 'izquierda':
                if (self.rectangulo.x <= x + tamaño_sprite and 
                    self.rectangulo.x >= x + tamaño_sprite - velocidad) and (
                    self.rectangulo.y + self.rectangulo.height > y and 
                    self.rectangulo.y < y + tamaño_sprite):
                    return x + tamaño_sprite
            
            elif direccion == 'derecha':
                if (self.rectangulo.x + self.rectangulo.width >= x and 
                    self.rectangulo.x + self.rectangulo.width <= x + velocidad) and (
                    self.rectangulo.y + self.rectangulo.height > y and 
                    self.rectangulo.y < y + tamaño_sprite):
                    return x - self.rectangulo.width
        
        # Si no hay colisión, se retorna la posición original dependiendo de la dirección
        if direccion == 'arriba':
            return self.rectangulo.y
        elif direccion == 'izquierda':
            return self.rectangulo.x
        elif direccion == 'derecha':
            return self.rectangulo.x

    def colision_monedas(self,nivel):
        """
        Se espera recibir el nivel actual
        Se encarga de que si esta colisionando con las monedas, estas desaparezcan del nivel, y que se le sume a los puntos
        """
        for monedas in nivel.colision_monedas["monedas"]:
            x,y = monedas
            rect = pygame.rect.Rect(x,y,tamaño_sprite,tamaño_sprite)
            if self.rectangulo.colliderect(rect):
                self.coins +=5
                nivel.colision_monedas["monedas"].remove((x,y))
                matriz_x = x // tamaño_sprite
                matriz_y = y // tamaño_sprite
                nivel.monedas[matriz_y][matriz_x] = -1

    def resetear_variables(self):
        """
        Funcion para resetear las variables, de posición, cuando muere o cuando cambia de nivel.
        """
        x,y = posicion_inicial_nivel[self.nivel]
        self.rectangulo.x = x
        self.rectangulo.y = y
        self.direccion = 0

    def colision_puertas(self,nivel):
        """
        Se espera recibir como parametros, el nivel actual, y funciona para detectar si se esta colisionando con la puerta.
        """
        for puertas in nivel.colision_puertas["puertas"]:
            x,y = puertas
            rect = pygame.rect.Rect(x,y,tamaño_sprite,tamaño_sprite)
            if self.rectangulo.colliderect(rect):
                return True
        return False

    def interaccion_puerta(self,screen,fuente):
        if self.colision_puertas(self.nivel_actual):
            self.dibujar_texto(screen,"Presione 'e' para continuar",fuente,self.rectangulo.x,self.rectangulo.y - tamaño_letras)

    def perder_vida(self):
        """
        Funcion de cuando pierde vida, cuando el jugador cae al vacio.
        """
        if self.rectangulo.y == alto - self.rectangulo.height:
            self.vidas -=1
            self.resetear_variables()

    def game_over(self):
        return self.vidas == -1

    def dibujar_corazones(self,screen):
        espacio = tamaño_sprite * 1.2

        for i in range(3):
            if i < self.vidas:
                sprite = self.corazones_sprite[0][1]
            else:
                sprite = self.corazones_sprite[0][0]
            screen.blit(sprite, (i * espacio, 0))
    
    def dibujar_texto(self,screen,texto,fuente,x,y):
        texto = fuente.render(texto,True,(0,0,0))
        screen.blit(texto,(x,y))

    def dibujar_personaje(self,screen):
        if self.sprite_actual > 2 or not self.en_movimiento:
            self.sprite_actual = 0
        screen.blit(self.personaje_sprite[self.direccion][self.sprite_actual],(self.rectangulo.x - 7, self.rectangulo.y -3))

    def dibujar(self,screen,fuente):
        self.dibujar_personaje(screen)
        self.dibujar_corazones(screen)
        self.dibujar_texto(screen,f"Puntos: {self.coins}",fuente,ancho//2,0)