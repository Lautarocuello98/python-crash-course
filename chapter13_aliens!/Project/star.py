import pygame
from pygame.sprite import Sprite
from random import randint

class Star(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        original_image = pygame.image.load("images/mine.bmp")
        self.image = pygame.transform.scale(original_image, (75, 75))
        self.rect = self.image.get_rect()

        # offset random (13.2)
        self.offset_x = randint(-10, 10)
        self.offset_y = randint(-10, 10)