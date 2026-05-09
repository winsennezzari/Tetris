from constants import COLORS

class Tetromino:
    """Classe qui représente une pièce de Tetris"""
    
    def __init__(self, x, y, shape):
        self.x = x                    # position horizontale
        self.y = y                    # position verticale
        self.shape = shape            # numéro de la pièce (1 à 7)
        self.color = COLORS[shape]    # couleur correspondante
        self.rotation = 0             # rotation actuelle (on l'utilisera plus tard)

    # Les 7 formes de base des Tetrominos
    SHAPES = [
        [[0]],  # 0 = vide (on ne l'utilise pas)

        # 1 = I (barre)
        [[1, 1, 1, 1]],

        # 2 = J
        [[2, 0, 0],
         [2, 2, 2]],

        # 3 = L
        [[0, 0, 3],
         [3, 3, 3]],

        # 4 = O (carré)
        [[4, 4],
         [4, 4]],

        # 5 = S
        [[0, 5, 5],
         [5, 5, 0]],

        # 6 = T
        [[0, 6, 0],
         [6, 6, 6]],

        # 7 = Z
        [[7, 7, 0],
        [0, 7, 7]]
   
    ]

    def get_shape_matrix(self):
        """Retourne la matrice de la forme actuelle"""
        return self.SHAPES[self.shape]