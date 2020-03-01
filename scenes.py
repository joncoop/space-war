# Imports
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
        self.background.update()

    def render(self):
        screen.fill(BLACK)
        self.background.draw(screen)

        draw_text(screen, TITLE, font_xl, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50], 'center')
        screen.blit(ship_img, [SCREEN_WIDTH // 2 - ship_img.get_width() // 2, SCREEN_HEIGHT // 2 + 10])


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
        self.delay_timer = 2 * FPS
        self.state = INTRO

        pygame.mixer.music.load(main_theme)
        pygame.mixer.music.play(-1)

        self.start_level()

    def start_level(self):
        mob1_locs = [[225, 100], [350, 100], [475, 100]]
        mob2_locs = [[100, 200], [225, 200], [350, 200], [475, 200], [600, 200]]

        for loc in mob1_locs:
            self.mobs.add(Mob(mob1_img, loc, 3, self))

        for loc in mob2_locs:
            self.mobs.add(Mob(mob2_img, loc, 1, self))

        x = random.randrange(50, SCREEN_WIDTH - 50)
        y = random.randrange(-3000, -1000)
        double_shot = DoubleShot(double_shot_img, [x, y])
        self.items.add(double_shot)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == p1_controls['shoot']:
                    if self.state == PLAYING:
                        self.ship.shoot()
                if event.key == p1_controls['restart']:
                    self.next_scene = TitleScene()

        if self.state == PLAYING or self.state == STAGE_CLEARED:
            if pressed_keys[p1_controls['left']]:
                self.ship.move_left()
            elif pressed_keys[p1_controls['right']]:
                self.ship.move_right()

    def check_status(self):
        if self.delay_timer == 0:
            if self.ship.num_lives == 0:
                self.state = GAME_OVER
                self.delay_timer = 20 * FPS
            elif self.ship.shield <= 0:
                self.state = SHIP_KILLED
                self.delay_timer = 2 * FPS
            elif len(self.mobs) == 0:
                self.state = STAGE_CLEARED
                self.delay_timer = 2 * FPS
        else:
            self.delay_timer -= 1

            if self.delay_timer == 0:
                if self.state == INTRO:
                    self.state = PLAYING
                elif self.state == SHIP_KILLED:
                    self.state = PLAYING
                    self.ship.respawn()
                elif self.state == STAGE_CLEARED:
                    self.state = PLAYING
                    self.level += 1
                    self.start_level()
                elif self.state == GAME_OVER:
                    self.next_scene = TitleScene()

    def display_stats(self):
        draw_text(screen, str(self.ship.score), font_md, WHITE, [SCREEN_WIDTH // 2, 8], 'midtop')
        draw_text(screen, 'Level: ' + str(self.level), font_md, WHITE, [SCREEN_WIDTH - 16, SCREEN_HEIGHT], 'bottomright')

        y = SCREEN_HEIGHT - 40
        for n in range(self.ship.num_lives):
            x = 16 + 50 * n
            screen.blit(ship_icon, [x, y])

        if self.state == INTRO:
            draw_text(screen, "Get Ready!", font_lg, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 'center')
        elif self.state == GAME_OVER:
            draw_text(screen, "Game Over", font_lg, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 'center')
        elif self.state == STAGE_CLEARED:
            draw_text(screen, "Stage cleared!", font_lg, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 'center')

    def update(self):
        self.background.update()
        self.mobs.update()
        self.lasers.update()
        self.bombs.update()
        self.items.update()
        self.explosions.update()

        if self.state == PLAYING or self.state == STAGE_CLEARED:
            self.player.update()

        self.check_status()

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
