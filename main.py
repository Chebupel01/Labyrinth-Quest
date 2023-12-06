import pygame
import random


def find_zero_indexes(maze):
    zero_indexes = []

    for i in range(1, len(maze) - 1):
        for j in range(1, len(maze[i]) - 1):
            if maze[i][j] == 0:
                neighbors = [maze[i + dx][j + dy] for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
                if neighbors.count(1) == 7 and neighbors.count(0) == 1:
                    zero_indexes.append((i, j))

    return zero_indexes


pygame.init()
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
WHITE, BLACK, YELLOW, RED = (255, 255, 255), (0, 0, 0), (255, 255, 0), (255, 0, 0)
maze = [[1] * COLS for _ in range(ROWS)]
visited = [[False] * COLS for _ in range(ROWS)]
stack = [(1, 1)]
directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
SET_FINISH = 0
START_FLAG = 0
GAME_STATUS = 0
player_row, player_col = 1, 1
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural Generation")
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            new_row, new_col = player_row - 1, player_col
        elif keys[pygame.K_s]:
            new_row, new_col = player_row + 1, player_col
        elif keys[pygame.K_a]:
            new_row, new_col = player_row, player_col - 1
        elif keys[pygame.K_d]:
            new_row, new_col = player_row, player_col + 1
    maze[1][1] = 0
    if stack:
        current_row, current_col = stack[-1]
        visited[current_row][current_col] = True
        random.shuffle(directions)
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc
            if 0 < new_row < ROWS - 1 and 0 < new_col < COLS - 1 and not visited[new_row][new_col]:
                maze[new_row][new_col] = 0
                maze[current_row + dr // 2][current_col + dc // 2] = 0
                stack.append((new_row, new_col))
                if not SET_FINISH:
                    player_row, player_col = 1, 1
                    SET_FINISH = 1
                break
        else:
            stack.pop()
    elif not stack and SET_FINISH == 1:
        result = find_zero_indexes(maze)
        choice = random.choice(result)
        maze[choice[0]][choice[1]] = 2
        SET_FINISH = 2
    if not stack and not START_FLAG:
        START_FLAG = 1
        new_row, new_col = player_col * CELL_SIZE, player_row * CELL_SIZE
    elif 0 < new_row < ROWS - 1 and 0 < new_col < COLS - 1 and maze[new_row][new_col] == 0 and not stack:
        player_row, player_col = new_row, new_col
    elif 0 < new_row < ROWS - 1 and 0 < new_col < COLS - 1 and maze[new_row][new_col] == 2:
        running = False
        GAME_STATUS = 1
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if maze[row][col] == 0 else BLACK
            if maze[row][col] == 2:
                color = RED
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, YELLOW, (player_col * CELL_SIZE, player_row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()
    clock.tick(700)
if GAME_STATUS:
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pygame - You Have Won!")
    black = (0, 0, 0)
    white = (255, 255, 255)
    font = pygame.font.Font(None, 36)
    running = True
    text = font.render("You have won!", True, white)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(black)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
pygame.quit()
