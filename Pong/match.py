import pygame
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from dataclasses import dataclass
import utility
from paddle import Paddle
from ball import Ball
import numpy as np
import os
import yaml
import io

pygame.mixer.init()

paddleSound = pygame.mixer.Sound(os.path.join(utility.SOUND_FOLDER, 'paddleCollision.mp3'))
paddleSound.set_volume(0.1)

pointSound = pygame.mixer.Sound(os.path.join(utility.SOUND_FOLDER, 'pointScore.mp3'))
pointSound.set_volume(0.1)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7


@dataclass
class Paddles:
    left: Paddle
    right: Paddle


class Match:
    def __init__(self, game, mode: str):
        self.paddles: Paddles
        self.left_score = 0
        self.right_score = 0
        self.balls = []
        self.number_of_bounces = 0
        self.mode = mode
        self.game = game

    def setup_game(self, dificulty_settings):
        left_paddle = Paddle(10, utility.WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2 - utility.BOTTOM_OFFSET // 2,
                             PADDLE_WIDTH, PADDLE_HEIGHT, dificulty_settings['paddle_speed'])

        right_paddle = Paddle(utility.WINDOW_WIDTH - 10 - PADDLE_WIDTH,
                              utility.WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2 - utility.BOTTOM_OFFSET // 2,
                              PADDLE_WIDTH, PADDLE_HEIGHT, dificulty_settings['paddle_speed'])

        self.paddles = Paddles(left=left_paddle, right=right_paddle)

        ball_instance = Ball(utility.WINDOW_WIDTH // 2, utility.WINDOW_HEIGHT // 2 - utility.BOTTOM_OFFSET // 2,
                             BALL_RADIUS, dificulty_settings['ball_starting_speed'],
                             dificulty_settings['ball_max_speed'], dificulty_settings['ball_speed_modifier'])

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

        # draw the bottom area of the game
        pygame.draw.rect(utility.WINDOW, utility.WHITE_COLOR,
                         (0, utility.WINDOW_HEIGHT - utility.BOTTOM_OFFSET,
                          utility.WINDOW_WIDTH, utility.BOTTOM_OFFSET))

        left_score_text = utility.NORMAL_FONT.render(f"{self.left_score}", 1, utility.BLACK_COLOR)
        right_score_text = utility.NORMAL_FONT.render(f"{self.right_score}", 1, utility.BLACK_COLOR)

        utility.WINDOW.blit(left_score_text, (utility.WINDOW_WIDTH // 4 - left_score_text.get_width() // 2,
                                              utility.WINDOW_HEIGHT - 90))
        utility.WINDOW.blit(right_score_text,
                            (utility.WINDOW_WIDTH * (3 / 4) - right_score_text.get_width() // 2,
                             utility.WINDOW_HEIGHT - 90))

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

    def ai_plays(self):
        miss_offset = 0
        if self.game.dificulty == "easy":
            miss_offset += 6
        if self.game.dificulty == "medium":
            miss_offset += 4
        if self.game.dificulty == "hard":
            miss_offset += 2

        # find nearest ball
        min_dist = utility.WINDOW_WIDTH
        ind = 0
        for i, ball in enumerate(self.balls):
            if self.paddles.right.x - ball.x < min_dist:
                min_dist = self.paddles.right.x - ball.x
                ind = i

        # verify paddle position with the nearest ball position
        if (self.paddles.right.y + self.paddles.right.height) + miss_offset < self.balls[ind].y:
            return 2
        if self.paddles.right.y - miss_offset > self.balls[ind].y:
            return 1
        return 0

    def handle_paddle_movement_keyboard(self, keys):
        if keys[pygame.K_w]:
            self.paddles.left.move(up=True)

        if keys[pygame.K_s]:
            self.paddles.left.move(up=False)

        if self.mode == "multi":
            if keys[pygame.K_UP]:
                self.paddles.right.move(up=True)

            if keys[pygame.K_DOWN]:
                self.paddles.right.move(up=False)

    def handle_paddle_movement_hands(self, cap, detector):
        # hand detection (for now local with 2 hands)
        success, img = cap.read()
        hands, img = detector.findHands(img, draw=True, flipType=True)

        cv2.imshow("Hand Position Debug", img)

        if hands:
            for hand in hands:
                # get final position
                _, y, _, _ = hand["bbox"]
                y -= self.paddles.left.height // 2

                y = np.clip(y, 0, 270)

                # check hand
                if hand["type"] == "Left":
                    self.paddles.left.y = y

                if self.mode == "multi":
                    if hand["type"] == "Right":
                        self.paddles.right.y = y
                elif self.mode == "single":
                    if hand["type"] == "Right":
                        self.paddles.left.y = y

    def handle_paddle_movement(self, keys, cap, detector):
        self.handle_paddle_movement_hands(cap, detector)
        self.handle_paddle_movement_keyboard(keys)

        if self.mode == "single":
            if self.ai_plays() == 1:
                self.paddles.right.move(up=True)
            elif self.ai_plays() == 2:
                self.paddles.right.move(up=False)

    def handle_input(self, cap, detector):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()

        self.handle_paddle_movement(keys, cap, detector)

    def ball_collided_with_paddle(self, ball_instance: Ball, paddle_instance):
        pygame.mixer.Sound.play(paddleSound)
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
        if ball_instance.y + ball_instance.radius >= utility.WINDOW_HEIGHT - utility.BOTTOM_OFFSET:
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
        cv2.destroyAllWindows()
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

        detector = HandDetector(staticMode=False, maxHands=max_hands, modelComplexity=1, detectionCon=0.5,
                                minTrackCon=0.5)

        if self.game.dificulty is not None:
            dificulty_settings = self.game.dificulty
        else:
            dificulty_settings = self.game.read_game_settings("medium")

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
                    pygame.mixer.Sound.play(pointSound)
                    self.right_score += 1

                    if len(self.balls) > 1:
                        self.balls.remove(ball)
                    else:
                        ball.reset()
                elif ball.x > utility.WINDOW_WIDTH:
                    pygame.mixer.Sound.play(pointSound)
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
                self.game.isPlaying = False
                break
