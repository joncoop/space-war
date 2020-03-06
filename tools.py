import os
import pygame
import getpass


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

def load_image(path, width=None, height=None):
    image = pygame.image.load(path).convert_alpha()

    if width is not None:
        if height is None:
            height = int(image.get_height() * width / image.get_width())
    if height is not None:
        if width is None:
            width = int(image.get_width() * height / image.get_height())

    if width is not None or height is not None:
        image = pygame.transform.scale(image, [width, height])

    return image

def load_sound(path, volume=1.0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)

    return sound

def read_high_score():
    username = getpass.getuser()
    folder_name = f'C:/Users/{username}/AppData/Local/Space War/'
    file_name = 'scores.txt'
    full_path = folder_name + file_name

    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            score = int(f.read())
    else:
        score = 0

    return int(score)

def save_high_score(score):
    print('writing...')
    username = getpass.getuser()
    folder_name = f'C:/Users/{username}/AppData/Local/Space War/'
    file_name = 'scores.txt'
    full_path = folder_name + file_name

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    with open(full_path, 'w') as f:
        f.write(str(score))
