class Background:
    def __init__(self, texture, screen, speed=100):
        """
        texture : Pygame surface (tileable)
        screen : Pygame surface of the screen
        speed : speed of vertical scrolling (px/sec)
        """
        self.screen = screen
        self.texture = texture
        self.speed = speed

        self.tex_width = texture.get_width()
        self.tex_height = texture.get_height()

        self.offset = 0

    def update(self, dt):
        # offset
        self.offset += self.speed * dt
        if self.offset >= self.tex_height:
            self.offset -= self.tex_height  # reset for infinite loop

    def draw(self):
        # draw the texture with offset
        for y in range(-self.tex_height, self.screen.get_height(), self.tex_height):
            for x in range(0, self.screen.get_width(), self.tex_width):
                self.screen.blit(self.texture, (x, y + self.offset))
