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
    (0, 1),
    ((0, 2), (2, 1), (3, 1)),
    (3, 5)
)


            

class RobDefProblem(SearchProblem):
    def cost(self, state, action, state2):
        return 1
    
    def actions(self, state):
        pos_robot = state[0]
        habs = set(state[1])
        
        robot_col, robot_row = pos_robot

        moves = [
            (robot_col - 1, robot_row),  # izquierda
            (robot_col + 1, robot_row),  # derecha
            (robot_col, robot_row - 1),  # arriba
            (robot_col, robot_row + 1),  # abajo
        ]

        available_actions = []
        for new_col, new_row in moves:
            new_pos = (new_col, new_row)
            if new_pos not in habs:
                available_actions.append(new_pos) 
        return available_actions
    
    def result(self, state, action):
        habs = state[1]
        target = state[2]

        new_state = (action, habs, target)
        return new_state

    def is_goal(self, state):
        pos_robot = state[0]
        target_pos = state[2]
        return pos_robot == target_pos
    
    

problem = RobDefProblem(INITIAL_CASE)

result = breadth_first(problem)

print("Cantidad de pasos:", len(result.path()) - 1)

for i, (action, state) in enumerate(result.path()):
    print(f"Paso {i}: Acción: {action}")