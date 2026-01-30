import pygame
from pathlib import Path
from helpers.blur import blur_image
from interfaces.button import Button

WALL_TEXTURES = Path("assets/images/wall-textures")
ASSETS = Path("assets/images")


class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.font = pygame.font.SysFont("Arial", 30)

        self.mossy_planks_texture = pygame.image.load(WALL_TEXTURES / "Mossy-Wooden-Planks.png").convert()
        self.mossy_planks_texture = pygame.transform.scale(self.mossy_planks_texture, (512, 512))

        self.grey_soil_texture = blur_image("assets/images/wall-textures/PlasterMossy.png")
        self.grey_soil_texture = pygame.transform.scale(self.grey_soil_texture, (512, 512))

        gecko_image = pygame.image.load(ASSETS / "gecko-sprite.png").convert_alpha()
        self.gecko_image = pygame.transform.scale_by(gecko_image, .77)
        self.gecko_image = pygame.transform.rotate(self.gecko_image, 50)

        self.start_button = Button(
            x=100, y=100, width=200, height=60,
            text="Démarrer",
            font=self.font,
            color=(60, 200, 100),
            hover_color=(100, 240, 140),
            action=self.start_game 
        )


    def start_game(self):
        self.game.change_scene("level1")


    def update(self, dt):
        pass


    def handle_events(self, event):
        self.start_button.handle_event(event=event)


    def draw(self):
        screen_w, screen_h = self.screen.get_size()

        left_width = int(screen_w * 0.15)
        right_width = int(screen_w * 0.15)
        center_width = screen_w - left_width - right_width

        # Textures zones
        self._tile_texture(self.grey_soil_texture, 0, 0, left_width, screen_h)
        self._tile_texture(self.mossy_planks_texture, left_width, 0, center_width, screen_h)
        self._tile_texture(self.grey_soil_texture, left_width + center_width, 0, right_width, screen_h)

        border_color = (198, 157, 90)  
        border_width = 10 

        pygame.draw.rect(self.screen, border_color, 
                        (left_width - border_width//2, 0, border_width, screen_h))
        pygame.draw.rect(self.screen, border_color, 
                        (left_width + center_width - border_width//2, 0, border_width, screen_h))

        # gecko
        gecko_rect = self.gecko_image.get_rect(center=self.screen_rect.center)
        self.screen.blit(self.gecko_image, gecko_rect)

        # start button
        self.start_button.rect.midbottom = self.screen_rect.midbottom
        self.start_button.rect.y -= 20
        self.start_button.draw(self.screen)


    def _tile_texture(self, texture, x_start, y_start, area_width, area_height):
        tex_w, tex_h = texture.get_size()

        # Fill zone by repeating texture
        for x in range(x_start, x_start + area_width, tex_w):
            for y in range(y_start, y_start + area_height, tex_h):
                self.screen.blit(texture, (x, y))
