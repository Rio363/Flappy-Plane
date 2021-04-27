from sprites import *
import shelve

shelve_file = shelve.open("data")
shelve_file.setdefault("score", 0)


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        pg.display.set_icon(ICON)
        self.clock = pg.time.Clock()

        # Game VARS...
        self.running = True
        self.splash = True
        self.score = 0
        self.highest_score = shelve_file.get("score", 0)

        self.background_x = 0
        self.ground_x = 0

        self.SPAWNOBSTACLE = pg.USEREVENT
        pg.time.set_timer(self.SPAWNOBSTACLE, 1400)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.ground_group = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.flipped_obstacles = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()

        self.plane = Plane()
        self.all_sprites.add(self.plane)

        self.ground = Ground(0, HEIGHT - ground_height)
        self.ground2 = Ground(WIDTH, HEIGHT - ground_height)
        self.ground3 = Ground(0, 0, rot="not None")
        self.ground4 = Ground(WIDTH, 0, rot="not None")

        self.all_sprites.add(self.ground)
        self.all_sprites.add(self.ground2)
        self.all_sprites.add(self.ground3)
        self.all_sprites.add(self.ground4)

        self.ground_group.add(self.ground)
        self.ground_group.add(self.ground2)
        self.ground_group.add(self.ground3)
        self.ground_group.add(self.ground4)

        self.run()

    def get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                # self.running = False
                # self.playing = False
                self.reset()

            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.plane.jump()

            if event.type == self.SPAWNOBSTACLE:
                if random() > 0.05:
                    self.obstacle = Obstacle()
                    self.obstacles.add(self.obstacle)
                    if random() > 0.1:
                        self.f_obstacle = F_Obstacle(self.obstacle.rect.x, self.obstacle.rect.top)
                        self.obstacles.add(self.f_obstacle)
                        self.flipped_obstacles.add(self.f_obstacle)
                    if random() > 0.65:  # Add coin/power_up
                        pow = Pow(self.obstacle.rect.centerx, self.obstacle.rect.top)
                        self.all_sprites.add(pow)
                        self.power_ups.add(pow)

    def run(self):
        self.playing = True

        while self.playing and not self.splash:
            self.clock.tick(FPS)
            self.get_events()
            self.update()
            self.draw()
            self.auto_pilot("off")

    def update(self):
        self.all_sprites.update()
        self.obstacles.update()
        self.check_collisions()
        self.update_score()

    def draw(self):
        self.screen.fill(BLACK)

        self.draw_background()
        self.obstacles.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.draw_score(int(self.score), char_dict, WIDTH / 2 - 10, 20)

        pg.display.update()

    def show_splash_screen(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False
                # self.playing = False

            if event.type == pg.KEYDOWN:
                self.splash = False

        self.screen.fill(BLACK)
        self.draw_background()
        self.draw_splash_ground()
        self.screen.blit(plane_imgs[0], PLAYER_POS)
        self.screen.blit(tapLeft, (200, 320))
        self.screen.blit(tapRight, (10, 320))
        self.screen.blit(tapTick, (150, 390))
        self.draw_score("score", letter_dict, WIDTH - WIDTH / 4 - 100, HEIGHT / 4 + 60)
        self.draw_score(int(self.highest_score), num_dict, WIDTH - WIDTH / 4 - 80, HEIGHT / 4 + 160)

        pg.display.flip()

    def update_score(self):
        for obstacle in self.obstacles:
            if obstacle.rect.right <= 10 and obstacle.rect.y >= HEIGHT / 2:  # Check the bottom obstacles only
                # coz self.obstacles have both
                self.score += 2
                snds["swooshing.wav"].play()

    def draw_score(self, txt, lst, x, y):
        x = x - 25 * len(str(txt))  # to kinda center it
        for idx, ch in enumerate(str(txt)):
            x_pad = 60
            # Exceptions for some letter and number...
            if ch == "i":
                x_pad = 63
            self.screen.blit(lst[ch], (x + x_pad * idx, y))

    def draw_background(self):
        self.background_x += BACKGROUND_SPEED
        if self.background_x <= -WIDTH:
            self.background_x = 0
        self.screen.blit(background, (self.background_x, 0))
        self.screen.blit(background, (self.background_x + WIDTH, 0))

    def draw_splash_ground(self):
        self.ground_x += OBSTACLES_SPEED
        if self.ground_x <= -WIDTH:
            self.ground_x = 0
        self.screen.blit(ground, (self.ground_x, HEIGHT - ground_height))
        self.screen.blit(ground, (self.ground_x + WIDTH, HEIGHT - ground_height))
        self.screen.blit(pg.transform.flip(ground, True, True), (self.ground_x, 0))
        self.screen.blit(pg.transform.flip(ground, True, True), (self.ground_x + WIDTH, 0))

    def check_collisions(self):
        # Collision between plane/ground
        if pg.sprite.spritecollideany(self.plane, self.ground_group):
            if pg.sprite.spritecollide(self.plane, self.ground_group, False, pg.sprite.collide_mask):
                e = Explosion(self.plane.rect.center)
                self.all_sprites.add(e)
                snds["hit.wav"].play()
                self.reset()

        # Collision between plane/Obstacles
        if pg.sprite.spritecollideany(self.plane, self.obstacles):
            if pg.sprite.spritecollide(self.plane, self.obstacles, False, pg.sprite.collide_mask):
                e = Explosion(self.plane.rect.center)
                self.all_sprites.add(e)
                snds["hit.wav"].play()
                self.reset()

        # Collision between plane/power_ups
        if pg.sprite.spritecollide(self.plane, self.power_ups, True, pg.sprite.collide_circle):
            self.score += 10
            snds["point.wav"].play()

    def reset(self):
        if self.score > self.highest_score:
            self.highest_score = self.score
            shelve_file['score'] = self.score

        self.splash = True
        self.score = 0

    def auto_pilot(self, on_off=None):
        if on_off is None:
            for obs in self.obstacles:
                if self.plane.rect.bottom + 10 >= obs.rect.top and obs.rect.bottom >= HEIGHT/1.5\
                   and obs.rect.x <= WIDTH/2.5 and obs.rect.left >= self.plane.rect.left:
                    self.plane.jump()
            if self.plane.rect.bottom + 10 >= HEIGHT-ground_height:
                self.plane.jump()

g = Game()
while g.running:
    g.new()
    g.show_splash_screen()
