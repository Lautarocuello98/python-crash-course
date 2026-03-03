import pygame
from pygame.sprite import Sprite
from random import randint
from random import uniform

class FallingStar(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        image = pygame.image.load("images/star1.bmp").convert_alpha()
        self.image = pygame.transform.scale(image, (20, 20))
        self.rect = self.image.get_rect()

        # Posición random arriba
        self.rect.x = randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = randint(-600, -20)

        self.y = float(self.rect.y)

        self.speed = uniform(0.3, 1.0)

    def update(self):
        self.y += self.speed
        self.rect.y = int(self.y)

        # Si desaparece abajo, vuelve arriba
        if self.rect.top > self.settings.screen_height:
            self.rect.x = randint(0, self.settings.screen_width - self.rect.width)
            self.rect.y = randint(-100, -40)
            self.y = float(self.rect.y)