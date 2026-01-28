import pygame
from interfaces.button import Button   


class PauseMenu:
    def __init__(self, calling_scene):
        self.calling_scene = calling_scene
        self.screen = calling_scene.screen
        self.screen_rect = self.screen.get_rect()

        # --- Overlay ---
        self.overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 100, 100))

        # --- Central pannel ---
        panel_width = 400
        panel_height = 370
        self.panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
        self.panel_rect.center = self.screen_rect.center

        # --- Font ---
        self.font = pygame.font.Font(None, 36)

        # --- Boutons ---
        btn_width = 200
        btn_height = 50
        btn_x = self.panel_rect.centerx - btn_width // 2

        self.resume_button = Button(
            btn_x,
            self.panel_rect.top + 100,
            btn_width,
            btn_height,
            "Resume",
            self.font,
            (180, 220, 180),
            (220, 255, 220),
            action=self.resume
        )

        self.menu_button = Button(
            btn_x,
            self.panel_rect.top + 170,
            btn_width,
            btn_height,
            "Menu",
            self.font,
            (220, 180, 180),
            (255, 220, 220),
            action=self.to_menu
        )

        self.quit_button = Button(
            btn_x,
            self.panel_rect.top + 240,
            btn_width,
            btn_height,
            "Quit",
            self.font,
            (220, 180, 180),
            (255, 220, 220),
            action=self.quit
        )


    # ---------------- ACTIONS ----------------

    def resume(self):
        print("resume")
        self.calling_scene.unpause()


    def to_menu(self):
        self.calling_scene.to_menu()


    def quit(self):
        self.calling_scene.quit()


    # ---------------- EVENTS ----------------

    def handle_events(self, event):
        self.resume_button.handle_event(event)
        self.menu_button.handle_event(event)
        self.quit_button.handle_event(event)

        """
        # Escape = resume
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.resume()
        """
            
    # ---------------- DRAW ----------------

    def draw(self):
        # Assombrir l'écran
        self.screen.blit(self.overlay, (0, 0))

        # Panneau
        pygame.draw.rect(self.screen, (230, 230, 230), self.panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, (120, 120, 120), self.panel_rect, 3, border_radius=12)

        # Titre
        title = self.font.render("Paused", True, (30, 30, 30))
        title_rect = title.get_rect(center=(self.panel_rect.centerx, self.panel_rect.top + 40))
        self.screen.blit(title, title_rect)

        # Boutons
        self.resume_button.draw(self.screen)
        self.menu_button.draw(self.screen)
        self.quit_button.draw(self.screen)
