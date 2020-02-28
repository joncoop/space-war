import math
import pygame
import random
from config import *


class Ship(pygame.sprite.Sprite):

    def __init__(self, image, location, scene):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.spawn_loc = location
        self.scene = scene

        self.shield = 1
        self.num_lives = 3
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
        num_lasers = len(self.scene.lasers)

        if self.shoots_double and num_lasers < 3:
            laser1 = Laser(laser_img, [self.rect.left, self.rect.centery])
            laser2 = Laser(laser_img, [self.rect.right, self.rect.centery])
            self.scene.lasers.add(laser1, laser2)
            laser_snd.play()
        elif num_lasers < 2:
            laser = Laser(laser_img, [self.rect.centerx, self.rect.top])
            self.scene.lasers.add(laser)
            laser_snd.play()

    def check_items(self):
        hit_list = pygame.sprite.spritecollide(self, self.scene.items, True,
                                                   pygame.sprite.collide_mask)
        for item in hit_list:
            item.apply(self)

    def check_bombs(self):
        hit_list = pygame.sprite.spritecollide(self, self.scene.bombs, True,
                                                   pygame.sprite.collide_mask)

        for bomb in hit_list:
            self.shield -= 1
            if self.shoots_double:
                power_down_snd.play()
                self.shoots_double = False

    def check_mobs(self):
        hit_list = pygame.sprite.spritecollide(self, self.scene.mobs, True,
                                                   pygame.sprite.collide_mask)

        for mob in hit_list:
            mob.health = 0
            self.shield = 0

    def respawn(self):
        self.rect.center = self.spawn_loc
        self.shield = 1
        self.scene.player.add(self)

    def check_status(self):
        if self.shield <= 0:
            explosion = Explosion(explosion_imgs, self.rect.center)
            self.scene.explosions.add(explosion)
            self.num_lives -= 1
            self.kill()

    def update(self):
        self.check_items()
        self.check_bombs()
        self.check_mobs()
        self.check_status()

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

    def __init__(self, image, location, shield, scene):
        super().__init__()

        self.image = image
        self.image_copy = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.fleet_loc = location
        self.shield = shield
        self.scene = scene
        self.attack_location = None
        self.angle = 0

    def drop_bomb(self):
        bomb = Bomb(bomb_img, [self.rect.centerx, self.rect.bottom])
        self.scene.bombs.add(bomb)

    def rotate(self):
        if self.attack_location is not None:
            center = self.rect.center
            dx = (self.attack_location[0] - self.rect.centerx)
            dy = (self.attack_location[1] - self.rect.centery)

            if dy == 0:
                angle_to_loc = 0
            else:
                angle_to_loc = round(math.degrees(math.atan(dx / dy)))

            if self.angle < angle_to_loc:
                self.angle += 1
            elif self.angle > angle_to_loc:
                self.angle -= 1

            self.image = pygame.transform.rotate(self.image_copy, self.angle)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = center
        else:
            self.image = self.image_copy

    def check_lasers(self):
        hit_list = pygame.sprite.spritecollide(self, self.scene.lasers, True,
                                                   pygame.sprite.collide_mask)

        for hit in hit_list:
            self.shield -= 1

    def check_status(self):
        if self.shield <= 0:
            explosion = Explosion(explosion_imgs, self.rect.center)
            self.scene.explosions.add(explosion)
            self.scene.ship.score += 1
            self.kill()

    def update(self):
        self.rotate()
        self.check_lasers()
        self.check_status()


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
        power_up_snd.play()

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

        explosion_snd.play()

    def update(self):
        self.ticks += 1

        if self.ticks % 3 == 0:
            self.image_index += 1

            if self.image_index < len(self.images):
                self.image = self.images[self.image_index]
            else:
                self.kill()


class Background:

    def __init__(self, image):
        w = image.get_width()
        h = image.get_height()

        self.image = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT + h])

        for x in range(0, SCREEN_WIDTH, w):
            for y in range(0, SCREEN_HEIGHT + h, h):
                self.image.blit(image, [x, y])

        self.rect = self.image.get_rect()
        self.rect.y = -1 * h
        self.scroll_speed = 4
        self.scroll_dist = h

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.scroll_speed
        if self.rect.y > 0:
            self.rect.y = -1 * self.scroll_dist

class Fleet(pygame.sprite.Group):

    def __init__(self, scene):
        super().__init__()

        self.scene = scene
        self.speed = 2
        self.bombs_per_second = 2.00

    def drop_bombs(self):
        for mob in self.sprites():
            r = random.randrange(0, 100 * FPS) / 100

            if r < self.bombs_per_second / len(self.sprites()):
                mob.drop_bomb()

    def move(self):
        for mob in self.sprites():
            if mob.attack_location is None:
                mob.rect.x += self.speed
                mob.fleet_loc[0] += self.speed
            else:
                mob.fleet_loc[0] += self.speed

                dx = (mob.attack_location[0] - mob.rect.centerx)
                dy = (mob.attack_location[1] - mob.rect.centery)

                if dx < 5 and dy < 5 :
                    mob.rect.center = [mob.fleet_loc[0], mob.fleet_loc[1]]
                    mob.attack_location = None
                else:
                    vx = 5 * dx / math.sqrt(dx ** 2 + dy ** 2)
                    vy = 5 * dy / math.sqrt(dx ** 2 + dy ** 2)
                    mob.rect.x += vx
                    mob.rect.y += vy

                if mob.rect.top > SCREEN_HEIGHT:
                    mob.rect.centery = -200
                    mob.attack_location = mob.fleet_loc

        hits_edge = False
        for mob in self.sprites():
            if (mob.fleet_loc[0] < 100 or mob.fleet_loc[0] > SCREEN_WIDTH - 100):
                hits_edge = True
        if hits_edge:
            self.speed *= -1

    def pick_attacker(self):
        if len(self.sprites()) > 0:
            attack_active = False
            for mob in self.sprites():
                if mob.attack_location is not None:
                    attack_active = True

            if not attack_active:
                r = random.randrange(0, 200)

                if r < 1:
                    attacker = random.choice(self.sprites())
                    x = random.randrange(75, SCREEN_WIDTH - 75)
                    y = SCREEN_HEIGHT + 100
                    attacker.attack_location = [x, y]

    def update(self):
        super().update()

        self.move()
        
        if self.scene.delay_timer == 0:
            self.drop_bombs()
            self.pick_attacker()
