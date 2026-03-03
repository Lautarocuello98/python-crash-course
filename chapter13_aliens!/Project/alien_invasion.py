import sys
import pygame

from star import Star
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from random import randint

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)    

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key in (pygame.K_q, pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False


    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        self.stars.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create the fleet of aliens, with a 1-in-10 chance of a mine per slot."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        mine = Star(self)
        mine_width, mine_height = mine.rect.size

        cell_w, cell_h = alien_width, alien_height

        current_x, current_y = cell_w, cell_h
        while current_y < (self.settings.screen_height - 3 * cell_h):
            while current_x < (self.settings.screen_width - 2 * cell_w):

                # 1 en 10 -> mina
                if randint(1, 10) == 1:
                    self._create_mine(current_x, current_y, cell_w, cell_h)
                else:
                    self._create_alien(current_x, current_y)

                current_x += 2 * cell_w

            current_x = cell_w
            current_y += 2 * cell_h

    def _create_mine(self, x_position, y_position, cell_w, cell_h):
        """Create a mine (star) centered in the alien cell."""
        mine = Star(self)

        # Centrar la mina dentro de la celda del alien
        mine.rect.x = x_position + (cell_w - mine.rect.width) // 2
        mine.rect.y = y_position + (cell_h - mine.rect.height) // 2

        self.stars.add(mine)


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()