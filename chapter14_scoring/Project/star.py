import pygame
from pygame.sprite import Sprite
from random import randint

class Star(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        original_image = pygame.image.load("images/mine.bmp")
        self.image = pygame.transform.scale(original_image, (75, 75))
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)

        self.offset_y = randint(-10, 10)

    def update(self):
        """Move mine left toward the ship."""
        self.x -= self.settings.alien_speed
        self.rect.x = int(self.x)