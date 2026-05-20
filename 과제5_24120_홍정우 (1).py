import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLACK = (30, 30, 30)

class GameObject:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Player(GameObject):
    def __init__(self):
        super().__init__(WIDTH//2, HEIGHT-60, 40, 40, GREEN)
        self.speed = 5
        self.hp = 100

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.rect.clamp_ip(screen.get_rect())

    def hit(self, damage):
        self.hp -= damage

class Bullet(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 5, 10, WHITE)
        self.speed = -7

    def update(self):
        self.rect.y += self.speed

class Enemy(GameObject):
    def __init__(self):
        x = random.randint(0, WIDTH-40)
        super().__init__(x, -40, 40, 40, RED)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed

class Game:
    def __init__(self):
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.spawn_timer = 0
        self.font = pygame.font.SysFont("malgungothic", 24)

    def spawn_enemy(self):
        self.enemies.append(Enemy())

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)

    def shoot(self):
        bullet = Bullet(self.player.rect.centerx, self.player.rect.y)
        self.bullets.append(bullet)

    def update(self):
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.rect.colliderect(self.player.rect):
                self.player.hit(10)
                self.enemies.remove(enemy)
            elif enemy.rect.top > HEIGHT:
                self.enemies.remove(enemy)

        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break

        self.spawn_timer += 1
        if self.spawn_timer > 30:
            self.spawn_enemy()
            self.spawn_timer = 0

    def draw_ui(self):
        pygame.draw.rect(screen, RED, (10, 10, 200, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, 2 * self.player.hp, 20))
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 40))

    def draw(self):
        screen.fill(BLACK)
        self.player.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        self.draw_ui()

    def is_game_over(self):
        return self.player.hp <= 0

def main():
    game = Game()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.shoot()

        game.handle_input()
        game.update()
        game.draw()

        if game.is_game_over():
            pygame.quit()
            sys.exit()

        pygame.display.flip()

main()