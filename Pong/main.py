import pygame
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

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


def draw(window, paddles, ball_instance):
    window.fill(constants.BACKGROUND_COLOR)

    left_score_text = constants.TEXT_FONT.render(f"{left_score}", 1, constants.WHITE_COLOR)
    right_score_text = constants.TEXT_FONT.render(f"{right_score}", 1, constants.WHITE_COLOR)

    window.blit(left_score_text, (constants.WINDOW_WIDTH // 4 - left_score_text.get_width() // 2, 20))
    window.blit(right_score_text, (constants.WINDOW_WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(constants.WINDOW)

    # middle dashed line
    for i in range(10, constants.WINDOW_HEIGHT, constants.WINDOW_HEIGHT // 20):
        if i % 2 == 1:
            continue

        pygame.draw.rect(window, constants.WHITE_COLOR,
                         (constants.WINDOW_WIDTH // 2 - 2, i, 4, constants.WINDOW_HEIGHT // 20))

    ball_instance.draw(window)

    pygame.display.update()


def handle_collision(ball_instance, left_paddle, right_paddle):
    # celling collision
    if ball_instance.y + ball_instance.radius >= constants.WINDOW_HEIGHT:
        ball_instance.y_velocity *= -1
    elif ball_instance.y - ball_instance.radius <= 0:
        ball_instance.y_velocity *= -1

    if ball_instance.x_velocity < 0:
        # left paddle collision
        if ball_instance.y >= left_paddle.y and ball_instance.y <= left_paddle.y + left_paddle.height:
            if ball_instance.x - ball_instance.radius <= left_paddle.x + left_paddle.width:
                ball_collided_with_paddle(ball_instance, left_paddle)
    else:
        # right paddle collision
        if ball_instance.y >= right_paddle.y and ball_instance.y <= right_paddle.y + right_paddle.height:
            if ball_instance.x + ball_instance.radius >= right_paddle.x:
                ball_collided_with_paddle(ball_instance, right_paddle)


def ball_collided_with_paddle(ball_instance, paddle_instance):
    ball_instance.x_velocity *= -1

    middle_y = paddle_instance.y + paddle_instance.height / 2
    difference_in_y = middle_y - ball_instance.y
    reduction_factor = (paddle_instance.height / 2) / ball_instance.MAX_VELOCITY
    y_velocity = difference_in_y / reduction_factor
    ball_instance.y_velocity = -1 * y_velocity



def handle_paddle_movement(keys, left_paddle, right_paddle):
    handle_paddle_movement_hands(left_paddle, right_paddle)
    handle_paddle_movement_keyboard(keys, left_paddle, right_paddle)


def handle_paddle_movement_hands(left_paddle, right_paddle):
    # hand detection (for now local with 2 hands)
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:
        for hand in hands:
            # get final position
            _, y, _, _ = hand["bbox"]
            y -= left_paddle.height // 2

            # check for boundaries
            y = np.clip(y, 0, constants.WINDOW_HEIGHT)

            # check hand
            if hand["type"] == "Left":
                left_paddle.y = y
            if hand["type"] == "Right":
                right_paddle.y = y

    cv2.imshow("Hand Position Debug", img)


def handle_paddle_movement_keyboard(keys, left_paddle, right_paddle):
    if keys[pygame.K_w]:
        left_paddle.move(up=True)

    if keys[pygame.K_s]:
        left_paddle.move(up=False)

    if keys[pygame.K_UP]:
        right_paddle.move(up=True)

    if keys[pygame.K_DOWN]:
        right_paddle.move(up=False)


def handle_input(left_paddle, right_paddle):
    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    handle_paddle_movement(keys, left_paddle, right_paddle)


def handle_player_win(win_text, ):
    text = constants.TEXT_FONT.render(win_text, 1, constants.WHITE_COLOR)

    pygame.draw.rect(constants.WINDOW, constants.BACKGROUND_COLOR, (
        constants.WINDOW_WIDTH // 2 - text.get_width() // 2, constants.WINDOW_HEIGHT // 2 - text.get_height() // 2,
        text.get_width(), text.get_height()))
    
    constants.WINDOW.blit(text, (constants.WINDOW_WIDTH // 2 - text.get_width() // 2, constants.WINDOW_HEIGHT // 2 - text.get_height() // 2))

    pygame.display.update()
    pygame.time.delay(5000)


def reset_game(ball_instance, left_paddle, right_paddle):
    global left_score
    global right_score
    
    left_score = 0
    right_score = 0
    ball_instance.reset()
    left_paddle.reset()
    right_paddle.reset()


def main():
    global left_score
    global right_score

    run = True
    clock = pygame.time.Clock()

    left_paddle = paddle.Paddle(10, constants.WINDOW_HEIGHT // 2 - paddle.PADDLE_HEIGHT // 2, paddle.PADDLE_WIDTH,
                                paddle.PADDLE_HEIGHT)
    
    right_paddle = paddle.Paddle(constants.WINDOW_WIDTH - 10 - paddle.PADDLE_WIDTH,
                                 constants.WINDOW_HEIGHT // 2 - paddle.PADDLE_HEIGHT // 2, paddle.PADDLE_WIDTH,
                                 paddle.PADDLE_HEIGHT)

    ball_instance = ball.Ball(constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2, ball.BALL_RADIUS)

    while run:
        clock.tick(constants.FPS)
        draw(constants.WINDOW, [left_paddle, right_paddle], ball_instance)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        handle_input(left_paddle, right_paddle)
        
        ball_instance.move()

        handle_collision(ball_instance, left_paddle, right_paddle)

        if ball_instance.x < 0:
            right_score += 1
            ball_instance.reset()
        elif ball_instance.x > constants.WINDOW_WIDTH:
            left_score += 1
            ball_instance.reset()

        won = False

        if left_score >= constants.WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= constants.WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            draw(constants.WINDOW, [left_paddle, right_paddle], ball_instance, left_score, right_score)

            handle_player_win(win_text)
            
            reset_game(left_score, right_score, ball_instance, left_paddle, right_paddle)
            
    pygame.quit()


if __name__ == '__main__':
    main()
