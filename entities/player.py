import pygame
from pathlib import Path

ASSETS = Path("assets/images")
DEBUG = False


class Player:
    def __init__(self, pos, sprite_name="gecko-sprite.png", scale=.33, hitbox="auto"):
        image = pygame.image.load(
            ASSETS / sprite_name
        ).convert_alpha()

        # Rescale the image
        self.image = pygame.transform.scale_by(image, scale)

        # Rect representing the image
        self.rect = self.image.get_rect(center=pos)

        # Rect representing the hitbox
        if type(hitbox) == pygame.Rect:  # Custom hitbox
            self.hitbox = hitbox
            self.__hitbox_offset = hitbox.x * scale, hitbox.y * scale
            self.hitbox = self.hitbox.scale_by(scale, scale)
            self.hitbox.x, self.hitbox.y = self.rect.x, self.rect.y
            self.hitbox.x += self.__hitbox_offset[0]
            self.hitbox.y += self.__hitbox_offset[1]
        else:                            # Default hitbox
            self.hitbox = self.rect.copy()
            self.__hitbox_offset = 0, 0

        self.speed = 600

        self.food = 100
        self.food_decrease_speed = 2  # 2 per seconds

        self.__face_right = True

    def update(self, dt):

        keys = pygame.key.get_pressed()

        # -- Player movement -- #

        # Go left
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.move(-self.speed * dt)
        # Go right
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move(self.speed * dt)

        # -- Quit -- #
        if keys[pygame.K_ESCAPE]:
            return False

        return True

        self.food -= dt * self.food_decrease_speed
        print(self.food)

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if DEBUG:
            pygame.draw.rect(screen, (255, 255, 0), self.rect, 1)  # Show image rect
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)  # Show hitbox

    def move(self, amount):
        if amount > 0:  # Move to the right
            # Flip the player if needed
            if not self.__face_right:
                self.flip()
                self.__face_right = True
                self.rect.x -= self.__hitbox_offset[0]

        else:  # Move to the left
            # Flip the player if needed
            if self.__face_right:
                self.flip()
                self.__face_right = False
                self.rect.x += self.__hitbox_offset[0]

        # Move the image and hitbox
        self.rect.x += amount
        self.hitbox.x += amount