from src.game.levels.level import Niveles
from src.game.entities.player import *
jugador = Player()

def obtener_nivel_actual():
    nivel = Niveles(f"src/game/levels/LEVEL{jugador.nivel}/mapa_suelo.csv",f"src/game/levels/LEVEL{jugador.nivel}/mapa_monedas.csv",f"src/game/levels/LEVEL{jugador.nivel}/mapa_puertas.csv",f"src/game/levels/LEVEL{jugador.nivel}/BACKGROUND.png")
    return nivel

jugador.nivel_actual = obtener_nivel_actual()