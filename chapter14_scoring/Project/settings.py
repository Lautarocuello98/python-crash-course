class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 6
        self.bullet_height = 20
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 5

        # Enemy spawn (frames)
        self.enemy_spawn_rate = 45
        self.min_enemy_spawn_rate = 12

        # Target settings (Exercise 14-3)
        self.target_speed = 2.0

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        # Defaults (these get overridden by difficulty buttons)
        self.ship_speed = 6.0
        self.bullet_speed = 12.0
        self.alien_speed = 3.0

        self.enemy_spawn_rate = 45
        self.target_speed = 2.0

        # Scoring (optional)
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        # Target also speeds up (Exercise 14-3)
        self.target_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

        # Spawn faster over time (lower = faster)
        new_rate = int(self.enemy_spawn_rate / self.speedup_scale)
        self.enemy_spawn_rate = max(self.min_enemy_spawn_rate, new_rate)

    def apply_difficulty(self, level: str):
        """Set starting difficulty values (Exercise 14-4)."""
        level = level.lower().strip()

        if level == "easy":
            self.ship_speed = 7.0
            self.bullet_speed = 13.0
            self.alien_speed = 2.5
            self.enemy_spawn_rate = 70
            self.target_speed = 2.0

        elif level == "medium":
            self.ship_speed = 6.0
            self.bullet_speed = 12.0
            self.alien_speed = 3.0
            self.enemy_spawn_rate = 45
            self.target_speed = 2.0

        elif level == "hard":
            self.ship_speed = 6.5
            self.bullet_speed = 12.5
            self.alien_speed = 3.6
            self.enemy_spawn_rate = 28
            self.target_speed = 2.2