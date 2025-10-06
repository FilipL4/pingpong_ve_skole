
import pygame
import sys

class PongGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.PADDLE_WIDTH, self.PADDLE_HEIGHT = 15, 100
        self.BALL_SIZE = 20

        self.left_paddle = pygame.Rect(30, self.HEIGHT//2 - self.PADDLE_HEIGHT//2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.right_paddle = pygame.Rect(self.WIDTH - 45, self.HEIGHT//2 - self.PADDLE_HEIGHT//2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.ball = pygame.Rect(self.WIDTH//2 - self.BALL_SIZE//2, self.HEIGHT//2 - self.BALL_SIZE//2, self.BALL_SIZE, self.BALL_SIZE)

        self.ball_vel_x = 5
        self.ball_vel_y = 5
        self.left_vel = 0

        self.font = pygame.font.SysFont(None, 55)
        self.score_left = 0
        self.score_right = 0

        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.left_vel = -7
                    if event.key == pygame.K_DOWN:
                        self.left_vel = 7
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        self.left_vel = 0

            self.left_paddle.y += self.left_vel

            # AI pro pravou pálku
            if self.right_paddle.centery < self.ball.centery:
                self.right_paddle.y += 6
            elif self.right_paddle.centery > self.ball.centery:
                self.right_paddle.y -= 6

            # Omezení pohybu pravé pálky
            self.right_paddle.y = max(0, min(self.HEIGHT - self.PADDLE_HEIGHT, self.right_paddle.y))
            # Omezení pohybu levé pálky
            self.left_paddle.y = max(0, min(self.HEIGHT - self.PADDLE_HEIGHT, self.left_paddle.y))

            # Pohyb míčku
            self.ball.x += self.ball_vel_x
            self.ball.y += self.ball_vel_y

            # Kolize s horní/dolní hranou
            if self.ball.top <= 0 or self.ball.bottom >= self.HEIGHT:
                self.ball_vel_y *= -1

            # Kolize s pálkami
            if self.ball.colliderect(self.left_paddle) or self.ball.colliderect(self.right_paddle):
                self.ball_vel_x *= -1

            # Skórování
            if self.ball.left <= 0:
                self.score_right += 1
                self.ball.x, self.ball.y = self.WIDTH//2 - self.BALL_SIZE//2, self.HEIGHT//2 - self.BALL_SIZE//2
                self.ball_vel_x *= -1
            if self.ball.right >= self.WIDTH:
                self.score_left += 1
                self.ball.x, self.ball.y = self.WIDTH//2 - self.BALL_SIZE//2, self.HEIGHT//2 - self.BALL_SIZE//2
                self.ball_vel_x *= -1

            # Vykreslení
            self.WIN.fill(self.BLACK)
            pygame.draw.rect(self.WIN, self.WHITE, self.left_paddle)
            pygame.draw.rect(self.WIN, self.WHITE, self.right_paddle)
            pygame.draw.ellipse(self.WIN, self.WHITE, self.ball)
            pygame.draw.aaline(self.WIN, self.WHITE, (self.WIDTH//2, 0), (self.WIDTH//2, self.HEIGHT))

            score_text = self.font.render(f"{self.score_left}   {self.score_right}", True, self.WHITE)
            self.WIN.blit(score_text, (self.WIDTH//2 - score_text.get_width()//2, 20))

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = PongGame()
    game.run()
