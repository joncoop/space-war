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
        pygame.mixer.music.stop()

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.next_scene = PlayScene()

    def update(self):
        self.background.update()

    def render(self):
        screen.fill(BLACK)
        self.background.draw(screen)

        draw_text(screen, TITLE, font_xl, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100], 'center')
        screen.blit(ship_img, [SCREEN_WIDTH // 2 - ship_img.get_width() // 2, SCREEN_HEIGHT // 2 - 32])
        draw_text(screen, 'Press any key to begin.', font_sm, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100], 'center')


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
        self.next_extra_life = 2000

        pygame.mixer.music.load(main_theme)

        self.start_level()

    def start_level(self):
        centerx = SCREEN_WIDTH // 2
        spacing = 125

        row1 = [[centerx - spacing, 100],
                [centerx, 100],
                [centerx + spacing, 100]]
        row2 = [[centerx - 2 * spacing, 200],
                [centerx - spacing, 200],
                [centerx, 200],
                [centerx + spacing, 200],
                [centerx + 2 * spacing, 200]]
        row3 = [[centerx - 2 * spacing, 300],
                [centerx - spacing, 300],
                [centerx, 300],
                [centerx + spacing, 300],
                [centerx + 2 * spacing, 300]]

        for loc in row1:
            self.mobs.add(Mob(mob1_img, loc, 3, self))

        for loc in row2:
            self.mobs.add(Mob(mob2_img, loc, 1, self))

        for loc in row3:
            self.mobs.add(Mob(mob2_img, loc, 1, self))

        x = random.randrange(50, SCREEN_WIDTH - 50)
        y = random.randrange(-3000, -1000)
        double_shot = DoubleShot(double_shot_img, [x, y])
        self.items.add(double_shot)

        self.shots_fired = 0
        self.shots_needed = 0
        for mob in self.mobs:
            self.shots_needed += mob.shield

        pygame.mixer.music.play(-1)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == p1_controls['shoot']:
                    if self.state == PLAYING:
                        self.shots_fired += self.ship.shoot()
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
                pygame.mixer.music.stop()
            elif self.ship.shield <= 0:
                self.state = SHIP_KILLED
                self.delay_timer = 2 * FPS
            elif len(self.mobs) == 0:
                self.state = STAGE_CLEARED
                self.accuracy = round(100 * self.shots_needed / self.shots_fired)
                self.bonus = self.accuracy
                self.delay_timer = 3 * self.accuracy + FPS
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

        if self.ship.score >= self.next_extra_life:
            self.ship.num_lives += 1
            self.next_extra_life = 100000000

    def display_stats(self):
        draw_text(screen, str(self.ship.score), font_md, WHITE, [SCREEN_WIDTH // 2, 8], 'midtop')
        draw_text(screen, 'Level: ' + str(self.level), font_md, WHITE, [SCREEN_WIDTH - 16, SCREEN_HEIGHT], 'bottomright')

        extra_lives = self.ship.num_lives - 1

        if self.state == SHIP_KILLED:
            extra_lives += 1

        y = SCREEN_HEIGHT - 40
        for n in range(extra_lives):
            x = 16 + 50 * n
            screen.blit(ship_icon, [x, y])

        if self.state == INTRO:
            draw_text(screen, 'Get Ready!', font_lg, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 'center')
        elif self.state == GAME_OVER:
            draw_text(screen, 'Game Over', font_lg, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 'center')
        elif self.state == STAGE_CLEARED:
            draw_text(screen, 'Stage cleared!', font_lg, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80], 'center')
            text = font_sm.render("Shots fired: " + str(self.shots_fired), True, WHITE)
            x = SCREEN_WIDTH // 2 - text.get_rect().width // 2
            draw_text(screen, 'Shots fired: ' + str(self.shots_fired), font_sm, WHITE, [x, SCREEN_HEIGHT // 2 - 30], 'midleft')
            draw_text(screen, 'Misses: ' + str(self.shots_fired - self.shots_needed), font_sm, WHITE, [x, SCREEN_HEIGHT // 2], 'midleft')
            draw_text(screen, 'Accuracy: ' + str(self.accuracy) + "%", font_sm, WHITE, [x, SCREEN_HEIGHT // 2 + 30], 'midleft')
            draw_text(screen, 'Bonus: ' + str(self.bonus), font_sm, WHITE, [x, SCREEN_HEIGHT // 2 + 60], 'midleft')

            if self.bonus > 0 and self.delay_timer % 3 == 0:
                self.ship.score += 1
                self.bonus -= 1

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
