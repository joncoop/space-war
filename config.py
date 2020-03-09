from tools import *


# Window settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 680
TITLE = "Space War!"
FPS = 60

# Game states
INTRO = 0
PLAYING = 1
PAUSED = 2
STAGE_CLEARED = 3
SHIP_KILLED = 4
GAME_OVER = 5

# Make window
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(TITLE)

icon = load_image('assets/images/window_icon.png')
pygame.display.set_icon(icon)

# Load assets
''' Colors '''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (94, 63, 107)

''' Fonts '''
font_sm = load_font('assets/fonts/recharge bd.ttf', 24)
font_md = load_font('assets/fonts/recharge bd.ttf', 32)
font_lg = load_font('assets/fonts/recharge bd.ttf', 48)
font_xl = load_font('assets/fonts/recharge bd.ttf', 72)

''' Images '''
background_img = load_image('assets/images/purple.png')
ship_img = load_image('assets/images/playerShip1_blue.png')
ship_icon = load_image('assets/images/playerShip1_blue.png', height=32)
mob1_img = load_image('assets/images/enemyBlack4.png')
mob2_img = load_image('assets/images/enemyRed1.png')
laser_img = load_image('assets/images/laserBlue03.png')
bomb_img = load_image('assets/images/laserRed03.png')
double_shot_img = load_image('assets/images/powerupYellow_bolt.png')
explosion_imgs = [load_image('assets/images/explosion00.png'),
                  load_image('assets/images/explosion01.png'),
                  load_image('assets/images/explosion02.png'),
                  load_image('assets/images/explosion03.png'),
                  load_image('assets/images/explosion04.png')]

explosion_imgs = [pygame.transform.scale(img, [128, 128]) for img in explosion_imgs]

''' Music '''
start_theme = 'assets/music/TheSmurfs-NES-Act1.wav'
main_theme = 'assets/music/SilverSurfer-NES-StageTheme1.wav'
end_theme = None

''' Sounds '''
laser_snd = load_sound('assets/sounds/laser.ogg')
explosion_snd = load_sound('assets/sounds/explosion.ogg')
power_up_snd = load_sound('assets/sounds/powerUp.wav')
point_snd = load_sound('assets/sounds/pointTally.wav')
end_snd = load_sound('assets/music/MegaMan-GameOver.wav')

# Controls
CONTROLS = {'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'shoot': pygame.K_SPACE,
            'restart': pygame.K_r}

# Game settings
NUM_LIVES = 3
SHIP_SPEED = 5
FLEET_SPEED = 1
MOB_ATTACK_SPEED = 5
LASER_SPEED = 8
BOMB_SPEED = 6
POWERUP_SPEED = 6
MOB1_VALUE = 10
MOB2_VALUE = 50
POWERUP_VALUE = 20
EXTRA_SHIP_AT = [2000, 5000, 10000]

# Attack types
NORMAL = 0
ZIG_ZAG = 1
OUT_AND_BACK = 2
