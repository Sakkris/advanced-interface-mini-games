import pygame
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from dataclasses import dataclass
import numpy as np
import yaml
import io

pygame.init()

import constants
import paddle
import ball

pygame.display.set_caption("Pong")

# set capture camera to default
cap = cv2.VideoCapture(0)

detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

left_score = 0
right_score = 0

@dataclass
class Paddles:
    left: paddle.Paddle
    right: paddle.Paddle

paddles: Paddles
balls = []


def draw():
    constants.WINDOW.fill(constants.BACKGROUND_COLOR)

    left_score_text = constants.TEXT_FONT.render(f"{left_score}", 1, constants.WHITE_COLOR)
    right_score_text = constants.TEXT_FONT.render(f"{right_score}", 1, constants.WHITE_COLOR)

    constants.WINDOW.blit(left_score_text, (constants.WINDOW_WIDTH // 4 - left_score_text.get_width() // 2, 20))
    constants.WINDOW.blit(right_score_text, (constants.WINDOW_WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))

    paddles.left.draw(constants.WINDOW)
    paddles.right.draw(constants.WINDOW)

    # middle dashed line
    for i in range(10, constants.WINDOW_HEIGHT, constants.WINDOW_HEIGHT // 20):
        if i % 2 == 1:
            continue

        pygame.draw.rect(constants.WINDOW, constants.WHITE_COLOR,
                         (constants.WINDOW_WIDTH // 2 - 2, i, 4, constants.WINDOW_HEIGHT // 20))
        
    for ball in balls:
        ball.draw(constants.WINDOW)

    pygame.display.update()


def handle_collision(ball_instance):
    # celling collision
    if ball_instance.y + ball_instance.radius >= constants.WINDOW_HEIGHT:
        ball_instance.y_velocity *= -1
    elif ball_instance.y - ball_instance.radius <= 0:
        ball_instance.y_velocity *= -1

    if ball_instance.x_velocity < 0:
        # left paddle collision
        if ball_instance.y >= paddles.left.y and ball_instance.y <= paddles.left.y + paddles.left.height:
            if ball_instance.x - ball_instance.radius <= paddles.left.x + paddles.left.width:
                ball_collided_with_paddle(ball_instance, paddles.left)
    else:
        # right paddle collision
        if ball_instance.y >= paddles.right.y and ball_instance.y <= paddles.right.y + paddles.right.height:
            if ball_instance.x + ball_instance.radius >= paddles.right.x:
                ball_collided_with_paddle(ball_instance, paddles.right)


def ball_collided_with_paddle(ball_instance: ball.Ball, paddle_instance):
    ball_instance.x_velocity *= -1

    middle_y = paddle_instance.y + paddle_instance.height / 2
    difference_in_y = middle_y - ball_instance.y
    reduction_factor = (paddle_instance.height / 2) / ball_instance.max_velocity
    y_velocity = difference_in_y / reduction_factor
    ball_instance.y_velocity = -1 * y_velocity

    ball_instance.increase_speed()


def handle_paddle_movement(keys):
    handle_paddle_movement_hands()
    handle_paddle_movement_keyboard(keys)


def handle_paddle_movement_hands():
    # hand detection (for now local with 2 hands)
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:
        for hand in hands:
            # get final position
            _, y, _, _ = hand["bbox"]
            y -= paddles.left.height // 2

            # check for boundaries
            y = np.clip(y, 0, constants.WINDOW_HEIGHT)

            # check hand
            if hand["type"] == "Left":
                paddles.left.y = y
            if hand["type"] == "Right":
                paddles.right.y = y

    cv2.imshow("Hand Position Debug", img)


def handle_paddle_movement_keyboard(keys):
    if keys[pygame.K_w]:
        paddles.left.move(up=True)

    if keys[pygame.K_s]:
        paddles.left.move(up=False)

    if keys[pygame.K_UP]:
        paddles.right.move(up=True)

    if keys[pygame.K_DOWN]:
        paddles.right.move(up=False)


def handle_input():
    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    handle_paddle_movement(keys)


def handle_player_win(win_text, ):
    text = constants.TEXT_FONT.render(win_text, 1, constants.WHITE_COLOR)

    pygame.draw.rect(constants.WINDOW, constants.BACKGROUND_COLOR, (
        constants.WINDOW_WIDTH // 2 - text.get_width() // 2, constants.WINDOW_HEIGHT // 2 - text.get_height() // 2,
        text.get_width(), text.get_height()))
    
    constants.WINDOW.blit(text, (constants.WINDOW_WIDTH // 2 - text.get_width() // 2, constants.WINDOW_HEIGHT // 2 - text.get_height() // 2))

    pygame.display.update()
    pygame.time.delay(5000)


def setup_game(dificulty_settings):
    global paddles
    global balls

    left_paddle = paddle.Paddle(10, constants.WINDOW_HEIGHT // 2 - paddle.PADDLE_HEIGHT // 2, paddle.PADDLE_WIDTH,
                                paddle.PADDLE_HEIGHT, dificulty_settings['paddle_speed'])
    
    right_paddle = paddle.Paddle(constants.WINDOW_WIDTH - 10 - paddle.PADDLE_WIDTH,
                                 constants.WINDOW_HEIGHT // 2 - paddle.PADDLE_HEIGHT // 2, paddle.PADDLE_WIDTH,
                                 paddle.PADDLE_HEIGHT, dificulty_settings['paddle_speed'])
    
    paddles = Paddles(left = left_paddle, right = right_paddle)

    ball_instance = ball.Ball(constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2, ball.BALL_RADIUS,
                              dificulty_settings['ball_starting_speed'], dificulty_settings['ball_max_speed'], dificulty_settings['ball_speed_modifier'])

    balls.append(ball_instance)


def reset_game():
    global left_score
    global right_score
    
    left_score = 0
    right_score = 0

    balls.clear()
    ball_instance = ball.Ball(constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2, ball.BALL_RADIUS)
    balls.append(ball_instance)

    paddles.left.reset()
    paddles.right.reset()


def read_game_settings(dificulty):
    with io.open("game_settings.yaml", "r") as stream:
        data = yaml.safe_load(stream)
    
    dificulty_settings = data['dificulties'][dificulty]

    return dificulty_settings


def main():
    global left_score
    global right_score

    run = True
    clock = pygame.time.Clock()

    dificulty_settings = read_game_settings("hard")

    setup_game(dificulty_settings)

    while run:
        clock.tick(constants.FPS)
        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        handle_input()
        
        for ball in balls:
            ball.move()
            handle_collision(ball)
        
            if ball.x < 0:
                right_score += 1

                if len(balls) > 1:
                    balls.remove(ball)
                else:
                    ball.reset()
            elif ball.x > constants.WINDOW_WIDTH:
                left_score += 1

                if len(balls) > 1:
                    balls.remove(ball)
                else:
                    ball.reset()

        won = False

        if left_score >= constants.WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= constants.WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            draw()

            handle_player_win(win_text)
            
            reset_game()
            
    pygame.quit()


if __name__ == '__main__':
    main()
