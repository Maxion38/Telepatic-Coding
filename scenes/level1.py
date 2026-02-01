import pygame
from entities.player import Player
from pathlib import Path
from .background import Background
from interfaces.overlayMenu import Overlay
from interfaces.gauge import Gauge
from interfaces.button import Button
from entities.effects import XSpeedModifier

WALL_TEXTURES = Path("assets/images/wall-textures")
FULLSCREEN = True


class Level1:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.DICTANCE_INCREASE_SPEED = 1  # 1 per second
        self.END_DISTANCE = 120

        self.distance = 0
        self.is_paused = False
        self.is_dead = False

        self.player = Player(
            pos=self.screen_rect.center,
            calling_scene=self,
            sprite_name="gecko-sprite.png",
            hitbox=pygame.Rect(252, 0, 249, 573),
        )

        self.resume_button = Button(200, 50, "Continuer", (60, 200, 100), (100, 240, 140), action=self.unpause)
        self.menu_button = Button(200, 50, "Menu", (60, 200, 100), (100, 240, 140), action=self.to_menu)
        self.quit_button = Button(200, 50, "Quitter", (220, 140, 200), (255, 180, 240), action=self.quit)
        self.pause_overlay = Overlay(self, [self.resume_button, self.menu_button, self.quit_button], "Pause")

        self.menu_button2 = Button(200, 50, "Menu", (60, 200, 100), (100, 240, 140), action=self.to_menu)
        self.quit_button2 = Button(200, 50, "Quitter", (220, 140, 200), (255, 180, 240), action=self.quit)
        self.died_overlay = Overlay(self, [self.menu_button2, self.quit_button2], "Vous êtes mort", (100, 0, 50, 100))

        self.distance_gauge = Gauge(True, 8, 300, (150, 150, 150), (255, 255, 255), self.END_DISTANCE, self.distance)
        self.distance_gauge.rect.midright = (
            self.screen_rect.right - 20,
            self.screen_rect.centery
        )

        self.speed_potion = XSpeedModifier(self.player, 2, 2)
        self.slow_potion = XSpeedModifier(self.player, 0.333333, 5)

        texture = pygame.image.load(WALL_TEXTURES / "BrokenWallA.png").convert()
        texture = pygame.transform.scale(texture, (312, 312))
        self.background = Background(texture, self.screen, speed=300)


    def die(self):
        self.pause()
        self.is_dead = True


    def pause(self):
        self.is_paused = True


    def unpause(self):
        self.is_paused = False


    def to_menu(self):
        self.game.change_scene("menu")


    def quit(self):
        self.game.quit()

    
    def handle_events(self, event):
        if self.is_dead:
            self.died_overlay.handle_events(event)
            return

        if self.is_paused:
            self.pause_overlay.handle_events(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not self.is_paused:
                self.is_paused = True
            elif event.key == pygame.K_ESCAPE and self.is_paused:
                self.is_paused = False # why doesn't it work ?
            elif event.key == pygame.K_a:
                self.speed_potion.activate()
            elif event.key == pygame.K_z:
                self.slow_potion.activate()


    def update(self, dt):
        if not self.is_paused:
            self.player.update(dt)
            self.background.update(dt)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_q] or keys[pygame.K_LEFT]:
                self.player.move_left(dt)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.player.move_right(dt)

            self.distance += dt * self.DICTANCE_INCREASE_SPEED
            self.distance_gauge.increase_capacity(dt * self.DICTANCE_INCREASE_SPEED)


    def draw(self):
        self.background.draw()
        self.player.draw(self.screen)

        if self.is_dead:
            self.died_overlay.draw()
        elif self.is_paused:
            self.pause_overlay.draw()

        self.distance_gauge.draw(self.screen)

