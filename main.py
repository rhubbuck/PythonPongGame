from game_rules import Ball, Paddle
import pygame
import neat
import os

pygame.init()

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCORE_TEXT = pygame.font.SysFont('Verdana', 50)
HIT_TEXT = pygame.font.SysFont('Verdana', 14)


def draw(window, paddles, ball, left_score, right_score, left_hits, right_hits):
    window.fill(BLACK)
    left_score_text = SCORE_TEXT.render(f"{left_score}", True, WHITE)
    left_hit_text = HIT_TEXT.render(f"Hits: {left_hits}", True, WHITE)
    right_score_text = SCORE_TEXT.render(f"{right_score}", True, WHITE)
    right_hit_text = HIT_TEXT.render(f"Hits: {right_hits}", True, WHITE)
    window.blit(left_score_text, (WINDOW_WIDTH // 4 - left_score_text.get_width() // 2, 15))
    window.blit(left_hit_text, (WINDOW_WIDTH / 2.5 - left_score_text.get_width() / 2, 5))
    window.blit(right_score_text, (WINDOW_WIDTH * (3 / 4) -
                                   right_score_text.get_width() // 2, 15))
    window.blit(right_hit_text, (WINDOW_WIDTH * .58 - right_score_text.get_width() / 2, 5))

    for paddle in paddles:
        paddle.draw(window)

    for i in range(10, WINDOW_HEIGHT, WINDOW_HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(window, WHITE, (WINDOW_WIDTH // 2 - 5, i, 10, WINDOW_HEIGHT // 20))

    ball.draw(window)
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle, left_hits, right_hits):
    if ball.y + ball.radius >= WINDOW_HEIGHT:
        ball.y_velocity *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_velocity *= -1

    if ball.x_velocity < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.max_velocity
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                left_hits += 1

    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velocity *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.max_velocity
                y_velocity = difference_in_y / reduction_factor
                ball.y_velocity = -1 * y_velocity
                right_hits += 1
    return left_hits, right_hits


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.velocity >= 0:
        left_paddle.move(down=False)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.velocity + left_paddle.height <= WINDOW_HEIGHT:
        left_paddle.move(down=True)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.velocity >= 0:
        right_paddle.move(down=False)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.velocity + right_paddle.height <= WINDOW_HEIGHT:
        right_paddle.move(down=True)


def loop_game(ball, left_paddle, right_paddle, left_hits, right_hits):
    left_score = 0
    right_score = 0
    left_hits = 0
    right_hits = 0

    ball.move()
    handle_collision(ball, left_paddle, right_paddle, left_hits, right_hits)

    if ball.x < 0:
        right_score += 1
        ball.reset()
    elif ball.x > WINDOW_WIDTH:
        left_score += 1
        ball.reset()

    left_hits, right_hits = handle_collision(ball, left_paddle, right_paddle, left_hits, right_hits)

    return left_score, right_score, left_hits, right_hits



def main():
    left_hits = 0
    right_hits = 0
    global win_text
    run_program = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, WINDOW_HEIGHT // 2 - Paddle.height //
                         2)
    right_paddle = Paddle(WINDOW_WIDTH - 10 - Paddle.width, WINDOW_HEIGHT //
                          2 - Paddle.height // 2)
    ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, Ball.radius)

    left_score = 0
    right_score = 0
    left_hits = 0
    right_hits = 0

    while run_program:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score, left_hits, right_hits)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run_program = False
                break

        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        left_hits, right_hits = handle_collision(ball, left_paddle, right_paddle, left_hits, right_hits)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WINDOW_WIDTH:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= 10:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= 10:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = SCORE_TEXT.render(win_text, True, WHITE)
            WINDOW.blit(text, (WINDOW_WIDTH // 2 - text.get_width() //
                               2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(4000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()
