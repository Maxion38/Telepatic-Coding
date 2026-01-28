import pygame
from PIL import Image, ImageFilter
from pathlib import Path


def blur_image(path: str | Path) -> pygame.Surface:
    img = Image.open(path).convert("RGBA")

    img = img.filter(ImageFilter.GaussianBlur(radius=5))

    mode = img.mode
    size = img.size
    data = img.tobytes()
    surface = pygame.image.fromstring(data, size, mode)

    return surface
