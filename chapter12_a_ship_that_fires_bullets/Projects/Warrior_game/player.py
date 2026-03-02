# player.py
import pygame
from settings import Settings
from sprites import load_sheet, slice_sheet, scale_frames

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        fw, fh = Settings.FRAME_W, Settings.FRAME_H

        idle = slice_sheet(load_sheet(Settings.WARRIOR_IDLE_SHEET), fw, fh)
        run = slice_sheet(load_sheet(Settings.WARRIOR_RUN_SHEET), fw, fh)
        atk = slice_sheet(load_sheet(Settings.WARRIOR_ATTACK_SHEET), fw, fh)

        # Escala simple para que se vea mejor (ajustá si querés)
        self.idle_frames = scale_frames(idle, 2.0)
        self.run_frames = scale_frames(run, 2.0)
        self.atk_frames = scale_frames(atk, 2.0)

        self.state = "idle"  # idle | run | attack
        self.facing = "right"  # right | left

        self.frame_i = 0
        self.anim_ms = 120
        self.last_anim = pygame.time.get_ticks()

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.Vector2(self.rect.center)
        self.vel = pygame.Vector2(0, 0)

        self.attacking = False
        self.attack_started = 0

        self.hp = 5

    def start_attack(self):
        if self.attacking:
            return
        self.attacking = True
        self.attack_started = pygame.time.get_ticks()
        self.state = "attack"
        self.frame_i = 0
        self.last_anim = 0  # forzar update

    def attack_hitbox(self) -> pygame.Rect:
        w, h = Settings.ATTACK_SIZE
        hb = pygame.Rect(0, 0, w, h)
        hb.centery = self.rect.centery
        if self.facing == "right":
            hb.left = self.rect.right - 5
        else:
            hb.right = self.rect.left + 5
        return hb

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel.xy = 0, 0

        if keys[pygame.K_a]:
            self.vel.x = -Settings.PLAYER_SPEED
            self.facing = "left"
        if keys[pygame.K_d]:
            self.vel.x = Settings.PLAYER_SPEED
            self.facing = "right"
        if keys[pygame.K_w]:
            self.vel.y = -Settings.PLAYER_SPEED
        if keys[pygame.K_s]:
            self.vel.y = Settings.PLAYER_SPEED

        if not self.attacking:
            self.state = "run" if self.vel.length_squared() > 0 else "idle"

    def clamp_to_screen(self):
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.rect.clamp_ip(pygame.Rect(0, 0, Settings.WIDTH, Settings.HEIGHT))
        self.pos.xy = self.rect.center

    def animate(self):
        now = pygame.time.get_ticks()

        if self.attacking and now - self.attack_started >= Settings.ATTACK_DURATION_MS:
            self.attacking = False
            self.state = "idle" if self.vel.length_squared() == 0 else "run"

        if now - self.last_anim < self.anim_ms:
            return
        self.last_anim = now

        frames = self.idle_frames
        if self.state == "run":
            frames = self.run_frames
        elif self.state == "attack":
            frames = self.atk_frames

        self.frame_i = (self.frame_i + 1) % len(frames)
        img = frames[self.frame_i]

        if self.facing == "left":
            img = pygame.transform.flip(img, True, False)

        center = self.rect.center
        self.image = img
        self.rect = self.image.get_rect(center=center)

    def update(self):
        self.handle_input()
        self.pos += self.vel
        self.clamp_to_screen()
        self.animate()