import pygame


# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Name of Game"
FPS = 60

# Make window
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(TITLE)

icon = pygame.image.load('assets/images/playerShip1_blue.png').convert_alpha()
pygame.display.set_icon(icon)

# Load assets
''' Colors '''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

''' Fonts '''
font_sm = pygame.font.Font(None, 24)
font_md = pygame.font.Font(None, 32)
font_lg = pygame.font.Font(None, 48)
font_xl = pygame.font.Font('assets/fonts/kenvector_future.ttf', 64)

''' Images '''
background_img = pygame.image.load('assets/images/purple.png').convert_alpha()
ship_img = pygame.image.load('assets/images/playerShip1_blue.png').convert_alpha()
ship_icon = pygame.image.load('assets/images/playerShip1_small.png').convert_alpha()
laser_img = pygame.image.load('assets/images/laserBlue03.png').convert_alpha()
mob1_img = pygame.image.load('assets/images/enemyBlack4.png').convert_alpha()
mob2_img = pygame.image.load('assets/images/enemyRed1.png').convert_alpha()
double_shot_img = pygame.image.load('assets/images/powerupYellow_bolt.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/laserRed03.png').convert_alpha()
explosion_imgs = [pygame.image.load('assets/images/explosion00.png').convert_alpha(),
                  pygame.image.load('assets/images/explosion01.png').convert_alpha(),
                  pygame.image.load('assets/images/explosion02.png').convert_alpha(),
                  pygame.image.load('assets/images/explosion03.png').convert_alpha(),
                  pygame.image.load('assets/images/explosion04.png').convert_alpha()]

explosion_imgs = [pygame.transform.scale(img, [128, 128]) for img in explosion_imgs]

''' Music '''
start_theme = None
main_theme = 'assets/music/SilverSurferNESStageTheme1.wav'
end_theme = None

''' Sounds '''
laser_snd = pygame.mixer.Sound('assets/sounds/sfx_laser1.ogg')
explosion_snd = pygame.mixer.Sound('assets/sounds/explosion1.ogg')
power_up_snd = pygame.mixer.Sound('assets/sounds/phaserUp3.ogg')
power_down_snd = pygame.mixer.Sound('assets/sounds/phaserDown3.ogg')

# Game settings
''' Controls '''
p1_controls = {'left': pygame.K_LEFT,
               'right': pygame.K_RIGHT,
               'shoot': pygame.K_SPACE,
               'restart': pygame.K_r}
