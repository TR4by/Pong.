import pygame, random

pygame.init()

### CONFIG ###

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) 
FPS = 60

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# Font
FONT = "PressStart2P.ttf"
FONT_SIZE_SMALL = 20
FONT_SIZE_MEDIUM = 40
FONT_SIZE_LARGE = 80

# Settings
WINNING_SCORE = 10
START_DELAY_MS = 3000

### ------ ###

screen_size = SCREEN_SIZE
full_screen = False

font = pygame.font.Font(FONT, FONT_SIZE_MEDIUM)
pong_font = pygame.font.Font(FONT, FONT_SIZE_LARGE)
game_over_font = pygame.font.Font(FONT, FONT_SIZE_SMALL)


text_left_player_won = font.render("PLAYER 1 WINS", False, COLOR_WHITE)
text_right_player_won = font.render("PLAYER 2 WINS", False, COLOR_WHITE)
text_game_over = game_over_font.render("Press ENTER to Restart", False, COLOR_WHITE)
text_pong = pong_font.render("PONG", True, COLOR_WHITE)
text_start = game_over_font.render("Press ENTER to Start", False, COLOR_WHITE)

clock = pygame.time.Clock()
round_start_time = 0

game_start = True
game_over = False

ball_information = []#[x, y, y_speed, direction]
ball_size = 20
ball_speed = 10

paddle_size = (20, 100)

left_paddle_position = [paddle_size[0] * 2, int(screen_size[1] / 2)]
right_paddle_position = [screen_size[0] - paddle_size[0] * 2, int(screen_size[1] / 2)]
paddle_speed = 5

left_score = 0
right_score = 0

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("BONG B]")

def ball_update(ball_position):
    new_y = ball_position[1] + ball_position[2]
    new_x = ball_position[0] + ball_speed * ball_position[3]
    if does_edge_bounce(new_y):
        new_speed = -ball_position[2]
    else:
        new_speed = ball_position[2]
    new_speed, new_direction = paddle_bounce(new_x, new_y, new_speed, ball_position[3])
    return [new_x, new_y, new_speed, new_direction]

def paddle_bounce(ball_x, ball_y, speed_y, direction):
    if ball_x - ball_size / 2 < left_paddle_position[0] and ball_x + ball_size / 2 > left_paddle_position[0] and ball_y - ball_size / 2 < left_paddle_position[1] + paddle_size[1] / 2 and ball_y + ball_size / 2 > left_paddle_position[1] - paddle_size[1] / 2 and direction == -1:
        speed_y = int((ball_y - left_paddle_position[1]) / 6) + random.randint(-1, 1)
        return speed_y, 1
    elif ball_x - ball_size / 2 < right_paddle_position[0] and ball_x + ball_size / 2 > right_paddle_position[0] and ball_y - ball_size / 2 < right_paddle_position[1] + paddle_size[1] / 2 and ball_y + ball_size / 2 > right_paddle_position[1] - paddle_size[1] / 2 and direction == 1:
        speed_y = int((ball_y - right_paddle_position[1]) / 6) + random.randint(-1, 1)
        return speed_y, -1
    else:
        return speed_y, direction

def does_edge_bounce(ball_y):
    if ball_y > screen_size[1] - ball_size / 2:
        return True
    elif ball_y < ball_size / 2:
        return True
    else:
        return False

def get_ball_start_position():
    random_direction = random.randint(0, 1)
    if random_direction == 0:
        random_direction = -1
    return [int(screen_size[0] / 2), int(screen_size[1] / 2), 0, random_direction]

def get_paddle_start_position():
    return int(screen_size[1] / 2)

def reset_all_positions():
    global left_paddle_position, right_paddle_position, ball_information
    ball_information = get_ball_start_position()
    left_paddle_position[1] = get_paddle_start_position()
    right_paddle_position[1] = get_paddle_start_position()

def score(ball_position):
    global right_score, left_score
    if ball_position[0] < 0:
        right_score += 1
        return True
    elif ball_position[0] > screen_size[0]:
        left_score += 1
        return True
    else:
        return False

reset_all_positions()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                reset_all_positions()
                left_score = 0
                right_score = 0
                round_start_time = pygame.time.get_ticks()
                game_start = False
                game_over = False
            elif event.key == pygame.K_f:
                if full_screen == False:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    full_screen = True
                elif full_screen == True:
                    pygame.display.quit()
                    screen = pygame.display.set_mode((800, 500))
                    full_screen = False
                    pygame.display.set_caption("Pong.")
                    pygame.display.init()
        elif event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_w] and left_paddle_position[1] > paddle_size[1]/2:
        left_paddle_position[1] -= paddle_speed
    if pressed_keys[pygame.K_s] and left_paddle_position[1] < screen_size[1] - paddle_size[1]/2:
        left_paddle_position[1] += paddle_speed
    if pressed_keys[pygame.K_UP] and right_paddle_position[1] > paddle_size[1]/2:
        right_paddle_position[1] -= paddle_speed
    if pressed_keys[pygame.K_DOWN] and right_paddle_position[1] < screen_size[1] - paddle_size[1]/2:
        right_paddle_position[1] += paddle_speed

    if pygame.time.get_ticks() - round_start_time > 3000 and not game_over and not game_start:
        ball_information = ball_update(ball_information)


    if score(ball_information):
        reset_all_positions()
        round_start_time = pygame.time.get_ticks()

    screen.fill((COLOR_BLACK))

    if game_start:
        screen.blit(text_pong, (int(screen_size[0]/2 - 330), int(screen_size[1]/2 - 60)))
        screen.blit(text_start, (int(screen_size[0]/2 - 330), int(screen_size[1]/2 + 20)))

    if game_over :
        screen.blit(text_game_over, (int(screen_size[0]/2 - 150), 450))

    if left_score >= 10:
        screen.blit(text_left_player_won, (int(screen_size[0]/2 - 270), screen_size[1] - 100))
        game_over = True
    elif right_score >= 10:
        screen.blit(text_right_player_won, (int(screen_size[0] / 2 - 270), screen_size[1] - 100))
        game_over = True

    if not game_start:
        left_score_text = font.render(str(left_score), False, (COLOR_WHITE))
        right_score_text = font.render(str(right_score), False, (COLOR_WHITE))
        screen.blit(left_score_text, (int(screen_size[0] / 2) - 150, 20))
        screen.blit(right_score_text, (int(screen_size[0] / 2) + 100, 20))
        pygame.draw.rect(screen, (COLOR_WHITE), (left_paddle_position[0] - int(paddle_size[0]), left_paddle_position[1] - int(paddle_size[1]/2), paddle_size[0], paddle_size[1]))
        pygame.draw.rect(screen, (COLOR_WHITE), (right_paddle_position[0], right_paddle_position[1] - int(paddle_size[1]/2), paddle_size[0], paddle_size[1]))

    pygame.draw.rect(screen, (COLOR_WHITE),(ball_information[0] - int(ball_size / 2), ball_information[1] - int(ball_size / 2), ball_size, ball_size))
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
