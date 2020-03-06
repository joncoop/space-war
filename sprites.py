import math
import random
from config import *

# Player
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
        self.num_lives = NUM_LIVES
        self.shoots_double = False
        self.score = 0

    def move_left(self):
        self.rect.x -= SHIP_SPEED

        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += SHIP_SPEED

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        num_lasers = len(self.scene.lasers)

        if self.shoots_double and num_lasers < 3:
            laser1 = Laser(laser_img, [self.rect.left, self.rect.centery])
            laser2 = Laser(laser_img, [self.rect.right, self.rect.centery])
            self.scene.lasers.add(laser1, laser2)
            laser_snd.play()
            return 2
        elif num_lasers < 2:
            laser = Laser(laser_img, [self.rect.centerx, self.rect.top])
            self.scene.lasers.add(laser)
            laser_snd.play()
            return 1

        return 0

    def check_items(self):
        hit_list = pygame.sprite.spritecollide(self, self.scene.items, True, pygame.sprite.collide_mask)

        for item in hit_list:
            item.apply(self)

    def check_bombs(self):
        hit_list = pygame.sprite.spritecollide(self, self.scene.bombs, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.die()

    def check_mobs(self):
        hit_list = pygame.sprite.spritecollide(self, self.scene.mobs, False, pygame.sprite.collide_mask)

        for mob in hit_list:
            mob.die()
            self.die()

    def die(self):
        self.alive = False
        self.num_lives -= 1
        self.kill()

        explosion = Explosion(explosion_imgs, self.rect.center)
        self.scene.explosions.add(explosion)

    def respawn(self):
        self.rect.center = self.spawn_loc
        self.alive = True
        self.scene.player.add(self)

    def update(self):
        self.check_items()
        self.check_bombs()
        self.check_mobs()


# Enemies
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

        if self.shield == 1:
            self.value = MOB1_VALUE
        else:
            self.value = MOB2_VALUE

    def drop_bomb(self):
        bomb = Bomb(bomb_img, [self.rect.centerx, self.rect.bottom])
        self.scene.bombs.add(bomb)

    def get_angle_to_loc(self, loc):
        dx = (loc[0] - self.rect.centerx)
        dy = (loc[1] - self.rect.centery)

        if dy == 0:
            angle = 0
        else:
            angle = round(math.degrees(math.atan(dx / dy)))

        return angle

    def rotate(self, angle):
        if angle != self.angle:
            center = self.rect.center

            if abs(self.angle - angle) > 5:
                rotate_amount = 3
            else:
                rotate_amount = 1

            if self.angle < angle:
                self.angle += rotate_amount
            elif self.angle > angle:
                self.angle -= rotate_amount

            self.image = pygame.transform.rotate(self.image_copy, self.angle)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = center

    def attack(self):
        dx = (self.attack_location[0] - self.rect.centerx)
        dy = (self.attack_location[1] - self.rect.centery)

        if dx < MOB_ATTACK_SPEED and dy < MOB_ATTACK_SPEED:
            self.rect.center = [self.fleet_loc[0], self.fleet_loc[1]]
            self.attack_location = None
        else:
            vx = MOB_ATTACK_SPEED * dx / math.sqrt(dx ** 2 + dy ** 2)
            vy = MOB_ATTACK_SPEED * dy / math.sqrt(dx ** 2 + dy ** 2)
            self.rect.x += vx
            self.rect.y += vy

        if self.rect.top > SCREEN_HEIGHT:
            self.rect.centery = -200
            self.attack_location = self.fleet_loc

        if self.rect.centery > self.fleet_loc[1]:
            r = random.randrange(0, 100)
            if r == 0:
                self.set_attack_location()

    def check_lasers(self):
        hit_list = pygame.sprite.spritecollide(self, self.scene.lasers, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            self.shield -= 1

        if self.shield <= 0:
            self.die()

    def set_attack_location(self):
        x = random.randrange(75, SCREEN_WIDTH - 75)
        y = SCREEN_HEIGHT + 100
        self.attack_location = [x, y]

    def die(self):
        explosion = Explosion(explosion_imgs, self.rect.center)
        self.scene.explosions.add(explosion)
        self.scene.ship.score += self.value
        self.kill()

    def update(self):
        if self.attack_location is not None:
            angle = self.get_angle_to_loc(self.attack_location)
        else:
            angle = self.get_angle_to_loc(self.rect.center)

        self.rotate(angle)
        self.check_lasers()


class Fleet(pygame.sprite.Group):

    def __init__(self, scene):
        super().__init__()

        self.scene = scene
        self.speed = FLEET_SPEED

    def drop_bombs(self):
        if len(self.sprites()) > 0:
            bombs_per_second = 0.25 * self.scene.level / len(self.sprites())

            for mob in self.sprites():
                r = random.randrange(0, 100 * FPS) / 100

                if r < bombs_per_second:
                    mob.drop_bomb()

    def move(self):
        hits_edge = False

        for mob in self.sprites():
            mob.fleet_loc[0] += self.speed

            if mob.attack_location is None:
                mob.rect.x += self.speed

                if mob.fleet_loc[0] < 100 or mob.fleet_loc[0] > SCREEN_WIDTH - 100:
                    hits_edge = True
            else:
                mob.attack()

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
                    attacker.set_attack_location()

    def update(self):
        super().update()
        self.move()

        if self.scene.state == PLAYING:
            self.drop_bombs()
            self.pick_attacker()


# Projectiles
class Laser(pygame.sprite.Sprite):

    def __init__(self, image, location):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = location

    def update(self):
        self.rect.y -= LASER_SPEED

        if self.rect.bottom < 0:
            self.kill()


class Bomb(pygame.sprite.Sprite):

    def __init__(self, image, location):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = location

    def update(self):
        self.rect.y += BOMB_SPEED

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Power-ups
class DoubleShot(pygame.sprite.Sprite):

    def __init__(self, image, location):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.value = POWERUP_VALUE

    def apply(self, ship):
        ship.shoots_double = True
        ship.score += self.value
        power_up_snd.play()

    def update(self):
        self.rect.y += POWERUP_SPEED

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Background and effects
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
