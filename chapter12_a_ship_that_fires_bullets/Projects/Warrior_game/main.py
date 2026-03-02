# main.py
import random
import sys
import pygame

from settings import Settings
from player import Player
from enemy import Enemy

def random_spawn_edge():
    w, h = Settings.WIDTH, Settings.HEIGHT
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        return (random.randint(0, w), -20)
    if side == "bottom":
        return (random.randint(0, w), h + 20)
    if side == "left":
        return (-20, random.randint(0, h))
    return (w + 20, random.randint(0, h))

def main():
    pygame.init()
    screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    pygame.display.set_caption("Warrior Arena")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    player = Player((Settings.WIDTH // 2, Settings.HEIGHT // 2))

    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)

    last_spawn = pygame.time.get_ticks()

    while True:
        dt = clock.tick(Settings.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.start_attack()

        # spawn enemigos
        now = pygame.time.get_ticks()
        if now - last_spawn >= Settings.ENEMY_SPAWN_MS:
            last_spawn = now
            e = Enemy(random_spawn_edge())
            enemies.add(e)
            all_sprites.add(e)

        # updates
        player.update()
        enemies.update(player.rect.center)

        # ataque: hitbox vs enemigos
        if player.attacking:
            hb = player.attack_hitbox()
            hit = [e for e in enemies if hb.colliderect(e.rect)]
            for e in hit:
                e.kill()

        # daño al jugador
        touched = pygame.sprite.spritecollide(player, enemies, dokill=False)
        if touched:
            # daño simple con cooldown ultra básico
            player.hp -= 1
            # empujoncito / respawn enemies para que no drene HP instantáneo
            for e in touched:
                e.pos += pygame.Vector2(random.randint(-40, 40), random.randint(-40, 40))
                e.rect.center = (int(e.pos.x), int(e.pos.y))

            if player.hp <= 0:
                pygame.quit()
                sys.exit()

        # draw
        screen.fill(Settings.BG)
        all_sprites.draw(screen)

        # debug hitbox
        if player.attacking:
            pygame.draw.rect(screen, (255, 80, 80), player.attack_hitbox(), 2)

        hp_text = font.render(f"HP: {player.hp}", True, (240, 240, 240))
        screen.blit(hp_text, (12, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()