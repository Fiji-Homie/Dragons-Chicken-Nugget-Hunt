import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 32  # Size of each "block" for dragon and nugget

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dragon Nugget Hunt")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load dragon and nugget sprites
dragon_sprite = pygame.image.load('dragon.png')
dragon_sprite = pygame.transform.scale(dragon_sprite, (CELL_SIZE, CELL_SIZE))  # Resize to fit CELL_SIZE

nugget_sprite = pygame.image.load('nugget.png')
nugget_sprite = pygame.transform.scale(nugget_sprite, (CELL_SIZE, CELL_SIZE))  # Resize to fit CELL_SIZE

# Fonts for game over and score
font_big = pygame.font.SysFont('arial', 50)
font_small = pygame.font.SysFont('arial', 24)

def display_score(score):
    """Function to display the score in the top-left corner."""
    score_surface = font_small.render(f'Score: {score}', True, (255, 165, 0))  # Orange color
    screen.blit(score_surface, (10, 10))

def display_game_over():
    """Function to display 'Game Over' message on the screen."""
    screen.fill((0, 0, 0))  # Clear the screen
    game_over_surface = font_big.render('GAME OVER', True, (255, 0, 0))  # Red text
    game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(game_over_surface, game_over_rect)

    play_again_surface = font_small.render('Press R to Play Again or Q to Quit', True, (255, 255, 255))  # White text
    play_again_rect = play_again_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(play_again_surface, play_again_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle Quit
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press R to play again
                    return True
                elif event.key == pygame.K_q:  # Press Q to quit
                    return False

def main_game():
    """Main game loop."""
    # Dragon settings
    dragon_pos = [100, 50]  # Start position
    dragon_body = [[100, 50], [100 - CELL_SIZE, 50], [100 - 2 * CELL_SIZE, 50]]  # Initial size (3 segments)
    direction = 'RIGHT'
    change_to = direction

    # Chicken nugget position
    nugget_pos = [random.randrange(1, (WIDTH // CELL_SIZE)) * CELL_SIZE,
                  random.randrange(1, (HEIGHT // CELL_SIZE)) * CELL_SIZE]
    nugget_spawn = True

    # Score
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close the game
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        # Change direction
        direction = change_to

        # Update dragon's position
        if direction == 'UP':
            dragon_pos[1] -= CELL_SIZE
        if direction == 'DOWN':
            dragon_pos[1] += CELL_SIZE
        if direction == 'LEFT':
            dragon_pos[0] -= CELL_SIZE
        if direction == 'RIGHT':
            dragon_pos[0] += CELL_SIZE

        # Grow the dragon
        dragon_body.insert(0, list(dragon_pos))

        # Create rectangles for collision detection
        dragon_head_rect = pygame.Rect(dragon_pos[0], dragon_pos[1], CELL_SIZE, CELL_SIZE)
        nugget_rect = pygame.Rect(nugget_pos[0], nugget_pos[1], CELL_SIZE, CELL_SIZE)

        # Check for collision with the chicken nugget
        if dragon_head_rect.colliderect(nugget_rect):
            score += 1
            nugget_spawn = False
        else:
            dragon_body.pop()

        # Respawn chicken nugget
        if not nugget_spawn:
            nugget_pos = [random.randrange(1, (WIDTH // CELL_SIZE)) * CELL_SIZE,
                          random.randrange(1, (HEIGHT // CELL_SIZE)) * CELL_SIZE]
        nugget_spawn = True

        # Game over conditions (hit wall or hit own body)
        if dragon_pos[0] < 0 or dragon_pos[0] >= WIDTH or dragon_pos[1] < 0 or dragon_pos[1] >= HEIGHT:
            return False

        for block in dragon_body[1:]:
            if dragon_pos == block:
                return False

        # Draw everything
        screen.fill((0, 0, 0))  # Black background

        # Draw dragon as sprites
        for pos in dragon_body:
            screen.blit(dragon_sprite, (pos[0], pos[1]))

        # Draw chicken nugget as a sprite
        screen.blit(nugget_sprite, (nugget_pos[0], nugget_pos[1]))

        display_score(score)
        pygame.display.update()

        clock.tick(15)  # Control speed (15 frames per second)

# Main game loop
while True:
    if not main_game():  # If the player loses, show game over screen
        play_again = display_game_over()
        if not play_again:
            break  # Exit the loop and end the game

pygame.quit()
