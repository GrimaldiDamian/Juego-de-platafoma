from src.game.levels.level import Niveles
from src.game.entities.player import *
ancho = 1280
alto = 720
tamaño_sprite = 32
jugador = Player()
lvl1 = Niveles("src/game/levels/LEVEL1/prueba de mapa 2.csv","src/game/levels/LEVEL1/BACKGROUND.png")
jugador.nivel_actual = lvl1