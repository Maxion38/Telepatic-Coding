import pygame
from entities.player import Player
from pathlib import Path
from .background import Background

WALL_TEXTURES = Path("assets/images/wall-textures")
FULLSCREEN = False


class Game:
    def __init__(self, fps=60):
        pygame.init()

        init_width, init_height = 1200, 600

        self.screen = (
            pygame.display.set_mode((init_width, init_height), pygame.FULLSCREEN) if FULLSCREEN
            else pygame.display.set_mode((init_width, init_height))
        )

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True

        screen_rect = self.screen.get_rect()
        self.player = Player(
            pos=screen_rect.center,
            sprite_name="gecko-sprite.png",
            hitbox=pygame.Rect(252, 0, 249, 573),
        )

        texture = pygame.image.load(WALL_TEXTURES / "BrokenWallA.png").convert()
        texture = pygame.transform.scale(texture, (512, 512))
        self.background = Background(texture, self.screen, speed=300)

        self.distance = 0
        self.distance_increase_speed = 1  # 1 per second
        self.end_distance = 100


    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


    def update(self, dt):
        if not self.player.update(dt):
            self.running = False
        self.background.update(dt)


    def draw(self):
        self.screen.fill((40, 40, 40))  
        self.background.draw()
        self.player.draw(self.screen)
        pygame.display.flip()
