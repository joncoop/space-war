from config import *
from save import *
from sprites import *
from tools import *


# Base scene
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


# Game scenes
class TitleScene(Scene):

    def __init__(self):
        super().__init__()

        self.background = Background(background_img)

        load_music(start_theme)
        play_music()

        self.high_score = read_high_score()

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.next_scene = PlayScene()
            if event.type == pygame.JOYBUTTONDOWN:
                if gamepad.get_button(9):
                    self.next_scene = PlayScene()

    def update(self):
        self.background.update()

    def render(self):
        screen.fill(BLACK)
        self.background.draw(screen)

        draw_text(screen, TITLE, font_xl, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100], 'center')
        screen.blit(ship_img, [SCREEN_WIDTH // 2 - ship_img.get_width() // 2, SCREEN_HEIGHT // 2 - 32])
        draw_text(screen, 'Press any key to begin.', font_sm, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100],
                  'center')


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
        self.ship = Ship(ship_img, [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 85], self)
        self.player.add(self.ship)

        self.level = 1
        self.delay_timer = 2 * FPS
        self.state = INTRO
        self.extra_life_index = 0

        self.high_score = read_high_score()
        self.num_lives = NUM_LIVES
        self.score = 0
        self.start_level()

        load_music(main_theme)
        play_music()

    # noinspection PyAttributeOutsideInit
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
        y = random.randrange(-5000, -1000)
        double_shot = DoubleShot(double_shot_img, [x, y], self)
        self.items.add(double_shot)

        self.shots_fired = 0
        self.shots_needed = 0
        for mob in self.mobs:
            self.shots_needed += mob.shield

        unpause_music()

    # noinspection PyAttributeOutsideInit
    def check_status(self):
        if self.delay_timer == 0:
            if self.num_lives == 0:
                self.state = GAME_OVER
                self.delay_timer = 20 * FPS
                stop_music()
                end_snd.play()

                if self.score >= self.high_score:
                    save_high_score(self.high_score)

            elif not self.ship.alive:
                self.state = SHIP_KILLED
                self.delay_timer = 3 * FPS

            elif len(self.mobs) == 0:
                self.state = STAGE_CLEARED
                self.accuracy = min(100, round(100 * self.shots_needed / self.shots_fired))
                self.misses = self.shots_fired - self.shots_needed
                self.bonus = self.accuracy

                if self.accuracy == 100:
                    self.bonus_multiplier = 5
                elif self.accuracy >= 90:
                    self.bonus_multiplier = 3
                elif self.accuracy >= 80:
                    self.bonus_multiplier = 2
                else:
                    self.bonus_multiplier = 1

                self.delay_timer = 3 * self.accuracy + 3 * FPS
                pause_music()
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

        if self.extra_life_index < len(EXTRA_SHIP_AT) and self.score >= EXTRA_SHIP_AT[self.extra_life_index]:
            self.num_lives += 1
            self.extra_life_index += 1

        self.high_score = max(self.high_score, self.score)

    def display_stats(self):
        score_str = f'Score: {self.score}'
        level_str = f'Level: {self.level}'
        high_score_str = f'High: {self.high_score}'
        draw_text(screen, score_str, font_sm, WHITE, [10, 10], 'topleft')
        draw_text(screen, level_str, font_sm, WHITE, [10, 40], 'topleft')
        draw_text(screen, high_score_str, font_sm, WHITE, [SCREEN_WIDTH - 10, 10], 'topright')

        extra_lives = self.num_lives - 1

        if self.state == SHIP_KILLED:
            extra_lives += 1

        y = SCREEN_HEIGHT - 40
        for n in range(extra_lives):
            x = 16 + 50 * n
            screen.blit(ship_icon, [x, y])

        if self.state == INTRO:
            draw_text(screen, 'Get ready!', font_lg, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 'center')
        elif self.state == GAME_OVER:
            draw_text(screen, 'Game over', font_lg, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 'center')
        elif self.state == STAGE_CLEARED:
            draw_text(screen, 'Stage cleared!', font_lg, WHITE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80], 'center')
            w, _ = get_text_size(f'Shots fired: {self.shots_fired}', font_sm)
            x = SCREEN_WIDTH // 2 - w // 2

            shot_str = f'Shots fired: {self.shots_fired}'
            miss_str = f'Misses: {self.misses}'
            accuracy_str = f'Accuracy: {self.accuracy}%'
            bonus_str = f'Bonus: {self.bonus}'
            if self.bonus_multiplier > 1:
                bonus_str += f'\u00D7{self.bonus_multiplier}'

            draw_text(screen, shot_str, font_sm, WHITE, [x, SCREEN_HEIGHT // 2 - 30], 'midleft')
            draw_text(screen, miss_str, font_sm, WHITE, [x, SCREEN_HEIGHT // 2], 'midleft')
            draw_text(screen, accuracy_str, font_sm, WHITE, [x, SCREEN_HEIGHT // 2 + 30], 'midleft')
            draw_text(screen, bonus_str, font_sm, WHITE, [x, SCREEN_HEIGHT // 2 + 60], 'midleft')

            if self.bonus > 0 and self.delay_timer % 3 == 0 and self.delay_timer < 3 * self.accuracy + 1.5 * FPS:
                self.score += 1 * self.bonus_multiplier
                self.bonus -= 1
                if self.delay_timer % 2 == 0:
                    point_snd.play()

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == CONTROLS['shoot']:
                    if self.state == PLAYING:
                        self.shots_fired += self.ship.shoot()
                if event.key == CONTROLS['restart']:
                    self.next_scene = TitleScene()
                elif event.key == pygame.K_i:
                    self.ship.invincible = not self.ship.invincible

            if event.type == pygame.JOYBUTTONDOWN:
                if gamepad.get_button(1):
                    if self.state == PLAYING:
                        self.shots_fired += self.ship.shoot()
                elif gamepad.get_button(8):
                    self.next_scene = TitleScene()

        if self.state == PLAYING or self.state == STAGE_CLEARED:
            if pressed_keys[CONTROLS['left']]:
                self.ship.move_left()
            elif pressed_keys[CONTROLS['right']]:
                self.ship.move_right()

            if gamepad is not None:
                if gamepad.get_axis(0) < 0:
                    self.ship.move_left()
                elif gamepad.get_axis(0) > 0:
                    self.ship.move_right()

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
        self.lasers.draw(screen)
        self.bombs.draw(screen)
        self.items.draw(screen)
        self.player.draw(screen)
        self.mobs.draw(screen)
        self.explosions.draw(screen)
        self.display_stats()


class EndScene(Scene):

    def __init__(self):
        super().__init__()
        stop_music()

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
