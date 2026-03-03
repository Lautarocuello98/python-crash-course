import sys
import pygame
from random import randint
from time import sleep

from star import Star
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
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

        # Sync settings resolution with fullscreen resolution
        self.settings.screen_width = self.screen_rect.width
        self.settings.screen_height = self.screen_rect.height

        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.stats.game_active = False  # menu state

        # Fonts used for UI text
        self.font = pygame.font.SysFont(None, 72)
        self.font_small = pygame.font.SysFont(None, 36)

        # ---- PLATFORM ----
        self.platform_image = pygame.image.load("images/base.bmp").convert_alpha()
        self.platform_image = pygame.transform.scale(self.platform_image, (90, 90))
        self.platform_rect = self.platform_image.get_rect()

        self.platform_rect.left = 20
        self.platform_rect.centery = self.screen_rect.centery

        # Platform vertical movement (up/down)
        self.platform_speed = 2.0
        self.platform_direction = 1
        self.platform_min_y = 120
        self.platform_max_y = self.screen_rect.height - 120
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

        # ---- LEVEL / WAVES ----
        self.enemies_spawned = 0
        self.enemies_to_spawn = 0
        # -----------------------

        # Scoreboard (improved)
        self.sb = Scoreboard(self)

        # Menu buttons (Difficulty levels)
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "Hard")

        cx = self.screen_rect.centerx
        cy = self.screen_rect.centery
        self.easy_button.rect.center = (cx, cy - 70)
        self.medium_button.rect.center = (cx, cy)
        self.hard_button.rect.center = (cx, cy + 70)

        pygame.mouse.set_visible(True)

    # ----------------- Level system -----------------

    def _setup_level(self):
        """Configure how many enemies will spawn this level."""
        # Progression example:
        # Level 1: 15 enemies
        # Level 2: 20
        # Level 3: 25 ...
        base = 15
        step = 5

        self.enemies_spawned = 0
        self.enemies_to_spawn = base + (self.stats.level - 1) * step

        # Clear any leftovers (safety)
        self.aliens.empty()
        self.stars.empty()
        self.bullets.empty()

        # Reset spawn delay a bit so wave starts clean
        self.spawn_timer = 30

    def _advance_level(self):
        """Go to next level: speed up and start a new wave."""
        self.stats.level += 1
        self.settings.increase_speed()

        self.sb.prep_level()
        self._setup_level()

    # ----------------- Game Control -----------------

    def _start_game(self, difficulty: str):
        """Start a new game with selected difficulty."""
        self.stats.reset_stats()
        self.stats.game_active = True

        # Reset settings and apply difficulty (if you implemented it)
        self.settings.initialize_dynamic_settings()
        if hasattr(self.settings, "apply_difficulty"):
            self.settings.apply_difficulty(difficulty)

        # Clear existing sprites
        self.bullets.empty()
        self.aliens.empty()
        self.stars.empty()

        # Reset spawn timer and reposition the ship
        self.spawn_timer = 0
        self.ship.center_ship()

        # Reset platform position
        self.platform_rect.centery = self.screen_rect.centery
        self.platform_direction = 1

        # Keep target attached
        self.target_rect.midbottom = (
            self.platform_rect.centerx,
            self.platform_rect.top + self.target_offset_y,
        )

        # Setup wave/level 1
        self._setup_level()

        # Refresh scoreboard visuals
        self.sb.prep_all()

        pygame.mouse.set_visible(False)

    def _reset_game(self):
        """Restart after Game Over."""
        self._start_game("Medium")

    # ----------------- Helpers -----------------

    def _create_falling_stars(self):
        """Create decorative background stars."""
        for _ in range(15):
            self.falling_stars.add(FallingStar(self))

    def _update_platform(self):
        """Move the platform up and down. The target stays on it."""
        self.platform_rect.y += self.platform_direction * self.platform_speed

        if self.platform_rect.top <= self.platform_min_y:
            self.platform_rect.top = self.platform_min_y
            self.platform_direction *= -1

        if self.platform_rect.bottom >= self.platform_max_y:
            self.platform_rect.bottom = self.platform_max_y
            self.platform_direction *= -1

    def _update_target_animation(self):
        """Animate the target sprite (no movement)."""
        self.target_anim_timer += 1
        if self.target_anim_timer >= self.target_anim_rate:
            self.target_anim_timer = 0
            self.target_index = 1 - self.target_index
            self.target_image = self.target_frames[self.target_index]

        self.target_rect.midbottom = (
            self.platform_rect.centerx,
            self.platform_rect.top + self.target_offset_y,
        )

    # ----------------- Main Loop -----------------

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()

                self._update_bullets()
                self._spawn_enemies()
                self._update_enemies()

                self.falling_stars.update()
                self._update_platform()
                self._update_target_animation()

                # LEVEL COMPLETE:
                # spawned all enemies AND none left on screen
                if (self.enemies_spawned >= self.enemies_to_spawn) and (not self.aliens) and (not self.stars):
                    self._advance_level()

            self._update_screen()
            self.clock.tick(60)

    # ----------------- Bullet Logic -----------------

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_collisions()

    def _check_bullet_collisions(self):
        """Handle bullet collisions and update score."""
        hits_aliens = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if hits_aliens:
            destroyed_count = sum(len(v) for v in hits_aliens.values())
            self.stats.score += self.settings.alien_points * destroyed_count
            self.sb.prep_score()
            self.sb.check_high_score()

        pygame.sprite.groupcollide(self.bullets, self.stars, True, True)

    # ----------------- Enemy Logic -----------------

    def _spawn_enemies(self):
        """Spawn enemies from the right side (limited per level)."""

        # Stop spawning when this level already spawned enough enemies
        if self.enemies_spawned >= self.enemies_to_spawn:
            return

        if self.spawn_timer > 0:
            self.spawn_timer -= 1
            return

        y = randint(0, self.settings.screen_height - 80)
        x = self.settings.screen_width + 10

        # 10% chance to spawn a Star (bomb), otherwise Alien
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

        self.enemies_spawned += 1
        self.spawn_timer = self.settings.enemy_spawn_rate

    def _update_enemies(self):
        self.aliens.update()
        self.stars.update()

        # If ANY enemy reaches the left side -> lose a life
        for alien in self.aliens.copy():
            if alien.rect.right < 0:
                self.ship_hit()
                return

        for bomb in self.stars.copy():
            if bomb.rect.right < 0:
                self.ship_hit()
                return

        # Touching an alien -> alien dies, player survives
        pygame.sprite.spritecollide(self.ship, self.aliens, True)

        # Touching a bomb -> player loses a life
        if pygame.sprite.spritecollideany(self.ship, self.stars):
            self.ship_hit()
            return

    # ----------------- Event Handling -----------------

    def _check_events(self):
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
                self._check_menu_click(mouse_pos)

    def _check_menu_click(self, mouse_pos):
        if self.stats.game_active:
            return

        if self.easy_button.rect.collidepoint(mouse_pos):
            self._start_game("Easy")
        elif self.medium_button.rect.collidepoint(mouse_pos):
            self._start_game("Medium")
        elif self.hard_button.rect.collidepoint(mouse_pos):
            self._start_game("Hard")

    def _check_keydown_events(self, event):
        if event.key in (pygame.K_q, pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        if event.key == pygame.K_p and not self.stats.game_active:
            self._start_game("Medium")
            return

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
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()

    def _check_keyup_events(self, event):
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
        text = self.font.render("GAME OVER", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.screen_rect.center)
        self.screen.blit(text, text_rect)

        text2 = self.font_small.render("Press R to restart", True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 60))
        self.screen.blit(text2, text2_rect)

    def _update_screen(self):
        self.screen.blit(self.background, (0, 0))

        self.falling_stars.draw(self.screen)

        self.screen.blit(self.platform_image, self.platform_rect)
        self.screen.blit(self.target_image, self.target_rect)

        self.aliens.draw(self.screen)
        self.stars.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()

        if self.stats.game_active:
            self.sb.show()

        # Menu
        if (not self.stats.game_active) and (self.stats.ships_left == self.settings.ship_limit):
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        # Game over
        if (not self.stats.game_active) and (self.stats.ships_left == 0):
            self._draw_game_over()

        pygame.display.flip()

    # ----------------- Shooting -----------------

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self))

    # ----------------- Ship Hit -----------------

    def ship_hit(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1

            self.bullets.empty()
            self.aliens.empty()
            self.stars.empty()

            self.ship.center_ship()
            self.spawn_timer = 60

            self.sb.prep_lives()
            sleep(0.5)

            # OPTIONAL: if you want to restart the SAME wave after losing a life,
            # uncomment the next line:
            # self._setup_level()

        else:
            self.stats.ships_left = 0
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.sb.prep_lives()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()