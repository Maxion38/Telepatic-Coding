import pygame
from scenes.level1 import Level1
from scenes.menu import Menu
from pygame._sdl2 import Window

FULLSCREEN = False


class Game:
    def __init__(self, fps=60):
        pygame.init()

        init_width, init_height = 1200, 600

        self.screen = (
            pygame.display.set_mode((init_width, init_height), pygame.FULLSCREEN) if FULLSCREEN
            else pygame.display.set_mode((init_width, init_height), pygame.RESIZABLE)
        )

        if not FULLSCREEN :
            Window.from_display_module().maximize()


        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True

        self.menu = Menu(self)
        self.level1 = Level1(self)

        self.current_scene = self.menu

    
    def quit(self):
        self.running = False


    def change_scene(self, scene_name):
        match scene_name:
            case "level1":
                self.current_scene = self.level1
            case "menu":
                self.current_scene = self.menu


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

            """
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            """
                    
            self.current_scene.handle_events(event)


    def update(self, dt):
        self.current_scene.update(dt)


    def draw(self):
        self.screen.fill((40, 40, 40))

        self.current_scene.draw()

        pygame.display.flip()
