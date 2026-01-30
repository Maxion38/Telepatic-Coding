import pygame
from pathlib import Path
from interfaces.gauge import Gauge

ASSETS = Path("assets/images")
DEBUG = False


class Player:
    def __init__(self, calling_scene, pos, sprite_name="gecko-sprite.png", scale=.33, hitbox="auto"):
        self.calling_scene = calling_scene
        self.screen = calling_scene.screen
        self.screen_rect = self.screen.get_rect()

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

        self.isAlive = True
        self.x_speed = 600
        self.y_speed = 400

        self.food = 100
        self.FOOD_DECREASE_SPEED = 5

        self.food_gauge = Gauge(False, 20, 200, (150, 150, 150), (200, 90, 30), self.food, self.food)
        self.food_gauge.rect.midleft = (
            self.screen_rect.left + 20,
            self.screen_rect.top + 20
        )

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
        if self.isAlive:
            for effect in self.effects_list:
                effect.update(dt)

            self.food -= dt * self.FOOD_DECREASE_SPEED
            self.food_gauge.decrease_capacity(dt * self.FOOD_DECREASE_SPEED)
            if self.food <= 0:
                print("You died")
                self.isAlive = False
                self.calling_scene.die()


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if DEBUG:
            pygame.draw.rect(screen, (255, 255, 0), self.rect, 1)  # Show image rect
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)  # Show hitbox

        self.food_gauge.draw(self.screen)