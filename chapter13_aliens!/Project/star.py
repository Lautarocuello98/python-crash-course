import pygame
from pygame.sprite import Sprite
from random import randint

class Star(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        original_image = pygame.image.load("images/mine.bmp").convert()
        self.image = pygame.transform.scale(original_image, (75, 75))
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)

        self.offset_x = randint(-10, 10)
        self.offset_y = randint(-10, 10)

    def check_edges(self):
        """Return True if mine is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        """Move the mine right/left with the fleet (same as Alien)."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = int(self.x)