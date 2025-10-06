
import pygame
import sys

class PongGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong")
        self.WHITE, self.BLACK = (255,255,255), (0,0,0)
        self.PADDLE_WIDTH, self.PADDLE_HEIGHT, self.BALL_SIZE = 15, 100, 20
        self.left_paddle = pygame.Rect(30, self.HEIGHT//2-50, 15, 100)
        self.right_paddle = pygame.Rect(self.WIDTH-45, self.HEIGHT//2-50, 15, 100)
        self.ball = pygame.Rect(self.WIDTH//2-10, self.HEIGHT//2-10, 20, 20)
        self.ball_vel_x, self.ball_vel_y, self.left_vel = 10, 5, 0
        self.font = pygame.font.SysFont(None, 55)
        self.score_left, self.score_right = 0, 0
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP: self.left_vel = -7
                    if e.key == pygame.K_DOWN: self.left_vel = 7
                if e.type == pygame.KEYUP:
                    if e.key in [pygame.K_UP, pygame.K_DOWN]: self.left_vel = 0

            self.left_paddle.y = max(0, min(self.HEIGHT-100, self.left_paddle.y + self.left_vel))
            self.right_paddle.y = max(0, min(self.HEIGHT-100, self.right_paddle.y + (6 if self.right_paddle.centery < self.ball.centery else -6 if self.right_paddle.centery > self.ball.centery else 0)))
            self.ball.x += self.ball_vel_x; self.ball.y += self.ball_vel_y
            if self.ball.top <= 0 or self.ball.bottom >= self.HEIGHT: self.ball_vel_y *= -1
            if self.ball.colliderect(self.left_paddle) or self.ball.colliderect(self.right_paddle): self.ball_vel_x *= -1
            if self.ball.left <= 0:
                self.score_right += 1; self.ball.x, self.ball.y = self.WIDTH//2-10, self.HEIGHT//2-10; self.ball_vel_x *= -1
            if self.ball.right >= self.WIDTH:
                self.score_left += 1; self.ball.x, self.ball.y = self.WIDTH//2-10, self.HEIGHT//2-10; self.ball_vel_x *= -1
            self.WIN.fill(self.BLACK)
            [pygame.draw.rect(self.WIN, self.WHITE, p) for p in [self.left_paddle, self.right_paddle]]
            pygame.draw.ellipse(self.WIN, self.WHITE, self.ball)
            pygame.draw.aaline(self.WIN, self.WHITE, (self.WIDTH//2,0), (self.WIDTH//2,self.HEIGHT))
            self.WIN.blit(self.font.render(f"{self.score_left}   {self.score_right}", True, self.WHITE), (self.WIDTH//2-50, 20))
            pygame.display.flip(); self.clock.tick(60)

def show_menu(win, width, height, font):
    win.fill((0,0,0))
    title = font.render("PONG", True, (255,255,255))
    start = font.render("Stiskni ENTER pro start", True, (255,255,255))
    win.blit(title, (width//2 - title.get_width()//2, height//2 - 80))
    win.blit(start, (width//2 - start.get_width()//2, height//2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

if __name__ == "__main__":
    game = PongGame()
    show_menu(game.WIN, game.WIDTH, game.HEIGHT, game.font)
    game.run()
