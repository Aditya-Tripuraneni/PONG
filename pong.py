import pygame
import random

WIDTH, HEIGHT = 750, 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

FPS = 120

# colours
RED = (255, 0, 0)
VIOLET = (148, 0, 211)
INDIGO = (75, 0, 130)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)
WHITE = (255, 255, 255)

# data

data = {
    "playerOneCoins": 0,
    "playerTwoCoins": 0
}

run = True
pygame.init()

PLAYER_WIDTH, PLAYER_HEIGHT = 20, 100
BALL_RADIUS = 10
MAX_POINTS = 5


class Player:
    def __init__(self, x, y, width, height, colour, velocity=5):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.velocity = float(velocity)
        self.points = 0

    def draw_player(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height))

    def display_points(self, x, window):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"Points: {self.points}", True, ORANGE, BLUE)
        window.blit(text, (x, 0))

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        if winner:
            self.points = 0


class Ball:
    MAX_VEL = 5

    def __init__(self, x, y, colour, radius):
        self.x = x
        self.y = y
        self.colour = colour
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw_ball(self, window):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)

    def move_ball(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset_ball(self):
        random_direction = random.choice((-1, 1))
        ball.x = WIDTH // 2 + BALL_RADIUS // 2
        ball.y = HEIGHT // 2
        ball.x_vel = ball.MAX_VEL * random_direction
        ball.y_vel = 0


def handle_collision():
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    if ball.x_vel < 0:
        if (
                player_one.y + player_one.height) >= ball.y >= player_one.y and ball.x - BALL_RADIUS <= player_one.x + player_one.width:
            ball.x_vel *= -1
            handle_speed(player_one)
    else:
        if (AI.y + AI.height) >= ball.y >= AI.y and ball.x + BALL_RADIUS >= AI.x:
            ball.x_vel *= -1
            handle_speed(AI)

    player_score = False
    if ball.x > WIDTH:
        player_one.points += 1
        player_score = True

    elif ball.x < 0:
        AI.points += 1
        player_score = True

    if player_score:
        ball.reset_ball()
        player_one.reset()
        AI.reset()


def handle_speed(player):
    player_middle = player.y + player.height / 2
    delta_d = ball.y - player_middle
    reduction_factor = (player.height / 2) / ball.MAX_VEL
    y_vel = (delta_d / reduction_factor)
    ball.y_vel = y_vel


player_one = Player(0, HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT, WHITE)
AI = Player(WIDTH - 20, HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT, WHITE, velocity=15)

ball = Ball(WIDTH // 2 + BALL_RADIUS // 2, HEIGHT // 2, RED, BALL_RADIUS)
clock = pygame.time.Clock()


def control_ai():
    if ball.y - BALL_RADIUS <= AI.y and AI.y >= 0:  # if balls top is less than ai's top move up
        AI.y -= AI.velocity
    if ball.y + BALL_RADIUS >= AI.y + AI.height and AI.y + AI.height <= HEIGHT:  # if balls bottom is greater than ai's bottom move down
        AI.y += AI.velocity


def game_commands():
    player_one.draw_player(screen)
    AI.draw_player(screen)
    control_ai()
    player_one.display_points(player_one.x, screen)
    AI.display_points(AI.x - 122, screen)
    ball.draw_ball(screen)
    ball.move_ball()
    handle_collision()


while run:
    screen.fill((0, 0, 0))
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and player_one.y > 0:
        player_one.y -= player_one.velocity
    if keys[pygame.K_s] and player_one.y < HEIGHT - player_one.height:
        player_one.y += player_one.velocity

    winner = False
    if player_one.points == MAX_POINTS:
        winner = True
        player_winner = "Player 1 Won!"
        data["playerOneCoins"] += 1
        print(data.values())

    elif AI.points == MAX_POINTS:
        winner = True
        player_winner = "Computer Won!"
        data["playerTwoCoins"] += 1
        print(data.values())

    if winner:
        font = pygame.font.SysFont('Helvetica.ttf', 32)
        text = font.render(player_winner, True, GREEN)
        screen.blit(text, (WIDTH // 2 - (text.get_width() // 2), HEIGHT // 2 - (text.get_height() // 2)))
        pygame.display.update()
        pygame.time.delay(5000)
        player_one.reset()
        AI.reset()
        ball.reset_ball()

    midpoint = pygame.draw.rect(screen, WHITE, (WIDTH // 2, 0, 10, HEIGHT))
    game_commands()
    pygame.display.update()
