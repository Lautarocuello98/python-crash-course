import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Enemy that moves from right to left (sideways shooter)."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        original_image = pygame.image.load("images/eye.bmp")
        self.image = pygame.transform.scale(original_image, (75, 75))
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)

    def update(self):
        """Move the alien left toward the ship."""
        self.x -= self.settings.alien_speed
        self.rect.x = int(self.x)