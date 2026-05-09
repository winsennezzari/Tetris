# main.py - Tetris avec gravité corrigée (seulement quand ligne supprimée)

import pygame
import sys
import random
from constants import *
from tetromino import Tetromino

def draw_grid(screen):
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, GRAY, (0, y * BLOCK_SIZE), (GRID_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE))

def draw_tetromino(screen, tetromino):
    shape = tetromino.get_shape_matrix()
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell != 0:
                draw_x = (tetromino.x + x) * BLOCK_SIZE
                draw_y = (tetromino.y + y) * BLOCK_SIZE
                pygame.draw.rect(screen, tetromino.color, (draw_x, draw_y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, (draw_x, draw_y, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_board(screen, board):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if board[y][x] != 0:
                draw_x = x * BLOCK_SIZE
                draw_y = y * BLOCK_SIZE
                color = COLORS[board[y][x]]
                pygame.draw.rect(screen, color, (draw_x, draw_y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, (draw_x, draw_y, BLOCK_SIZE, BLOCK_SIZE), 1)

def can_move(piece, dx, dy, board):
    shape = piece.get_shape_matrix()
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell != 0:
                new_x = piece.x + x + dx
                new_y = piece.y + y + dy
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                    return False
                if new_y >= 0 and board[new_y][new_x] != 0:
                    return False
    return True

def lock_piece(piece, board):
    shape = piece.get_shape_matrix()
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell != 0:
                board_y = piece.y + y
                board_x = piece.x + x
                if board_y >= 0:
                    board[board_y][board_x] = piece.shape

def drop_floating_blocks(board):
    """Fait tomber tous les blocs qui flottent (gravité réelle)"""
    for x in range(GRID_WIDTH):
        write_y = GRID_HEIGHT - 1
        for y in range(GRID_HEIGHT - 1, -1, -1):
            if board[y][x] != 0:
                if write_y != y:
                    board[write_y][x] = board[y][x]
                    board[y][x] = 0
                write_y -= 1

def clear_lines(board):
    lines_cleared = 0
    i = 0
    while i < len(board):
        if all(board[i][x] != 0 for x in range(GRID_WIDTH)):
            del board[i]
            lines_cleared += 1
        else:
            i += 1
    
    # Ajoute des lignes vides en haut
    for _ in range(lines_cleared):
        board.insert(0, [0] * GRID_WIDTH)
    
    # Si on a supprimé au moins une ligne → on fait tomber les blocs
    if lines_cleared > 0:
        drop_floating_blocks(board)
    
    return lines_cleared

def is_game_over(board):
    for x in range(GRID_WIDTH):
        if board[0][x] != 0 or board[1][x] != 0:
            return True
    return False

def reset_game():
    board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_piece = Tetromino(x=3, y=0, shape=random.randint(1, 7))
    return board, current_piece, 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris - Gravité Correcte")
    
    clock = pygame.time.Clock()
    
    board, current_piece, score = reset_game()
    
    last_fall_time = pygame.time.get_ticks()
    fall_speed = FALL_SPEED
    game_over = False
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if game_over:
                    if event.key == pygame.K_r:
                        board, current_piece, score = reset_game()
                        last_fall_time = current_time
                        game_over = False
                else:
                    if event.key == pygame.K_LEFT:
                        if can_move(current_piece, -1, 0, board):
                            current_piece.x -= 1
                    if event.key == pygame.K_RIGHT:
                        if can_move(current_piece, 1, 0, board):
                            current_piece.x += 1
                    if event.key == pygame.K_DOWN:
                        if can_move(current_piece, 0, 1, board):
                            current_piece.y += 1
                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                        original = current_piece.get_shape_matrix()
                        new_shape = [list(reversed(col)) for col in zip(*original)]
                        current_piece.SHAPES[current_piece.shape] = new_shape
                        if not can_move(current_piece, 0, 0, board):
                            current_piece.SHAPES[current_piece.shape] = original

        if not game_over:
            if current_time - last_fall_time > fall_speed:
                if can_move(current_piece, 0, 1, board):
                    current_piece.y += 1
                    last_fall_time = current_time
                else:
                    lock_piece(current_piece, board)
                    
                    lines = clear_lines(board)
                    if lines > 0:
                        score += lines * 100
                    
                    if is_game_over(board):
                        game_over = True
                    else:
                        current_piece = Tetromino(x=3, y=0, shape=random.randint(1, 7))
                        last_fall_time = current_time

        screen.fill(BLACK)
        pygame.draw.rect(screen, DARK_GRAY, (0, 0, GRID_WIDTH * BLOCK_SIZE, SCREEN_HEIGHT))
        
        draw_grid(screen)
        draw_board(screen, board)
        if not game_over:
            draw_tetromino(screen, current_piece)

        font = pygame.font.SysFont("Arial", 28)
        score_text = font.render(f"Score : {score}", True, WHITE)
        screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 40, 80))

        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((180, 0, 0))
            screen.blit(overlay, (0, 0))
            
            font_big = pygame.font.SysFont("Arial", 72, bold=True)
            font_small = pygame.font.SysFont("Arial", 32)
            
            go_text = font_big.render("GAME OVER", True, WHITE)
            screen.blit(go_text, (SCREEN_WIDTH//2 - go_text.get_width()//2, 180))
            
            final_score = font_small.render(f"Score final : {score}", True, WHITE)
            screen.blit(final_score, (SCREEN_WIDTH//2 - final_score.get_width()//2, 280))
            
            restart = font_small.render("Appuie sur R pour recommencer", True, WHITE)
            screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, 340))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()