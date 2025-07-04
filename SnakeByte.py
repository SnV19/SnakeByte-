import pygame
import time
import random

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Load sounds
start_sound = pygame.mixer.Sound('start.wav')
eat_sound = pygame.mixer.Sound('crunch.wav')
game_over_sound = pygame.mixer.Sound('gameend.wav')
start_sound.play()

# Game settings
snake_speed = 5
speed_increment = 3
window_x = 720
window_y = 480

# Colors
black = pygame.Color(255, 255, 0)
white = pygame.Color(255, 0, 0)
red = pygame.Color(0, 0, 255)
green = pygame.Color(0, 0, 0)
blue = pygame.Color(0, 0, 255)

# Window setup
pygame.display.set_caption('GeeksforGeeks Snakes')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

# Snake setup
snake_position = [100, 50]
snake_body = [
    [100, 50],
    [90, 50],
    [80, 50],
    [70, 50]
]

# Fruit setup
fruit_position = [
    random.randrange(1, (window_x // 10)) * 10,
    random.randrange(1, (window_y // 10)) * 10
]
fruit_spawn = True

# Initial direction and score
direction = 'RIGHT'
change_to = direction
score = 0

# Display score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# Game over function
def game_over():
    pygame.mixer.Sound.play(game_over_sound)
    my_font = pygame.font.SysFont('Segoe Script', 15)

    if score < 100:
        level_message = "Easy Level"
        cool_message = "Game Over! But don't worry, you can always shed your skin and try again"
    elif score < 200:
        level_message = "Medium Level - Well Done!"
        cool_message = "You're getting better! But don't get too comfortable..."
    else:
        level_message = "Hard Level - You're a Pro!"
        cool_message = "You're a snake master! Brilliant job!"

    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect(center=(window_x / 2, window_y / 4))
    game_window.blit(game_over_surface, game_over_rect)

    level_surface = my_font.render(level_message, True, white)
    level_rect = level_surface.get_rect(center=(window_x / 2, window_y / 2))
    game_window.blit(level_surface, level_rect)

    cool_surface = my_font.render(cool_message, True, white)
    cool_rect = cool_surface.get_rect(center=(window_x / 2, window_y / 2 + 50))
    game_window.blit(cool_surface, cool_rect)

    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Prevent reverse direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body mechanics
    snake_body.insert(0, list(snake_position))
    if snake_position == fruit_position:
        score += 10
        snake_speed += speed_increment
        fruit_spawn = False
        pygame.mixer.Sound.play(eat_sound)
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [
            random.randrange(1, (window_x // 10)) * 10,
            random.randrange(1, (window_y // 10)) * 10
        ]
    fruit_spawn = True

    # Draw background, snake and fruit
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Collision with wall
    if (snake_position[0] < 0 or snake_position[0] > window_x - 10 or
        snake_position[1] < 0 or snake_position[1] > window_y - 10):
        game_over()

    # Collision with self
    for block in snake_body[1:]:
        if snake_position == block:
            game_over()

    # Display score and update screen
    show_score(1, white, 'times new roman', 20)
    pygame.display.update()
    fps.tick(snake_speed)
