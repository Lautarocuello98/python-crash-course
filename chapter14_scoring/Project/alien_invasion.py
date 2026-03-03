import sys
import pygame
from random import randint
from time import sleep

from star import Star
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from falling_star import FallingStar
from button import Button


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()

        self.background = pygame.image.load("images/background.jpg").convert()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        self.settings.screen_width = self.screen_rect.width
        self.settings.screen_height = self.screen_rect.height

        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)

        # Start in menu state
        self.stats.game_active = False

        # Fonts used for UI text
        self.font = pygame.font.SysFont(None, 72)
        self.font_small = pygame.font.SysFont(None, 36)

        # ---- PLATFORM ----
        self.platform_image = pygame.image.load("images/base.bmp").convert_alpha()
        self.platform_image = pygame.transform.scale(self.platform_image, (90, 90))
        self.platform_rect = self.platform_image.get_rect()

        self.platform_rect.left = 20
        self.platform_rect.bottom = self.screen_rect.bottom - 650
        # ------------------

        # ---- TARGET ANIMATION (2 frames) ----
        self.target_frames = [
            pygame.image.load("images/normal.bmp").convert_alpha(),
            pygame.image.load("images/shout.bmp").convert_alpha(),
        ]

        self.target_frames = [
            pygame.transform.smoothscale(img, (90, 90)) for img in self.target_frames
        ]

        self.target_index = 0
        self.target_image = self.target_frames[self.target_index]
        self.target_rect = self.target_image.get_rect()

        # Offset so the target sits slightly above the platform
        self.target_offset_y = 35
        self.target_rect.midbottom = (
            self.platform_rect.centerx,
            self.platform_rect.top + self.target_offset_y,
        )

        self.target_anim_timer = 0
        self.target_anim_rate = 12
        # ------------------------------------

        # Background decorative stars
        self.falling_stars = pygame.sprite.Group()
        self._create_falling_stars()

        # Player ship
        self.ship = Ship(self)

        # Projectile and enemy groups
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        # Enemy spawn timer
        self.spawn_timer = 0

        # Play button for the menu
        self.play_button = Button(self, "Play")

        pygame.mouse.set_visible(True)

    # ----------------- Game Control -----------------

    def _start_game(self):
        """Start a new game. Can be triggered by the Play button or by pressing P."""
        self.stats.reset_stats()
        self.stats.game_active = True

        # Clear existing sprites
        self.bullets.empty()
        self.aliens.empty()
        self.stars.empty()

        # Reset spawn timer and reposition the ship
        self.spawn_timer = 0
        self.ship.center_ship()

        # Hide mouse cursor during gameplay
        pygame.mouse.set_visible(False)

    def _reset_game(self):
        """Restart the game after Game Over."""
        self._start_game()

    # ----------------- Helpers -----------------

    def _create_falling_stars(self):
        """Create decorative background stars."""
        for _ in range(15):
            self.falling_stars.add(FallingStar(self))

    def _update_target_animation(self):
        """Animate the target sprite."""
        self.target_anim_timer += 1

        if self.target_anim_timer >= self.target_anim_rate:
            self.target_anim_timer = 0
            self.target_index = 1 - self.target_index
            self.target_image = self.target_frames[self.target_index]

        # Keep the target attached to the platform
        self.target_rect.midbottom = (
            self.platform_rect.centerx,
            self.platform_rect.top + self.target_offset_y,
        )

    # ----------------- Main Loop -----------------

    def run_game(self):
        """Start the main game loop."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()

                self._update_bullets()
                self._spawn_enemies()
                self._update_enemies()

                self.falling_stars.update()
                self._update_target_animation()

            self._update_screen()
            self.clock.tick(60)

    # ----------------- Bullet Logic -----------------

    def _update_bullets(self):
        """Update bullet positions."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_collisions()

    def _check_bullet_collisions(self):
        """Handle bullet collisions."""
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        pygame.sprite.groupcollide(self.bullets, self.stars, True, True)

    # ----------------- Enemy Logic -----------------

    def _spawn_enemies(self):
        """Spawn enemies from the right side of the screen."""
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
            return

        y = randint(0, self.settings.screen_height - 80)
        x = self.settings.screen_width + 10

        if randint(1, 10) == 1:
            enemy = Star(self)
            enemy.rect.x = x
            enemy.rect.y = y
            enemy.x = float(enemy.rect.x)
            self.stars.add(enemy)
        else:
            enemy = Alien(self)
            enemy.rect.x = x
            enemy.rect.y = y
            enemy.x = float(enemy.rect.x)
            self.aliens.add(enemy)

        self.spawn_timer = self.settings.enemy_spawn_rate

    def _update_enemies(self):
        """Update enemy movement and collisions."""
        self.aliens.update()
        self.stars.update()

        for alien in self.aliens.copy():
            if alien.rect.left <= 0:
                self.ship_hit()
                return

        for mine in self.stars.copy():
            if mine.rect.left <= 0:
                self.ship_hit()
                return

        if self.ship:
            pygame.sprite.spritecollide(self.ship, self.aliens, True)

            if pygame.sprite.spritecollideany(self.ship, self.stars):
                self.ship_hit()

    # ----------------- Event Handling -----------------

    def _check_events(self):
        """Respond to keyboard and mouse events."""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start the game when the Play button is clicked."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _check_keydown_events(self, event):
        """Respond to key presses."""

        # Start the game when the player presses P
        if event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

        # Restart the game after Game Over
        if not self.stats.game_active and event.key == pygame.K_r:
            self._reset_game()
            return

        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key in (pygame.K_q, pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""

        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # ----------------- Drawing -----------------

    def _draw_game_over(self):
        """Display Game Over text."""
        text = self.font.render("GAME OVER", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.screen_rect.center)
        self.screen.blit(text, text_rect)

        text2 = self.font_small.render("Press R to restart", True, (255, 255, 255))
        text2_rect = text2.get_rect(
            center=(self.screen_rect.centerx, self.screen_rect.centery + 60)
        )
        self.screen.blit(text2, text2_rect)

    def _update_screen(self):
        """Redraw all screen elements."""
        self.screen.blit(self.background, (0, 0))

        self.falling_stars.draw(self.screen)

        self.screen.blit(self.platform_image, self.platform_rect)
        self.screen.blit(self.target_image, self.target_rect)

        self.aliens.draw(self.screen)
        self.stars.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        if self.ship:
            self.ship.blitme()

        if not self.stats.game_active and self.stats.ships_left == self.settings.ship_limit:
            self.play_button.draw_button()

        if not self.stats.game_active and self.stats.ships_left == 0:
            self._draw_game_over()

        pygame.display.flip()

    # ----------------- Shooting -----------------

    def _fire_bullet(self):
        """Create a new bullet."""
        if len(self.bullets) < self.settings.bullet_allowed:
            self.bullets.add(Bullet(self))

    # ----------------- Ship Hit -----------------

    def ship_hit(self):
        """Respond to the ship being hit."""
        if self.stats.ships_left > 1:

            self.stats.ships_left -= 1

            self.bullets.empty()
            self.aliens.empty()
            self.stars.empty()

            self.ship.center_ship()
            self.spawn_timer = 60

            sleep(0.5)

        else:
            self.stats.ships_left = 0
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()