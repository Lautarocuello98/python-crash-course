import pygame
from pygame.sprite import Group, Sprite


class LifeIcon(Sprite):
    """Small ship icon used only for showing lives (no movement/logic)."""

    def __init__(self, image: pygame.Surface, x: int, y: int):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))


class Scoreboard:
    """Display score, high score, level, and lives. Friendly with image backgrounds."""

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats

        # Fonts
        self.font = pygame.font.SysFont(None, 44)
        self.font_small = pygame.font.SysFont(None, 28)

        # Colors (white text + black shadow reads on most backgrounds)
        self.text_color = (255, 255, 255)
        self.shadow_color = (0, 0, 0)

        # Cache a life icon image from the ship (scaled)
        ship_img = ai_game.ship.image
        self.life_image = pygame.transform.smoothscale(ship_img, (36, 36))

        self.prep_all()

    # ---------- helpers ----------

    def _render(self, text: str, font: pygame.font.Font):
        main = font.render(text, True, self.text_color)
        shadow = font.render(text, True, self.shadow_color)
        return main, shadow

    def _blit_shadowed(self, main, shadow, x, y):
        self.screen.blit(shadow, (x + 2, y + 2))
        self.screen.blit(main, (x, y))

    # ---------- prep ----------

    def prep_all(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()

    def prep_score(self):
        rounded = round(self.stats.score, -1)
        score_str = f"{rounded:,}"

        self.score_label_main, self.score_label_shadow = self._render("SCORE", self.font_small)
        self.score_main, self.score_shadow = self._render(score_str, self.font)

        right = self.screen_rect.right - 20
        self.score_label_pos = (right - self.score_label_main.get_width(), 14)
        self.score_pos = (right - self.score_main.get_width(), 40)

    def prep_high_score(self):
        high = round(self.stats.high_score, -1)
        hi_str = f"{high:,}"

        self.hi_label_main, self.hi_label_shadow = self._render("HI", self.font_small)
        self.hi_main, self.hi_shadow = self._render(hi_str, self.font)

        cx = self.screen_rect.centerx
        self.hi_label_pos = (cx - self.hi_label_main.get_width() // 2, 14)
        self.hi_pos = (cx - self.hi_main.get_width() // 2, 40)

    def prep_level(self):
        level_str = f"LEVEL {self.stats.level}"
        self.level_main, self.level_shadow = self._render(level_str, self.font_small)

        right = self.screen_rect.right - 20
        self.level_pos = (right - self.level_main.get_width(), 78)

    def prep_lives(self):
        """Show remaining lives as ship icons (top-left)."""
        self.lives = Group()

        self.lives_label_main, self.lives_label_shadow = self._render("LIVES", self.font_small)
        self.lives_label_pos = (20, 14)

        x = 20
        y = 42
        spacing = 10

        for i in range(self.stats.ships_left):
            icon = LifeIcon(self.life_image, x + i * (self.life_image.get_width() + spacing), y)
            self.lives.add(icon)

    # ---------- logic ----------

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    # ---------- draw ----------

    def show(self):
        # Lives (top-left)
        self._blit_shadowed(self.lives_label_main, self.lives_label_shadow, *self.lives_label_pos)
        self.lives.draw(self.screen)

        # High score (top-center)
        self._blit_shadowed(self.hi_label_main, self.hi_label_shadow, *self.hi_label_pos)
        self._blit_shadowed(self.hi_main, self.hi_shadow, *self.hi_pos)

        # Score + level (top-right)
        self._blit_shadowed(self.score_label_main, self.score_label_shadow, *self.score_label_pos)
        self._blit_shadowed(self.score_main, self.score_shadow, *self.score_pos)
        self._blit_shadowed(self.level_main, self.level_shadow, *self.level_pos)