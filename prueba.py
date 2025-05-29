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
     (1, 2, 3), 
     (1, 4, 1),
     (3, 1, 2)) # Robot (Fila, Col, Cant. Robot)
)

caso = (
    (2, 3), # Posicion Jedy (Fila, col)
    (5), # Cantidad puntos concentracion
    ((0, 1), 
     (1, 1), 
     (2, 1), 
     (3, 3), 
     (3, 4), 
     (3, 5)), # Paredes
    ((0, 2, 2), 
     (1, 2, 3), 
     (1, 4, 0),
     (3, 1, 0)) # Robot (Fila, Col, Cant. Robot)
)


def heuristic(state):
        count_robot_restantes = 0
        robot = set(state[3])
        pos_jedy = state[0]

        for bot in robot:
            count_robot_restantes += bot[2]

        if count_robot_restantes == 0:
             return 0 
        
        def manhattan(pos1, pos2):
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        
        distancia = [manhattan(pos_jedy,(bots[0], bots[1])) for bots in robot]
        distancia.sort()

        return sum(distancia[:count_robot_restantes])

problem = heuristic(caso)
print(problem)