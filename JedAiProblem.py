from simpleai.search.viewers import BaseViewer, WebViewer
from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    limited_depth_first,
    uniform_cost,
    iterative_limited_depth_first,
    greedy,
    astar,
)


def hayRobotsEnMiLugar(fila,col, state):
    coordenada_jed = (fila,col)
    coordenada_rob = (0,0)

    for fila in state[3]:
        coordenada_rob = fila[0:2]
        if coordenada_rob == coordenada_jed: #evalua si hay robots en su casillero
            return True
    return False

def comprobarlugar(fila,col,state):
    if hayRobotsEnMiLugar(fila,col,state):
        return True
    if hayRobotsEnMiLugar(fila - 1,col,state):
        return True
    if hayRobotsEnMiLugar(fila + 1, col,state):
        return True
    if hayRobotsEnMiLugar(fila, col + 1,state): 
        return True
    if hayRobotsEnMiLugar(fila, col - 1,state):
        return True
    else:
        return False
        
INITIAL_CASE = (
    (2, 2), # Posicion Jedy (Fila, col)
    (5), # Cantidad puntos concentracion
    ((0, 1), 
     (1, 1), 
     (2, 1), 
     (3, 3), 
     (3, 4), 
     (3, 5)), # Paredes
    ((0, 2, 4), 
     (1, 2, 2), 
     (1, 4, 1),
     (3, 1, 3)) # Robot (Fila, Col, Cant. Robot)
)


class JedAiProblem(SearchProblem):
    def cost(self, state, action, state2):
        count_time = 0
        if action[2] == "rest":
            count_time += 3
        elif action[2] == "force":
            count_time += 2
        else:
            count_time += 1

        return count_time
    
    def is_goal(self, state):
        for tupla in state[3]:
            if tupla[2] != 0:
                return False
        return True

    def actions(self, state):
        row_jedy, col_jedy = state[0]
        wall = set(state[2])
        p_concentration = state[1]

        available_actions = []

        moves = [
            (row_jedy, col_jedy + 1, "move"), # Derecha
            (row_jedy - 1, col_jedy, "move"), # Arriba
            (row_jedy + 1, col_jedy, "move"), # Abajo
            (row_jedy, col_jedy - 1, "move"), # Izquierda
            (row_jedy - 1, col_jedy - 1, "jump"), # Diagonal arriba izquierda
            (row_jedy + 1, col_jedy + 1, "jump"), # Diagonal abajo derecha
            (row_jedy + 1 , col_jedy - 1, "jump"), # Diagonal abajo izquierda
            (row_jedy - 1, col_jedy + 1, "jump"), # Diagonal arriba derecha
            (row_jedy, col_jedy, "rest"), # Descansar
            (row_jedy, col_jedy, "slash"), # Ataque de espada
            (row_jedy, col_jedy, "force") # Ataque en area
        ]
        # 1. Rest solo cuando en move no haya robot
        # 2. force cuando haya 2 o mas puntos de concentracion y solo cuando en su casilla haya 1 o mas robot
        # 3. slash cuando haya 1 o mas puntos de concentracion y solo cuando en su casilla haya 1 o mas robot
        # 4. jump cuando haya 1 o mas puntos de concentracion y el destino no sea un muro
        # 5. move cuando el destino no haya un muro

        for new_row, new_col, act in moves:
            new_pos = (new_row, new_col)
            #Rest restriction
            if act == "rest":
                if comprobarlugar(new_row, new_col, state) == False:
                    new_act = (new_row, new_col, act)
                    available_actions.append(new_act)

            #Force restriction
            if act == "force":
                if hayRobotsEnMiLugar(new_row, new_col, state) and p_concentration >= 5:
                    new_act = (new_row, new_col, act)
                    available_actions.append(new_act)

            #Slash restriction
            if act == "slash":
                if hayRobotsEnMiLugar(new_row, new_col, state) and p_concentration >= 1:
                    new_act = (new_row, new_col, act)
                    available_actions.append(new_act)

            #Jump restriction
            if act == "jump":
                if new_pos not in wall and p_concentration >= 1:
                    new_act = (new_row, new_col, act)
                    available_actions.append(new_act)
                    
            #Move restriction
            if act == "move":     
                if new_pos not in wall: 
                    new_act = (new_row, new_col, act)
                    available_actions.append(new_act)
                    
        return available_actions
    
    def result(self, state, action):
        row_jedy, col_jedy = action[0], action[1]
        pconcentration = state[1]
        wall = state[2]
        old_robots = state[3]

        # Actualizar puntos de concentración por la acción
        if action[2] == "rest":
            pconcentration += 10
        elif action[2] == "jump":
            pconcentration -= 1
        # move no cambia pconcentration, force/slash restan después

        # Construir nuevo conjunto de robots
        new_robots = []
        for bot_row, bot_col, bot_count in old_robots:
            if (bot_row, bot_col) == (row_jedy, col_jedy):
                if action[2] == "force":
                    bot_count = 0
                    pconcentration -= 5
                elif action[2] == "slash":
                    bot_count = max(0, bot_count - 1)
                    pconcentration -= 1
            new_robots.append((bot_row, bot_col, bot_count))

        # Devolver estado completamente nuevo (inmutable)
        return (
            (row_jedy, col_jedy),
            pconcentration,
            tuple(wall),
            tuple(new_robots),
        )


   
    def heuristic(self, state):
        pos_jedy = state[0]         # (fila, columna)
        robots   = state[3]         # lista de (fila, columna, cantidad)

        # Si no hay robots, no falta costo
        if all(amount == 0 for (_, _, amount) in robots):
            return 0

        def manhattan(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        # Sumar dist × cantidad para cada celda
        h = 0
        for row, col, amount in robots:
            if amount > 0:
                d = manhattan(pos_jedy, (row, col))
                h += d * amount

        return h
    
problem = JedAiProblem(INITIAL_CASE)
viewer = WebViewer()
result = astar(
    problem,
    graph_search=True,
)
# result.path() es una lista de tuplas (acción, estado), donde la primera acción es None
path = result.path()

# Extraemos y formateamos solo las acciones
jedi_actions = []
for action, state in path[1:]:  
    act_type = action[2] 
    pconcentration = state[1] 
    if act_type in ("move", "jump"):
        destino = (action[0], action[1])
    else:
        destino = None

    jedi_actions.append((act_type, destino, pconcentration))

# Imprimimos la secuencia óptima
print(jedi_actions)

[('move', (2, 2), 5), 
 ('move', (1, 2), 5), 
 ('move', (0, 2), 5), 
 ('force', None, 0), 
 ('move', (1, 2), 0), 
 ('move', (2, 2), 0), 
 ('move', (2, 3), 0), 
 ('rest', None, 10), 
 ('jump', (1, 2), 9), 
 ('slash', None, 8), 
 ('slash', None, 7), 
 ('move', (2, 2), 7), 
 ('jump', (3, 1), 6), 
 ('slash', None, 5), 
 ('slash', None, 4), 
 ('slash', None, 3), 
 ('jump', (2, 2), 2), 
 ('move', (1, 2), 2), 
 ('move', (1, 3), 2),
('move', (1, 4), 2), 
('slash', None, 1)]