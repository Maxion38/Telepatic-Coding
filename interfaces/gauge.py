import pygame

class Gauge:
    def __init__(self, isVertical, thickness, length, empty_color, fill_color, max_capacity=100, current_capacity=100):
        self.thickness = thickness
        self.length = length
        
        if isVertical:
            self.rect = pygame.Rect(0, 0, self.thickness, self.length)
        else:
            self.rect = pygame.Rect(0, 0, self.length, self.thickness)

        self.isVertical = isVertical
        self.max_capacity = max_capacity
        self.current_capacity = current_capacity
        self.empty_color = empty_color
        self.fill_color = fill_color


    def decrease_capacity(self, amount):
        self.current_capacity -= amount

        if self.current_capacity <= 0:
            self.current_capacity = 0
            return False # gauge is empty
        

    def increase_capacity(self, amount):
        self.current_capacity += amount

        if self.current_capacity >= self.max_capacity:
            self.current_capacity = self.max_capacity
            return False # gauge is full
        

    def draw(self, screen):
        fill_length = int(self.length * self.current_capacity / self.max_capacity)

        if self.isVertical:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y + (self.length - fill_length), self.thickness, fill_length)
        else:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_length, self.thickness)

        pygame.draw.rect(screen, self.empty_color, self.rect)
        pygame.draw.rect(screen, self.fill_color, fill_rect)

        
