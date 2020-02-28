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

        self.background = Background(background_img)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = PlayScene()

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        self.background.draw(screen)

        draw_text(screen, TITLE, font_xl, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 'center')


class PlayScene(Scene):
    def __init__(self):
        super().__init__()

        self.player = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.mobs = Fleet(self)
        self.items = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.background = Background(background_img)
        self.ship = Ship(ship_img, [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75], self)
        self.player.add(self.ship)

        self.level = 1
        self.delay_timer = 0
        self.game_over = False

        pygame.mixer.music.load(main_theme)
        pygame.mixer.music.play(-1)

        self.start_level()

    def start_level(self):
        mob1_locs =[[225, 100], [350, 100], [475, 100]]
        mob2_locs =[[100, 200], [225, 200], [350, 200], [475, 200], [600, 200]]

        for loc in mob1_locs:
            self.mobs.add( Mob(mob1_img, loc, 3, self) )

        for loc in mob2_locs:
            self.mobs.add( Mob(mob2_img, loc, 1, self) )

        x = random.randrange(50, SCREEN_WIDTH - 50)
        y = random.randrange(-2000, 0)
        double_shot = DoubleShot(double_shot_img, [x, y])
        self.items.add(double_shot)

        self.mobs.speed = 2
        self.mobs.bombs_per_second = self.level

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == p1_controls['shoot']:
                    if len(self.player) > 0:
                        self.ship.shoot()
                if event.key == p1_controls['restart']:
                    self.next_scene = TitleScene()

        if pressed_keys[p1_controls['left']]:
            self.ship.move_left()
        elif pressed_keys[p1_controls['right']]:
            self.ship.move_right()

    def check_status(self):
        if self.ship.num_lives == 0:
            self.game_over = True
        elif self.ship.shield <= 0:
            self.delay_timer = 2 * FPS
            self.ship.shield = 1
        elif len(self.mobs) == 0:
            self.level += 1
            self.start_level()

        if self.game_over:
            pygame.mixer.music.stop()

    def display_stats(self):
        draw_text(screen, 'Level: ' + str(self.level), font_md, WHITE, [20, 20], 'topleft')
        draw_text(screen, 'Score: ' + str(self.ship.score), font_md, WHITE, [SCREEN_WIDTH - 20, 20], 'topright')

        y = SCREEN_HEIGHT - 48
        for n in range(self.ship.num_lives):
            x = 16 + 50 * n
            screen.blit(ship_icon, [x, y])

        if self.ship.num_lives == 0:
            draw_text(screen, "Game Over", font_lg, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 'center')
        elif len(self.mobs) == 0:
            draw_text(screen, "Stage cleared!", font_lg, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 'center')

    def update(self):
        self.background.update()
        self.mobs.update()
        self.lasers.update()
        self.bombs.update()
        self.items.update()
        self.explosions.update()

        if self.delay_timer == 0:
            self.player.update()
            self.check_status()
            if self.delay_timer == 0 and self.ship.num_lives > 0 and len(self.player) == 0:
                self.ship.respawn()
        else:
            self.delay_timer -= 1

    def render(self):
        screen.fill(BLACK)
        self.background.draw(screen)
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
        pygame.mixer.music.stop()

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
