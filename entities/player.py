import pygame
from pathlib import Path

ASSETS = Path("assets/images")

class Player:
    def __init__(self, pos):
        image = pygame.image.load(
            ASSETS / "gecko-sprite.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            image,
            (256, 256)
        )

        self.rect = self.image.get_rect(center=pos)
        self.speed = 600

        self.food = 100
        self.food_decrease_speed = 2 # 2 per seconds


    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.rect.x += self.speed * dt

        self.food -= dt * self.food_decrease_speed
        print(self.food)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
