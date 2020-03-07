import os
import sys

import pygame

# Stuff to make executables work
if getattr(sys, 'frozen', False):
    application_path = sys.MEIPASS + '/'
else:
    application_path = os.path.dirname(__file__) + '/'


# Helper functions
def draw_text(surface, text, font, color, loc, anchor='topleft'):
    text = str(text)
    text = font.render(text, True, color)
    rect = text.get_rect()

    if anchor == 'topleft':
        rect.topleft = loc
    elif anchor == 'bottomleft':
        rect.bottomleft = loc
    elif anchor == 'topright':
        rect.topright = loc
    elif anchor == 'bottomright':
        rect.bottomright = loc
    elif anchor == 'midtop':
        rect.midtop = loc
    elif anchor == 'midleft':
        rect.midleft = loc
    elif anchor == 'midbottom':
        rect.midbottom = loc
    elif anchor == 'midright':
        rect.midleft = loc
    elif anchor == 'center':
        rect.center = loc

    surface.blit(text, rect)


def get_text_size(text, font):
    text = str(text)
    text = font.render(text, True, [0, 0, 0])
    rect = text.get_rect()

    return rect.width, rect.height


def load_image(relative_path, width=None, height=None):
    image = pygame.image.load(application_path + relative_path).convert_alpha()

    if width is not None:
        if height is None:
            height = int(image.get_height() * width / image.get_width())
    if height is not None:
        if width is None:
            width = int(image.get_width() * height / image.get_height())

    if width is not None or height is not None:
        image = pygame.transform.scale(image, [width, height])

    return image


def load_sound(relative_path, volume=1.0):
    sound = pygame.mixer.Sound(application_path + relative_path)
    sound.set_volume(volume)

    return sound


def load_font(relative_path, size):
    return pygame.font.Font(application_path + relative_path, size)


def load_music(relative_path, volume=1.0):
    pygame.mixer.music.load(application_path + relative_path)


def play_music(loops=-1):
    pygame.mixer.music.play(loops)


def pause_music():
    pygame.mixer.music.pause()


def unpause_music():
    pygame.mixer.music.unpause()


def stop_music():
    pygame.mixer.music.stop()
