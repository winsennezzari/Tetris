# constants.py
# Tous les paramètres du jeu Tetris

# Dimensions de la grille
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Taille de chaque bloc (en pixels)
BLOCK_SIZE = 30

# Dimensions de la fenêtre
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE + 300   # 300 pixels pour la zone de droite (score + next)
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (40, 40, 40)

# Couleurs des 7 pièces de Tetris
COLORS = [
    (0, 0, 0),        # 0 = vide (ne pas utiliser)
    (0, 255, 255),    # 1 = I Cyan
    (255, 165, 0),    # 2 = J Orange
    (0, 0, 255),      # 3 = L Bleu
    (255, 255, 0),    # 4 = O Jaune
    (0, 255, 0),      # 5 = S Vert
    (128, 0, 128),    # 6 = T Violet
    (255, 0, 0)       # 7 = Z Rouge
]

# Vitesse de chute (en millisecondes)
FALL_SPEED = 500      # 500 ms = 0.5 seconde (on pourra le changer plus tard)

# Taille de la zone "Prochaine pièce"
PREVIEW_SIZE = 4