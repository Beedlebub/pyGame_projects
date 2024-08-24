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


def ball_control():
    # Make sure these variables are global and not local to function
    global ball_speed_x, ball_speed_y
    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    # Ball collision
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_restart()
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # type: ignore
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))


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


def draw_game():
    # Draw visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH / 2,
                                            0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
    # Update window
    pygame.display.flip()


while True:
    # Main game loop
    ball_control()
    player_control()
    opponent_control()
    draw_game()
    # Updates the game clock
    clock.tick(60)
