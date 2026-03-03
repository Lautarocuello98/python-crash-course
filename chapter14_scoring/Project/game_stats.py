class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings

        # High score should NOT reset when starting a new game
        self.high_score = 0

        # Start in menu state; main decides when to activate
        self.game_active = False

        self.reset_stats()

    def reset_stats(self):
        """Initialize stats that change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def increase_level(self):
        """Increase level count."""
        self.level += 1

    def check_high_score(self):
        """Update high score if needed."""
        if self.score > self.high_score:
            self.high_score = self.score