INITIAL_CASE = (
    (2, 3), # Posicion Jedy (Fila, col)
    (5), # Cantidad puntos concentracion
    ((0, 1), 
     (1, 1), 
     (2, 1), 
     (3, 3), 
     (3, 4), 
     (3, 5)), # Paredes
    ((0, 2, 0), 
     (1, 2, 0), 
     (1, 4, 0),
     (3, 1, 2)) # Robot (Fila, Col, Cant. Robot)
)

def rest_func(row,col):
    robot = set(INITIAL_CASE[3])

    if (row,col) not in :
        return True
    return False
