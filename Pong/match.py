import pygame
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from dataclasses import dataclass
import utility
from paddle import Paddle
from ball import Ball
import numpy as np
import yaml
import io

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

@dataclass
class Paddles:
    left: Paddle
    right: Paddle


class Match:
    def __init__(self, mode: str):
        self.paddles: Paddles
        self.left_score = 0
        self.right_score = 0
        self.balls = []
        self.number_of_bounces = 0
        self.mode = mode

    def read_game_settings(self, dificulty: str):
        with io.open("game_settings.yaml", "r") as stream:
            data = yaml.safe_load(stream)

        dificulty_settings = data['dificulties'][dificulty]
        return dificulty_settings

    def setup_game(self, dificulty_settings):
        left_paddle = Paddle(10, utility.WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH,
                                    PADDLE_HEIGHT, dificulty_settings['paddle_speed'])

        right_paddle = Paddle(utility.WINDOW_WIDTH - 10 - PADDLE_WIDTH,
                                     utility.WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH,
                                     PADDLE_HEIGHT, dificulty_settings['paddle_speed'])

        self.paddles = Paddles(left=left_paddle, right=right_paddle)

        ball_instance = Ball(utility.WINDOW_WIDTH // 2, utility.WINDOW_HEIGHT // 2, BALL_RADIUS,
                                  dificulty_settings['ball_starting_speed'], dificulty_settings['ball_max_speed'],
                                  dificulty_settings['ball_speed_modifier'])

        self.balls.append(ball_instance)

    def spawn_ball(self, dificulty_settings):
        if len(self.balls) == dificulty_settings['max_balls']:
            return

        ball_instance = Ball(utility.WINDOW_WIDTH // 2, utility.WINDOW_HEIGHT // 2, BALL_RADIUS,
                                  dificulty_settings['ball_starting_speed'], dificulty_settings['ball_max_speed'],
                                  dificulty_settings['ball_speed_modifier'])

        self.balls.append(ball_instance)

    def draw_match(self):
        utility.WINDOW.fill(utility.BACKGROUND_COLOR)

        left_score_text = utility.NORMAL_FONT.render(f"{self.left_score}", 1, utility.WHITE_COLOR)
        right_score_text = utility.NORMAL_FONT.render(f"{self.right_score}", 1, utility.WHITE_COLOR)

        utility.WINDOW.blit(left_score_text, (utility.WINDOW_WIDTH // 4 - left_score_text.get_width() // 2, 20))
        utility.WINDOW.blit(right_score_text,
                              (utility.WINDOW_WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))

        self.paddles.left.draw(utility.WINDOW)
        self.paddles.right.draw(utility.WINDOW)

        # middle dashed line
        for i in range(10, utility.WINDOW_HEIGHT, utility.WINDOW_HEIGHT // 20):
            if i % 2 == 1:
                continue

            pygame.draw.rect(utility.WINDOW, utility.WHITE_COLOR,
                             (utility.WINDOW_WIDTH // 2 - 2, i, 4, utility.WINDOW_HEIGHT // 20))

        for ball in self.balls:
            ball.draw(utility.WINDOW)

        pygame.display.update()

    def handle_paddle_movement_keyboard(self, keys):
        if keys[pygame.K_w]:
            self.paddles.left.move(up=True)

        if keys[pygame.K_s]:
            self.paddles.left.move(up=False)

        if keys[pygame.K_UP]:
            self.paddles.right.move(up=True)

        if keys[pygame.K_DOWN]:
            self.paddles.right.move(up=False)

    def handle_paddle_movement_hands(self, cap, detector):
        # hand detection (for now local with 2 hands)
        success, img = cap.read()
        hands, img = detector.findHands(img, draw=True, flipType=True)

        if hands:
            for hand in hands:
                # get final position
                _, y, _, _ = hand["bbox"]
                y -= self.paddles.left.height // 2

                # check for boundaries
                y = np.clip(y, 0, utility.WINDOW_HEIGHT)

                # check hand
                if hand["type"] == "Left":
                    self.paddles.left.y = y
                if hand["type"] == "Right":
                    self.paddles.right.y = y

        cv2.imshow("Hand Position Debug", img)

    def handle_paddle_movement(self, keys, cap, detector):
        self.handle_paddle_movement_hands(cap, detector)
        self.handle_paddle_movement_keyboard(keys)

    def handle_input(self, cap, detector):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()

        self.handle_paddle_movement(keys, cap, detector)

    def ball_collided_with_paddle(self, ball_instance: Ball, paddle_instance):
        self.number_of_bounces += 1

        ball_instance.x_velocity *= -1

        middle_y = paddle_instance.y + paddle_instance.height / 2
        difference_in_y = middle_y - ball_instance.y
        reduction_factor = (paddle_instance.height / 2) / ball_instance.max_velocity
        y_velocity = difference_in_y / reduction_factor
        ball_instance.y_velocity = -1 * y_velocity

        ball_instance.increase_speed()

    def handle_collision(self, ball_instance):
        # celling collision
        if ball_instance.y + ball_instance.radius >= utility.WINDOW_HEIGHT:
            ball_instance.y_velocity *= -1
        elif ball_instance.y - ball_instance.radius <= 0:
            ball_instance.y_velocity *= -1

        if ball_instance.x_velocity < 0:
            # left paddle collision
            if self.paddles.left.y <= ball_instance.y <= self.paddles.left.y + self.paddles.left.height:
                if ball_instance.x - ball_instance.radius <= self.paddles.left.x + self.paddles.left.width:
                    self.ball_collided_with_paddle(ball_instance, self.paddles.left)
        else:
            # right paddle collision
            if self.paddles.right.y <= ball_instance.y <= self.paddles.right.y + self.paddles.right.height:
                if ball_instance.x + ball_instance.radius >= self.paddles.right.x:
                    self.ball_collided_with_paddle(ball_instance, self.paddles.right)

    def handle_player_win(self, win_text):
        text = utility.NORMAL_FONT.render(win_text, 1, utility.WHITE_COLOR)

        pygame.draw.rect(utility.WINDOW, utility.BACKGROUND_COLOR, (
            utility.WINDOW_WIDTH // 2 - text.get_width() // 2, utility.WINDOW_HEIGHT // 2 - text.get_height() // 2,
            text.get_width(), text.get_height()))

        utility.WINDOW.blit(text, (
        utility.WINDOW_WIDTH // 2 - text.get_width() // 2, utility.WINDOW_HEIGHT // 2 - text.get_height() // 2))

        pygame.display.update()
        pygame.time.delay(5000)

    def reset_game(self, dificulty_settings):
        global left_score
        global right_score

        left_score = 0
        right_score = 0

        self.balls.clear()
        self.spawn_ball(dificulty_settings)

        self.paddles.left.reset()
        self.paddles.right.reset()

    def start_match(self):

        clock = pygame.time.Clock()
        cap = cv2.VideoCapture(0)

        if self.mode == "single":
            max_hands = 1
        else:
            max_hands = 2

        detector = HandDetector(staticMode=False, maxHands=max_hands, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)
        dificulty_settings = self.read_game_settings(utility.DIFFICULTY)
        self.setup_game(dificulty_settings)

        while True:
            clock.tick(utility.FPS)

            if self.number_of_bounces > 5:
                self.spawn_ball(dificulty_settings)
                self.number_of_bounces = 0

            self.draw_match()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.handle_input(cap, detector)

            for ball in self.balls:
                ball.move()
                self.handle_collision(ball)

                if ball.x < 0:
                    self.right_score += 1

                    if len(self.balls) > 1:
                        self.balls.remove(ball)
                    else:
                        ball.reset()
                elif ball.x > utility.WINDOW_WIDTH:
                    self.left_score += 1

                    if len(self.balls) > 1:
                        self.balls.remove(ball)
                    else:
                        ball.reset()

            won = False

            if self.left_score >= utility.WINNING_SCORE:
                won = True
                win_text = "Left Player Won!"
            elif self.right_score >= utility.WINNING_SCORE:
                won = True
                win_text = "Right Player Won!"

            if won:
                self.draw_match()
                self.handle_player_win(win_text)
                self.reset_game(dificulty_settings)
