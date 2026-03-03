import sys
import pygame
from random import randint

from star import Star
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from falling_star import FallingStar


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.background = pygame.image.load("images/background.jpg").convert()
        self.background = pygame.transform.scale(
        self.background,
        self.screen.get_size()
        )
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.falling_stars = pygame.sprite.Group()
        self._create_falling_stars()

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()

    def _create_falling_stars(self):
        for _ in range(15):
            star = FallingStar(self)
            self.falling_stars.add(star)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_fleet()
            self.falling_stars.update()
            self._update_screen()
            self.clock.tick(60)
            

    # ----------------- Updates -----------------

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_fleet(self):
        """Update aliens + mines and handle edges/direction changes."""
        self._check_fleet_edges()
        self.aliens.update()
        self.stars.update()

    # ----------------- Fleet movement helpers -----------------

    def _check_fleet_edges(self):
        """Respond if any alien or mine has reached an edge."""
        for sprite in self.aliens.sprites():
            if sprite.check_edges():
                self._change_fleet_direction()
                return

        for sprite in self.stars.sprites():
            if sprite.check_edges():
                self._change_fleet_direction()
                return

    def _change_fleet_direction(self):
        """Drop the entire fleet and change direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        for mine in self.stars.sprites():
            mine.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    # ----------------- Events -----------------

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

    # ----------------- Drawing -----------------

    def _update_screen(self):
        """Redraw the screen during each pass through the loop."""
        self.screen.blit(self.background, (0, 0))

        self.falling_stars.draw(self.screen)

        # Mines + aliens
        self.stars.draw(self.screen)
        self.aliens.draw(self.screen)

        # Bullets + ship
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()

        pygame.display.flip()


    # ----------------- Shooting -----------------

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # ----------------- Fleet creation -----------------

    def _create_fleet(self):
        """Create a mixed fleet: 1-in-10 chance a slot is a mine."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        cell_w, cell_h = alien_width, alien_height

        current_x, current_y = cell_w, cell_h
        while current_y < (self.settings.screen_height - 3 * cell_h):
            while current_x < (self.settings.screen_width - 2 * cell_w):

                if randint(1, 10) == 1:
                    self._create_mine(current_x, current_y, cell_w, cell_h)
                else:
                    self._create_alien(current_x, current_y)

                current_x += 2 * cell_w

            current_x = cell_w
            current_y += 2 * cell_h

    def _create_mine(self, x_position, y_position, cell_w, cell_h):
        """Create a mine centered in the alien cell, with random offset."""
        mine = Star(self)

        mine.rect.x = x_position + (cell_w - mine.rect.width) // 2 + mine.offset_x
        mine.rect.y = y_position + (cell_h - mine.rect.height) // 2 + mine.offset_y
        mine.x = float(mine.rect.x)  # IMPORTANT: sync float position for update()

        self.stars.add(mine)

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()