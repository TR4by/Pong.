import pygame
from enum import Enum
from src.config import *
from src.paddle import Paddle
from src.ball import Ball

class GameState(Enum):
    PLAYING = 0
    STARTING = 1
    GAME_OVER = 2

class Game:
    def __init__(self):

        # Initialize game
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
        pygame.display.set_caption("Pong.")
        self.clock = pygame.time.Clock()
        self.running = True
        self.full_screen = False
        self.state = GameState.STARTING

        # Initialize fonts
        self.font = pygame.font.Font(FONT_PATH, 40)
        self.pong_font = pygame.font.Font(FONT_PATH, 80)
        self.game_over_font = pygame.font.Font(FONT_PATH, 20)

        # Initialize text
        self.text_pong = self.pong_font.render("PONG", True, COLOR_WHITE)
        self.text_left_player_won = self.font.render("PLAYER 1 WINS", False, COLOR_WHITE)
        self.text_right_player_won = self.font.render("PLAYER 2 WINS", False, COLOR_WHITE)
        self.text_game_over = self.game_over_font.render("Press ENTER to Restart", False, COLOR_WHITE)
        self.text_start = self.game_over_font.render("Press ENTER to Start", False, COLOR_WHITE)

        # Initialize game objects
        paddle_left_x = PADDLE_OFFSET
        paddle_right_x = SCREEN_WIDTH - PADDLE_OFFSET - PADDLE_WIDTH
        paddle_y = SCREEN_HEIGHT // 2

        self.left_paddle = Paddle(
            x = paddle_left_x, 
            y = paddle_y, 
            width = PADDLE_WIDTH, 
            height = PADDLE_HEIGHT, 
            speed = PADDLE_SPEED, 
            up_key = pygame.K_w, 
            down_key = pygame.K_s,
            color = COLOR_WHITE
        )
        
        self.right_paddle = Paddle(
            x = paddle_right_x, 
            y = paddle_y, 
            width = PADDLE_WIDTH, 
            height = PADDLE_HEIGHT, 
            speed = PADDLE_SPEED, 
            up_key = pygame.K_UP, 
            down_key = pygame.K_DOWN,
            color = COLOR_WHITE
        )
        
        self.ball = Ball(
            size = BALL_SIZE, 
            speed = BALL_SPEED, 
            color = COLOR_WHITE
        )

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_RETURN:
                    if self.state in [GameState.STARTING, GameState.GAME_OVER]:
                        self.left_paddle.score = 0
                        self.right_paddle.score = 0
                        self.reset_round()
                        self.state = GameState.PLAYING
                elif event.key == pygame.K_f:
                    self.toggle_fullscreen()

    def toggle_fullscreen(self):
        pygame.display.toggle_fullscreen()
        self.full_screen = not self.full_screen

    def reset_round(self):
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.round_start_time = pygame.time.get_ticks()

    def update(self):
        if self.state != GameState.PLAYING:
            return
        pressed_keys = pygame.key.get_pressed()
        self.left_paddle.move(pressed_keys)
        self.right_paddle.move(pressed_keys)
        if pygame.time.get_ticks() - self.round_start_time > START_DELAY_MS:
            self.ball.update()
            self.ball.bounce_edges()
            self.ball.check_paddle_collision(self.left_paddle, self.right_paddle)
            self.check_scoring()

    def check_scoring(self):
        if self.ball.position.x > SCREEN_WIDTH:
            self.left_paddle.score += 1
            if self.left_paddle.score >= WINNING_SCORE:
                self.state = GameState.GAME_OVER
            else:
                self.reset_round()
        elif self.ball.position.x < 0:
            self.right_paddle.score += 1
            if self.right_paddle.score >= WINNING_SCORE:
                self.state = GameState.GAME_OVER
            else:
                self.reset_round()
                
    def draw(self):
        self.screen.fill(COLOR_BLACK)

        if self.state == GameState.STARTING:
            self.screen.blit(self.text_pong, (SCREEN_WIDTH // 2 - 330, SCREEN_HEIGHT // 2 - 60))
            self.screen.blit(self.text_start, (SCREEN_WIDTH // 2 - 330, SCREEN_HEIGHT // 2 + 20))

        elif self.state == GameState.GAME_OVER:
            over_rect = self.text_game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            self.screen.blit(self.text_game_over, over_rect)
            if self.left_paddle.score >= WINNING_SCORE:
                won_rect = self.text_left_player_won.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(self.text_left_player_won, won_rect)
            elif self.right_paddle.score >= WINNING_SCORE:
                won_rect = self.text_right_player_won.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(self.text_right_player_won, won_rect)

        if self.state != GameState.STARTING:
            left_score_text = self.font.render(str(self.left_paddle.score), False, COLOR_WHITE)
            right_score_text = self.font.render(str(self.right_paddle.score), False, COLOR_WHITE)
            self.screen.blit(left_score_text, (SCREEN_WIDTH // 2 - 150, 20))
            self.screen.blit(right_score_text, (SCREEN_WIDTH // 2 + 100, 20))
            self.left_paddle.draw()
            self.right_paddle.draw()

        self.ball.draw()
        pygame.display.flip()