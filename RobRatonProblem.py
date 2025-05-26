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

INITIAL_CASE = (
    (5, 3), #RobotRaton estado inicial
    ((3, 0),(5, 0),(1, 1),(3, 1),(3, 2),(4, 2),(0, 3),(1, 4),(3, 4),(5, 4),(5, 3)), #Paredes
    ((2, 1),(4, 3),(0, 4)), #Comida
    (5, 3), # Salida y entrada
    (0) # Contador
)



class RobRatonProblem(SearchProblem):
    def is_goal(self, state):
        count = state[4]
        return count == 3

    def cost(self, state, action, state2):
        return 1
    
    def actions(self, state):
        col_raton, row_raton = state[0]
        wall = set(state[1])

        available_actions = []

        moves = [
            (col_raton - 1, row_raton),  # izquierda
            (col_raton + 1, row_raton),  # derecha
            (col_raton, row_raton - 1),  # arriba
            (col_raton, row_raton + 1),  # abajo
            (col_raton, row_raton ),  # quedarse en el lugar
        ]

        for new_col, new_row in moves:
            new_pos = (new_col, new_row)
            if 0 <= new_col <= 5 and 0 <= new_row <= 5 and new_pos not in wall:
                available_actions.append(new_pos)
        
        return available_actions

    def result(self, state, action):
        wall = state[1]
        meal = set(state[2])
        exit = state[3]
        count = state[4]
        if action in meal:
            meal.remove(action)
            count += 1

        new_state = (action, wall, tuple(meal), exit, count)
        return new_state
    
    def heuristic(self, state):
        raton_pos = state[0]
        comidas = set(state[2])
        contador = state[4]

        if contador >= 3:
            return 0

        def manhattan(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        distancias = [manhattan(raton_pos, comida) for comida in comidas]
        distancias.sort()

        comidas_restantes = 3 - contador
        return sum(distancias[:comidas_restantes])

problem = RobRatonProblem(INITIAL_CASE)

result = astar(problem, problem.heuristic)

print("Cantidad de pasos:", len(result.path()) - 1)

for i, (action, state) in enumerate(result.path()):
    print(f"Paso {i}: Acción: {action}")