import pygame
from entities.player import Player
from pathlib import Path
from .background import Background
from interfaces.pause import PauseMenu
from entities.effects import XSpeedModifier

WALL_TEXTURES = Path("assets/images/wall-textures")
FULLSCREEN = True


class Level1:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.player = Player(
            pos=self.screen_rect.center,
            sprite_name="gecko-sprite.png",
            hitbox=pygame.Rect(252, 0, 249, 573),
        )

        texture = pygame.image.load(WALL_TEXTURES / "BrokenWallA.png").convert()
        texture = pygame.transform.scale(texture, (512, 512))
        self.background = Background(texture, self.screen, speed=300)

        self.pause = False

        self.distance = 0
        self.distance_increase_speed = 1  # 1 per second
        self.end_distance = 100

        self.pause_menu = PauseMenu(self)

        self.speed_potion = XSpeedModifier(self.player, 2, 2)
        self.slow_potion = XSpeedModifier(self.player, 0.333333, 5)


    def pause(self):
        self.pause = True


    def unpause(self):
        self.pause = False


    def to_menu(self):
        self.game.change_scene("menu")


    def quit(self):
        self.game.quit()

    
    def handle_events(self, event):
        """ Handles ponctual events specific to level1 """
        if event.type == pygame.KEYDOWN: # if a key is pressed
            if event.key == pygame.K_ESCAPE:
                if self.pause:
                    self.pause = False
                else:
                    self.pause = True

            elif event.key == pygame.K_a:
                self.speed_potion.activate()
            elif event.key == pygame.K_z:
                self.slow_potion.activate()

        self.pause_menu.handle_events(event)


    def update(self, dt):
        if not self.pause:
            self.player.update(dt)
            self.background.update(dt)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_q] or keys[pygame.K_LEFT]:
                self.player.move_left(dt)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.player.move_right(dt)


    def draw(self):
        self.background.draw()
        self.player.draw(self.screen)

        if self.pause:
            self.pause_menu.draw()
