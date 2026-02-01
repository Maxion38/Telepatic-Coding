import pygame


import pygame


class Overlay:
    def __init__(self, calling_scene, buttons, title, overlay_color=(0, 100, 50, 100)):
        self.calling_scene = calling_scene
        self.screen = calling_scene.screen
        self.screen_rect = self.screen.get_rect()

        self.BUTTONS_MARGIN = 20
        self.TOP_PADDING = 90
        self.BOTTOM_PADDING = 50

        self.buttons = buttons
        self.title = title

        # --- Overlay ---
        self.overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill(overlay_color)

        # --- Font ---
        self.font = pygame.font.Font(None, 36)

        # --- pannel height ---
        buttons_total_height = sum(button.rect.height for button in self.buttons)
        margins_total = self.BUTTONS_MARGIN * (len(self.buttons) - 1)

        panel_width = 400
        BASE_HEIGHT = self.TOP_PADDING + self.BOTTOM_PADDING
        panel_height = BASE_HEIGHT + buttons_total_height + margins_total

        self.panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
        self.panel_rect.center = self.screen_rect.center

        # --- Buttons ---
        y_offset = 0
        for button in self.buttons:
            button.rect.center = (
                self.panel_rect.centerx,
                self.panel_rect.top + self.TOP_PADDING + y_offset + button.rect.height // 2
            )
            y_offset += button.rect.height + self.BUTTONS_MARGIN


    def resume(self):
        print("resume")
        self.calling_scene.unpause()


    def to_menu(self):
        self.calling_scene.to_menu()


    def quit(self):
        self.calling_scene.quit()


    def handle_events(self, event):
        for button in self.buttons:        
            button.handle_event(event)


    def draw(self):
        # Assombrir l'écran
        self.screen.blit(self.overlay, (0, 0))

        # Panneau
        pygame.draw.rect(self.screen, (230, 230, 230), self.panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, (120, 120, 120), self.panel_rect, 3, border_radius=12)

        # Titre
        title = self.font.render(self.title, True, (30, 30, 30))
        title_rect = title.get_rect(center=(self.panel_rect.centerx, self.panel_rect.top + 40))
        self.screen.blit(title, title_rect)

        # Boutons
        for button in self.buttons:
            button.draw(self.screen)
