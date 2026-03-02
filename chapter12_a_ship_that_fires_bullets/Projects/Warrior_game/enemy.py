# enemy.py
import pygame
from settings import Settings
from sprites import load_sheet, slice_sheet, scale_frames

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        fw, fh = Settings.FRAME_W, Settings.FRAME_H
        idle = slice_sheet(load_sheet(Settings.ENEMY_IDLE_SHEET), fw, fh)
        run = slice_sheet(load_sheet(Settings.ENEMY_RUN_SHEET), fw, fh)

        self.idle_frames = scale_frames(idle, 2.0)
        self.run_frames = scale_frames(run, 2.0)

        self.image = self.run_frames[0]
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.Vector2(self.rect.center)
        self.vel = pygame.Vector2(0, 0)

        self.frame_i = 0
        self.anim_ms = 140
        self.last_anim = pygame.time.get_ticks()

        self.facing = "right"

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim < self.anim_ms:
            return
        self.last_anim = now

        frames = self.run_frames
        self.frame_i = (self.frame_i + 1) % len(frames)
        img = frames[self.frame_i]

        if self.facing == "left":
            img = pygame.transform.flip(img, True, False)

        center = self.rect.center
        self.image = img
        self.rect = self.image.get_rect(center=center)

    def update(self, player_pos):
        direction = pygame.Vector2(player_pos) - self.pos
        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.vel = direction * Settings.ENEMY_SPEED
        self.pos += self.vel

        # facing según movimiento
        if self.vel.x < -0.1:
            self.facing = "left"
        elif self.vel.x > 0.1:
            self.facing = "right"

        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.animate()