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
        self.target_frames = [pygame.transform.smoothscale(img, (90, 90)) for img in self.target_frames]

        self.target_index = 0
        self.target_image = self.target_frames[self.target_index]
        self.target_rect = self.target_image.get_rect()

        # Arriba de la plataforma
        self.target_rect.midbottom = (self.platform_rect.centerx, self.platform_rect.top + 35)

        self.target_anim_timer = 0
        self.target_anim_rate = 15   # cambia cada 12 frames (~5 veces/seg)
        # ------------------------------------

        # Background falling stars
        self.falling_stars = pygame.sprite.Group()
        self._create_falling_stars()

        # Player
        self.ship = Ship(self)

        # Projectiles and enemies
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()  # mines

        # Sideways spawn timer
        self.spawn_timer = 0

    def _create_falling_stars(self):
        for _ in range(15):
            self.falling_stars.add(FallingStar(self))

    def _update_target_animation(self):
        # alternar frames
        self.target_anim_timer += 1
        if self.target_anim_timer >= self.target_anim_rate:
            self.target_anim_timer = 0
            self.target_index = 1 - self.target_index
            self.target_image = self.target_frames[self.target_index]

        # mantenerla pegada arriba de la plataforma
        self.target_rect.midbottom = (self.platform_rect.centerx, self.platform_rect.top + 35)

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                if self.ship:
                    self.ship.update()

                self._update_bullets()
                self._spawn_enemies()
                self._update_enemies()

                self.falling_stars.update()
                self._update_target_animation()

            self._update_screen()
            self.clock.tick(60)

    # ----------------- Bullets -----------------

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_collisions()

    def _check_bullet_collisions(self):
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        pygame.sprite.groupcollide(self.bullets, self.stars, True, True)

    # ----------------- Enemies -----------------

    def _spawn_enemies(self):
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
            return

        y = randint(0, self.settings.screen_height - 80)
        x = self.settings.screen_width + 10

        if randint(1, 10) == 1:
            enemy = Star(self)
            enemy.rect.x = x
            enemy.rect.y = y + getattr(enemy, "offset_y", 0)
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
        self.aliens.update()
        self.stars.update()

        for a in self.aliens.copy():
            if a.rect.right < 0:
                self.aliens.remove(a)

        for m in self.stars.copy():
            if m.rect.right < 0:
                self.stars.remove(m)

        if self.ship:
            pygame.sprite.spritecollide(self.ship, self.aliens, True)

            if pygame.sprite.spritecollideany(self.ship, self.stars):
                self.ship_hit()

    # ----------------- Events -----------------

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
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
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # ----------------- Drawing -----------------

    def _update_screen(self):
        self.screen.blit(self.background, (0, 0))

        self.falling_stars.draw(self.screen)

        # Platform + target arriba
        self.screen.blit(self.platform_image, self.platform_rect)
        self.screen.blit(self.target_image, self.target_rect)

        self.aliens.draw(self.screen)
        self.stars.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        if self.ship:
            self.ship.blitme()

        pygame.display.flip()

    # ----------------- Shooting -----------------

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            self.bullets.add(Bullet(self))

    # ----------------- Ship hit -----------------

    def ship_hit(self):
        self.stats.ships_left -= 1

        self.bullets.empty()
        self.aliens.empty()
        self.stars.empty()

        self.ship.center_ship()
        self.spawn_timer = 60

        sleep(0.5)

        if self.stats.ships_left <= 0:
            self.stats.game_active = False


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()