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

contador_tiempo = 0

INITIAL_CASE = (
    (2, 3), # Posicion Jedy (Fila, col)
    (5), # Cantidad puntos concentracion
    ((0, 1), (1, 1), (2, 1), (3, 3), (3, 4), (3, 5)), # Paredes
    ((0, 2, 4), (1, 2, 2), (1, 4, 1),(3, 1, 3)) # Robot (Fila, Col, Cant. Robot)
)


class JedAiProblem(SearchProblem):
    def cost(self, state, action, state2):
        jump_set = set("Upleft", "Upright", "Downright", "Downleft")
        move_set = set("Up", "Down", "Left", "Right")
        cantidad_concentracion= state[1]
        if action[2] in jump_set:
            cantidad_concentracion -= 1
            contador_tiempo += 1
        pass
    
    def is_goal(self, state):
        pass

    def actions(self, state):
        row_jedy, col_jedy = state[0]
        wall = set(state[2])

        available_actions = []

        moves = [
            (row_jedy - 1, col_jedy, "Up"), # Arriba
            (row_jedy + 1, col_jedy, "Down"), # Abajo
            (row_jedy, col_jedy - 1, "Left"), # Izquierda
            (row_jedy, col_jedy + 1, "Right"), # Derecha
            (row_jedy - 1, col_jedy - 1, "Upleft"), # Diagonal arriba izquierda
            (row_jedy + 1, col_jedy + 1, "Downright"), # Diagonal abajo derecha
            (row_jedy + 1 , col_jedy - 1, "Downleft"), # Diagonal abajo izquierda
            (row_jedy - 1, col_jedy + 1, "Upright"), # Diagonal arriba derecha
        ]
        for new_col, new_row in moves:
            new_pos = (new_col, new_row)
            if new_pos not in wall:
                available_actions.append(new_pos)
        
        return available_actions
    
    def result(self, state, action):
        wall = set(state[2])

        pass
    
    