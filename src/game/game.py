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

    def dibujar(self):
        if self.etapa == "level 1":
            lvl1.dibujar(self.screen)
        
        pygame.display.flip()

    def game(self):
        while self.runnig:
            self.manejo_evento
            
            self.reloj.tick(60)
            
            self.dibujar()