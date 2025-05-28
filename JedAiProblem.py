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
dicc_moves = {
     "Slash": {
         "Tiempo": 1, 
         "Concentracion": 1
     },
     "Move": {
         "Tiempo": 1, 
         "Concentracion": 0
     },
     "Slash": {
         "Tiempo": 1, 
         "Concentracion": 1
     },
     "Slash": {
         "Tiempo": 1, 
         "Concentracion": 1
     }
}



INITIAL_CASE = (
    (2, 3), # Posicion Jedy (Fila, col)
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
        jump_set = "jump"
        move_set = "move"
        rest = "rest"
        slash = "slash"
        force = "force"
        cantidad_concentracion= state[1]
        if action[2] in jump_set:
            cantidad_concentracion -= 1
            contador_tiempo += 1
            
        if action[2] in rest:
            cantidad_concentracion += 10
            contador_tiempo += 3

        if action[2] in slash:
            cantidad_concentracion -= 1
            contador_tiempo += 1

        if action[2] in force:
            cantidad_concentracion -= 2
            contador_tiempo += 5

        if action[2] in move_set:
            contador_tiempo += 1

        
        return contador_tiempo, cantidad_concentracion
    
    def is_goal(self, state):
        for tupla in state[3]:
            if tupla[2] != 0:
                return False
        return True

    def actions(self, state):
        row_jedy, col_jedy = state[0]
        wall = set(state[2])
        robot = set(state[3])
        p_concentration = state[1]

        available_actions = []

        moves = [
            (row_jedy - 1, col_jedy, "move"), # Arriba
            (row_jedy + 1, col_jedy, "move"), # Abajo
            (row_jedy, col_jedy - 1, "move"), # Izquierda
            (row_jedy, col_jedy + 1, "move"), # Derecha
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

        for new_col, new_row, act in moves:
            new_pos = (new_col, new_row)
            #Rest
            if act == "rest":
                if (new_col, new_row) not in robot:
                    
                    
            #Cuando se hace un move
            if new_pos not in wall: 
                available_actions.append(new_pos)

        
        return available_actions
    
    def result(self, state, action):
        wall = set(state[2])
        robot = set(state[3])
        pconcentration = state[1]
        slash = "Slash"
        force = "Force"

        row_jedy, col_jedy = action[0], action[1]
        pos_jedy = (row_jedy, col_jedy)
        if action[2] in slash:
            row_jedy, col_jedy = action[0], action[1]
            jedy_pos = (row_jedy, col_jedy)
            for bot in robot:
                for row_bot, col_bot, cant_bot in bot:
                    pos_bot = (row_bot,col_bot)
                    if pos_bot == jedy_pos:
                        return cant_bot
            
            cant_bot -= 1
        
        if action[2] in force:
            row_jedy, col_jedy = action[0], action[1]
            jedy_pos = (row_jedy, col_jedy)
            for bot in robot:
                for row_bot, col_bot, cant_bot in bot:
                    pos_bot = (row_bot,col_bot)
                    if pos_bot == jedy_pos:
                        return cant_bot
            
            cant_bot -= cant_bot

        jedy_pos
        new_state = (pos_jedy,pconcentration,wall,robot )
        return new_state
    
    