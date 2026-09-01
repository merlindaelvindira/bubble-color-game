import pygame
import random

# --- GAME SETUP ---
pygame.init()

# Screen dimensions and grid settings
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 5
CELL_SIZE = WIDTH // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Match Game")

# Colors (RGB)
COLORS = [
    (255, 59, 48),   # Red
    (52, 199, 89),   # Green
    (0, 122, 255),   # Blue
    (255, 204, 0)    # Yellow
]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create grid with random ball colors
board = [[random.choice(COLORS) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

score = 0
font = pygame.font.Font(None, 36)
selected_ball = None


# --- GAME LOGIC ---
def check_matches():
    global score
    matches = []

    # Check horizontal matches
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE - 2):
            if board[y][x] == board[y][x + 1] == board[y][x + 2]:
                matches.extend([(x, y), (x + 1, y), (x + 2, y)])

    # Check vertical matches
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE - 2):
            if board[y][x] == board[y + 1][x] == board[y + 2][x]:
                matches.extend([(x, y), (x, y + 1), (x, y + 2)])

    # Remove matched balls, replace with new colors, and update score
    if matches:
        for x, y in set(matches):
            board[y][x] = random.choice(COLORS)
            score += 10
        return True
    return False


# Clear initial matches before game starts
while check_matches():
    score = 0


def draw_screen():
    screen.fill(WHITE)

    # Draw grid balls
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            ball_color = board[y][x]
            center_x = x * CELL_SIZE + CELL_SIZE // 2
            center_y = y * CELL_SIZE + CELL_SIZE // 2 + 50  # 50px offset for score banner

            # Draw ball
            pygame.draw.circle(screen, ball_color, (center_x, center_y), CELL_SIZE // 2 - 5)

            # Draw selection border
            if selected_ball == (x, y):
                pygame.draw.circle(screen, BLACK, (center_x, center_y), CELL_SIZE // 2, 3)

    # Render score text
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()


# --- MAIN GAME LOOP ---
running = True
while running:
    draw_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Ensure click is inside the game board area
            if mouse_y > 50:
                grid_x = mouse_x // CELL_SIZE
                grid_y = (mouse_y - 50) // CELL_SIZE

                if selected_ball:
                    x_start, y_start = selected_ball

                    # Check if selected cell is adjacent (up/down/left/right)
                    if abs(x_start - grid_x) + abs(y_start - grid_y) == 1:
                        # Swap colors
                        board[y_start][x_start], board[grid_y][grid_x] = (
                            board[grid_y][grid_x],
                            board[y_start][x_start],
                        )

                        # Revert swap if no match is made
                        if not check_matches():
                            board[y_start][x_start], board[grid_y][grid_x] = (
                                board[grid_y][grid_x],
                                board[y_start][x_start],
                            )

                    selected_ball = None  # Reset selection
                else:
                    selected_ball = (grid_x, grid_y)

pygame.quit()