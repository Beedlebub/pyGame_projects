# Simple game of Pong, using pygame

# Import modules
import pygame
import sys
import random


# General setup
pygame.init()
clock = pygame.time.Clock()

# Set up Main Screen display surface
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Ball
ball_width = 20
ball_height = 20
ball = pygame.Rect(SCREEN_WIDTH / 2 - ball_width / 2,
                   SCREEN_HEIGHT / 2 - ball_height / 2, ball_width, ball_height)
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))

# Player
player_width = 10
player_height = 100
player = pygame.Rect(SCREEN_WIDTH - (player_width + 10), SCREEN_HEIGHT / 2 -
                     player_height / 2, player_width, player_height)
player_current_speed = 0
player_speed = 7

# Opponent
opponent_width = 10
opponent_height = 100
opponent = pygame.Rect(10, SCREEN_HEIGHT / 2 - opponent_height /
                       2, opponent_width, opponent_height)
opponent_speed = 5

# Colors
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Text
player_score = 0
opponent_score = 0
game_font = pygame.font.Font('freesansbold.ttf', 32)

# Score timer
score_time = True
current_time = None


def ball_control():
    # Make sure these variables are global and not local to function
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    # Ball collision
    if ball.left <= 0:
        player_score += 1  # Change back to 1
        score_time = pygame.time.get_ticks()
    if ball.right >= SCREEN_WIDTH:
        opponent_score += 1  # Change back to 1
        score_time = pygame.time.get_ticks()
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


def ball_restart():
    global ball_speed_x, ball_speed_y, current_time, score_time
    current_time = pygame.time.get_ticks()
    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # type: ignore
    if current_time - score_time < 700:
        number_three = game_font.render('3', False, light_grey)
        screen.blit(number_three, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
        print('Three')
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render('2', False, light_grey)
        screen.blit(number_two, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
        print('Two')
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render('1', False, light_grey)
        screen.blit(number_one, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
        print('One')
    if current_time - score_time < 2100:
        ball_speed_x = 0
        ball_speed_y = 0
    else:
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        score_time = None


def player_control():
    # Make sure these variables are global and not local to function
    global player_current_speed, player_speed
    # Input key assignments
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_current_speed += player_speed
            if event.key == pygame.K_UP:
                player_current_speed -= player_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_current_speed -= player_speed
            if event.key == pygame.K_UP:
                player_current_speed += player_speed
    # Update player vertical (y up/down) position based on any keys pressed
    player.y += player_current_speed
    # Don't let player move off the screen
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT


def opponent_control():
    # Make sure these variables are global and not local to function
    global opponent_speed
    # If the opponent's top is avove center of ball, move it down
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    # If the opponent's bottom is below center of ball, move it up
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    # Don'e let opponent move off the screen
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT


def draw():
    # Draw visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH / 2,
                                            0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
    # Draw text
    player_text = game_font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text, (415, 285))
    opponent_text = game_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text, (355, 285))
    # Update window
    pygame.display.flip()


while True:
    # Main game loop
    if score_time:
        ball_restart()
    ball_control()
    player_control()
    opponent_control()
    draw()
    # Updates the game clock
    clock.tick(60)
