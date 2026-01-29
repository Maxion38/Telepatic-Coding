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

        self.x_speed = 600
        self.y_speed = 400

        self.food = 100
        self.food_decrease_speed = 2  # 2 per seconds

        self.__face_right = True

        self.effects_list = []


    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)


    def set_x_speed(self, x_speed):
        self.x_speed = x_speed


    def set_y_speed(self, y_speed):
        self.y_speed = y_speed


    def move_left(self, dt):
        self.move(-self.x_speed * dt)


    def move_right(self, dt):
        self.move(self.x_speed * dt)


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


    def add_effect(self, effect):
        self.effects_list.append(effect)


    def remove_effect(self, effect):
        self.effects_list.remove(effect)


    def update(self, dt):
        self.food -= dt * self.food_decrease_speed
        # print(self.food)

        for effect in self.effects_list:
            effect.update(dt)


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if DEBUG:
            pygame.draw.rect(screen, (255, 255, 0), self.rect, 1)  # Show image rect
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)  # Show hitbox