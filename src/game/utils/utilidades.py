from src.game.levels.level import Niveles
from src.game.entities.player import *
jugador = Player()
lvl1 = Niveles("src/game/levels/LEVEL1/mapa_suelo.csv","src/game/levels/LEVEL1/mapa_monedas.csv","src/game/levels/LEVEL1/BACKGROUND.png")
jugador.nivel_actual = lvl1