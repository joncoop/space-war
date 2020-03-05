import os
import pygame
import sys
from tools import *


# Stuff to make exe work
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS + '/'
else:
    application_path = os.path.dirname(__file__) + '/'


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
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(TITLE)

icon = load_image(application_path + 'assets/images/playerShip1_blue.png')
pygame.display.set_icon(icon)


# Load assets
''' Colors '''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

''' Fonts '''
font_sm = pygame.font.Font(application_path + 'assets/fonts/recharge bd.ttf', 24)
font_md = pygame.font.Font(application_path + 'assets/fonts/recharge bd.ttf', 32)
font_lg = pygame.font.Font(application_path + 'assets/fonts/recharge bd.ttf', 48)
font_xl = pygame.font.Font(application_path + 'assets/fonts/recharge bd.ttf', 72)

''' Images '''
background_img = load_image(application_path + 'assets/images/purple.png')

ship_img = load_image(application_path + 'assets/images/playerShip1_blue.png')
ship_icon = load_image(application_path + 'assets/images/playerShip1_blue.png', height=32)
mob1_img = load_image(application_path + 'assets/images/enemyBlack4.png')
mob2_img = load_image(application_path + 'assets/images/enemyRed1.png')
laser_img = load_image(application_path + 'assets/images/laserBlue03.png')
bomb_img = load_image(application_path + 'assets/images/laserRed03.png')
double_shot_img = load_image(application_path + 'assets/images/powerupYellow_bolt.png')
explosion_imgs = [load_image(application_path + 'assets/images/explosion00.png'),
                  load_image(application_path + 'assets/images/explosion01.png'),
                  load_image(application_path + 'assets/images/explosion02.png'),
                  load_image(application_path + 'assets/images/explosion03.png'),
                  load_image(application_path + 'assets/images/explosion04.png')]

explosion_imgs = [pygame.transform.scale(img, [128, 128]) for img in explosion_imgs]

''' Music '''
start_theme = application_path + 'assets/music/The Smurfs NES - Act 1.wav'
main_theme = application_path + 'assets/music/SilverSurferNESStageTheme1.wav'
end_theme = None

''' Sounds '''
laser_snd = load_sound(application_path + 'assets/sounds/sfx_laser1.ogg')
explosion_snd = load_sound(application_path + 'assets/sounds/explosion1.ogg')
power_up_snd = load_sound(application_path + 'assets/sounds/phaserUp3.ogg')
power_down_snd = load_sound(application_path + 'assets/sounds/phaserDown3.ogg')
end_snd = load_sound(application_path + 'assets/music/Mega Man - Game Over.wav')


# Game settings
''' Controls '''
CONTROLS = {'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'shoot': pygame.K_SPACE,
            'restart': pygame.K_r}

NUM_LIVES = 3
SHIP_SPEED = 5
MOB_ATTACK_SPEED = 5
LASER_SPEED = 8
BOMB_SPEED = 6
POWERUP_SPEED = 6
MOB1_VALUE = 10
MOB2_VALUE = 50
POWERUP_VALUE = 20
EXTRA_SHIP_AT = [2000, 5000, 10000]
