import pygame
pygame.init()

import constants
import paddle
import ball

pygame.display.set_caption("Pong")

def draw(window, paddles, ball_instance, left_score, right_score):
    window.fill(constants.BACKGROUND_COLOR)

    left_score_text = constants.TEXT_FONT.render(f"{left_score}", 1, constants.WHITE_COLOR)
    right_score_text = constants.TEXT_FONT.render(f"{right_score}", 1, constants.WHITE_COLOR)

    window.blit(left_score_text, (constants.WINDOW_WIDTH // 4 - left_score_text.get_width() // 2, 20))
    window.blit(right_score_text, (constants.WINDOW_WIDTH * (3/4) - right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(constants.WINDOW)

    # middle dashed line
    for i in range(10, constants.WINDOW_HEIGHT, constants.WINDOW_HEIGHT//20):
        if i % 2 == 1:
            continue

        pygame.draw.rect(window, constants.WHITE_COLOR, (constants.WINDOW_WIDTH//2 - 2, i, 4, constants.WINDOW_HEIGHT//20))

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
                ball_instance.x_velocity *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball_instance.y
                reduction_factor = (left_paddle.height / 2) / ball_instance.MAX_VELOCITY
                y_velocity = difference_in_y / reduction_factor
                ball_instance.y_velocity = -1 * y_velocity
    else:
        # right paddle collision
        if ball_instance.y >= right_paddle.y and ball_instance.y <= right_paddle.y + right_paddle.height:
            if ball_instance.x + ball_instance.radius >= right_paddle.x:
                ball_instance.x_velocity *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball_instance.y
                reduction_factor = (right_paddle.height / 2) / ball_instance.MAX_VELOCITY
                y_velocity = difference_in_y / reduction_factor
                ball_instance.y_velocity = -1 * y_velocity


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    if keys[pygame.K_w]:
        left_paddle.move(up=True)
    
    if keys[pygame.K_s]:
        left_paddle.move(up=False)

    if keys[pygame.K_UP]:
        right_paddle.move(up=True)
    
    if keys[pygame.K_DOWN]:
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = paddle.Paddle(10, constants.WINDOW_HEIGHT//2 - paddle.PADDLE_HEIGHT//2, paddle.PADDLE_WIDTH, paddle.PADDLE_HEIGHT)
    right_paddle = paddle.Paddle(constants.WINDOW_WIDTH - 10 - paddle.PADDLE_WIDTH, constants.WINDOW_HEIGHT//2 - paddle.PADDLE_HEIGHT//2, paddle.PADDLE_WIDTH, paddle.PADDLE_HEIGHT)
    
    ball_instance = ball.Ball(constants.WINDOW_WIDTH//2, constants.WINDOW_HEIGHT//2, ball.BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(constants.FPS)
        draw(constants.WINDOW, [left_paddle, right_paddle], ball_instance, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

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

            text = constants.TEXT_FONT.render(win_text, 1, constants.WHITE_COLOR)
            pygame.draw.rect(constants.WINDOW, constants.BACKGROUND_COLOR, (constants.WINDOW_WIDTH//2 - text.get_width() // 2, constants.WINDOW_HEIGHT // 2 - text.get_height() // 2, text.get_width() , text.get_height()))
            constants.WINDOW.blit(text, (constants.WINDOW_WIDTH // 2 - text.get_width() // 2, constants.WINDOW_HEIGHT // 2 - text.get_height() // 2))

            pygame.display.update()
            pygame.time.delay(5000)

            left_score = 0
            right_score = 0
            ball_instance.reset()
            left_paddle.reset()
            right_paddle.reset()

    pygame.quit()

if __name__ == '__main__':
    main()