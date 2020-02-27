# Imports
import math
import random
from config import *
from sprites import *
from tools import *

# Scenes
class Scene:
    def __init__(self):
        self.next_scene = self

    def process_input(self, events, pressed_keys):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def terminate(self):
        self.next_scene = None


class TitleScene(Scene):
    def __init__(self):
        super().__init__()

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = PlayScene()

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        draw_text(screen, TITLE, font_xl, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 'center')


class PlayScene(Scene):
    def __init__(self):
        super().__init__()

        self.player = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.ship = Ship(ship_img, [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75], self)
        self.player.add(self.ship)

        self.level = 1
        pygame.mixer.music.load(main_theme)
        self.start_level()

    def start_level(self):
        if self.level == 1:
            mob1_locs =[[225, 100], [350, 100], [475, 100]]
            mob2_locs =[[100, 200], [225, 200], [350, 200], [475, 200], [600, 200]]
        elif self.level == 2:
            mob1_locs =[[225, 100], [350, 100], [475, 100]]
            mob2_locs =[[100, 200], [225, 200], [350, 200], [475, 200], [600, 200]]
        elif self.level == 3:
            mob1_locs =[[225, 100], [350, 100], [475, 100]]
            mob2_locs =[[100, 200], [225, 200], [350, 200], [475, 200], [600, 200]]

        for loc in mob1_locs:
            self.mobs.add( Mob(mob1_img, loc, self) )

        for loc in mob2_locs:
            self.mobs.add( Mob(mob2_img, loc, self) )

        x = random.randrange(50, SCREEN_WIDTH - 50)
        y = random.randrange(-2000, 0)
        double_shot = DoubleShot(double_shot_img, [x, y])
        self.items.add(double_shot)

        self.fleet_speed = 2
        self.bombs_per_second = 2.00

        pygame.mixer.music.play(-1)


    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == p1_controls['shoot']:
                    self.ship.shoot()

        if pressed_keys[p1_controls['left']]:
            self.ship.move_left()
        elif pressed_keys[p1_controls['right']]:
            self.ship.move_right()

    def move_fleet(self):
        for mob in self.mobs:
            if mob.attack_location is None:
                mob.rect.x += self.fleet_speed
                mob.fleet_loc[0] += self.fleet_speed
            else:
                mob.fleet_loc[0] += self.fleet_speed

                if mob.rect.centery < mob.fleet_loc[1]:
                    dx = (mob.fleet_loc[0] - mob.rect.centerx)
                    dy = (mob.fleet_loc[1] - mob.rect.centery)
                else:
                    dx = (mob.attack_location[0] - mob.rect.centerx)
                    dy = (mob.attack_location[1] - mob.rect.centery)

                if dx < 5 and dy < 5:
                    mob.rect.center = [mob.fleet_loc[0], mob.fleet_loc[1]]
                    mob.attack_location = None
                elif dx != 0 or dy != 0:
                    vx = 5 * dx / math.sqrt(dx ** 2 + dy ** 2)
                    vy = 5 * dy / math.sqrt(dx ** 2 + dy ** 2)
                    mob.rect.x += vx
                    mob.rect.y += vy

                if mob.rect.top > SCREEN_HEIGHT:
                    mob.rect.centery = -200

        hits_edge = False
        for mob in self.mobs:
            #if mob.rect.left < 0 or mob.rect.right > SCREEN_WIDTH:
            if (mob.rect.centerx < 100 or mob.fleet_loc[0] < 100 or
                mob.rect.centerx > SCREEN_WIDTH - 100 or mob.fleet_loc[0] > SCREEN_WIDTH - 100):
                hits_edge = True
        if hits_edge:
            self.fleet_speed *= -1

    def drop_bombs(self):
        for mob in self.mobs:
            r = random.randrange(0, 100 * FPS) / 100

            if r < self.bombs_per_second / len(self.mobs):
                mob.drop_bomb(self.bombs)

    def pick_attacker(self):
        if len(self.mobs) > 0:
            attack_active = False
            for mob in self.mobs:
                if mob.attack_location is not None:
                    attack_active = True

            if not attack_active:
                r = random.randrange(0, 200)

                if r < 1:
                    attacker = random.choice(self.mobs.sprites())
                    x = random.randrange(0, SCREEN_WIDTH)
                    y = SCREEN_HEIGHT + 100
                    attacker.attack_location = [x, y]

    def check_status(self):
        if len(self.player) == 0 and len(self.explosions) == 0:
            self.next_scene = EndScene()
        elif len(self.mobs) == 0:
            if self.level < 3:
                self.level += 1
                self.start_level()
            else:
                self.next_scene = EndScene()

    def display_stats(self):
        draw_text(screen, 'Level: ' + str(self.level), font_md, WHITE, [20, 20], 'topleft')
        draw_text(screen, 'Score: ' + str(self.ship.score), font_md, WHITE, [SCREEN_WIDTH - 20, 20], 'topright')

    def update(self):
        self.player.update()
        self.mobs.update()
        self.lasers.update()
        self.bombs.update()
        self.items.update()
        self.explosions.update()

        self.move_fleet()
        self.drop_bombs()
        self.pick_attacker()

        self.check_status()

    def render(self):
        screen.fill(BLACK)
        self.player.draw(screen)
        self.lasers.draw(screen)
        self.mobs.draw(screen)
        self.bombs.draw(screen)
        self.items.draw(screen)
        self.explosions.draw(screen)
        self.display_stats()


class EndScene(Scene):
    def __init__(self):
        super().__init__()

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = TitleScene()

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        draw_text(screen, "Game Over", font_lg, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 'center')
