import pygame
from config import *


class Ship(pygame.sprite.Sprite):

    def __init__(self, image, location, scene):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.scene = scene

        self.shield = 5
        self.shoots_double = False
        self.score = 0

    def move_left(self):
        self.rect.x -= 5

        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += 5

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        if self.shoots_double:
            laser1 = Laser(laser_img, [self.rect.left, self.rect.centery])
            laser2 = Laser(laser_img, [self.rect.right, self.rect.centery])
            self.scene.lasers.add(laser1, laser2)
        else:
            laser = Laser(laser_img, [self.rect.centerx, self.rect.top])
            self.scene.lasers.add(laser)

        laser_snd.play()

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, self.scene.items, True,
                                                   pygame.sprite.collide_mask)
        for item in hit_list:
            item.apply(self)

        hit_list = pygame.sprite.spritecollide(self, self.scene.bombs, True,
                                                   pygame.sprite.collide_mask)

        for bomb in hit_list:
            self.shield -= 1
            self.shoots_double = False

        hit_list = pygame.sprite.spritecollide(self, self.scene.mobs, True,
                                                   pygame.sprite.collide_mask)

        for mob in hit_list:
            mob.health = 0
            self.shield = 0

        if self.shield <= 0:
            explosion = Explosion(explosion_imgs, self.rect.center)
            self.scene.explosions.add(explosion)
            self.kill()


class Laser(pygame.sprite.Sprite):

    def __init__(self, image, location):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = location

    def update(self):
        self.rect.y -= 8

        if self.rect.bottom < 0:
            self.kill()


class Mob(pygame.sprite.Sprite):

    def __init__(self, image, location, scene):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.fleet_loc = location
        self.scene = scene

        self.shield = 3
        self.speed = 3
        self.attack_location = None

    def drop_bomb(self, bombs):
        bomb = Bomb(bomb_img, [self.rect.centerx, self.rect.bottom])
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, self.scene.lasers, True,
                                                   pygame.sprite.collide_mask)

        for hit in hit_list:
            self.shield -= 1

        if self.shield <= 0:
            explosion = Explosion(explosion_imgs, self.rect.center)
            self.scene.explosions.add(explosion)
            self.scene.ship.score += 1
            self.kill()
            mob_explosion_snd.play()


class Bomb(pygame.sprite.Sprite):

    def __init__(self, image, location):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = location

    def update(self):
        self.rect.y += 6

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class DoubleShot(pygame.sprite.Sprite):

    def __init__(self, image, location):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = location

    def apply(self, ship):
        ship.shoots_double = True

    def update(self):
        self.rect.y += 5

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):

    def __init__(self, images, location):
        super().__init__()

        self.images = images
        self.image_index = 0
        self.image = images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.ticks = 0

    def update(self):
        self.ticks += 1

        if self.ticks % 3 == 0:
            self.image_index += 1

            if self.image_index < len(self.images):
                self.image = self.images[self.image_index]
            else:
                self.kill()
