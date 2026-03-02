# settings.py

class Settings:
    # Window
    WIDTH = 960
    HEIGHT = 540
    FPS = 60
    BG = (20, 20, 30)

    # Spritesheet slicing
    FRAME_W = 128
    FRAME_H = 128

    # Player
    PLAYER_SPEED = 4.0
    ATTACK_DURATION_MS = 220
    ATTACK_RANGE = 55
    ATTACK_SIZE = (70, 40)  # hitbox w,h

    # Enemy
    ENEMY_SPEED = 2.2
    ENEMY_SPAWN_MS = 1200

    # Paths
    # Warrior_Idle.png, Warrior_Run.png, Warrior_Attack1.png
    WARRIOR_IDLE_SHEET = "assets/Warrior_idle.png"
    WARRIOR_RUN_SHEET = "assets/Warrior_Run.png"
    WARRIOR_ATTACK_SHEET = "assets/Warrior_Attack1.png"

    ENEMY_IDLE_SHEET = "assets/Idle.png"
    ENEMY_RUN_SHEET = "assets/Run.png"