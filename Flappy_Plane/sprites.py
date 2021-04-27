from settings import *


class Ground(pg.sprite.Sprite):
    def __init__(self, x, y, rot=None):
        super().__init__()
        self.x = x
        self.image = ground if rot == None else pg.transform.flip(ground, True, True)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x_pos = 0

    def update(self):
        self.x_pos += OBSTACLES_SPEED
        self.rect.x = self.x_pos if self.x == 0 else self.x_pos + WIDTH
        if self.x_pos <= -WIDTH:
            self.x_pos = 0


class Plane(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = plane_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.center = (PLAYER_POS)

        self.speedy = 0
        self.flap_height = -11

        self.frame = 0
        self.frame_rate = 0.75

        self.angle = 0
        self.rot_speed = 3.5
        self.flap_rot = 80
        self.rot_limit = -80

    def update(self):
        self.drop()
        self.animate()

    def drop(self):
        self.speedy += GRAVITY
        self.rect.y += self.speedy

    def jump(self):
        self.speedy = self.flap_height
        self.angle = self.flap_rot
        snds["wing.wav"].play()

    def animate(self):
        self.frame += self.frame_rate

        if self.frame + self.frame_rate >= len(plane_imgs) \
                or self.frame + self.frame_rate <= -len(plane_imgs):
            self.frame_rate *= -1

        old_center = self.rect.center
        self.image = self.rotate()
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def rotate(self):
        self.angle -= self.rot_speed
        img = pg.transform.rotate(plane_imgs[int(self.frame)], self.angle)
        if self.angle <= self.rot_limit:
            self.angle = self.rot_limit
        return img


class Obstacle(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_ch.convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = randint(HEIGHT - ground_height // 4, int(HEIGHT * 1.25))
        self.rect.left = WIDTH + 100

    def update(self):
        self.rect.x += OBSTACLES_SPEED

        if self.rect.right <= 0:
            self.kill()


class F_Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.transform.flip(obstacle_ch, True, True)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        rndm_y_pad = randint(175, 250)
        rndm_x_pad = randint(0, 250)
        self.rect.bottom = y - rndm_y_pad
        self.rect.left = x + rndm_x_pad

    def update(self):
        self.rect.x += OBSTACLES_SPEED

        if self.rect.right <= 0:
            self.kill()

class Pow(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = power_up
        self.rect = self.image.get_rect()
        self.rect.center = (x + randint(-200, 300), y - randint(10, 200))
        self.radius = 20

    def update(self):
        self.rect.x += OBSTACLES_SPEED


class Explosion(pg.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.center = center
        self.image = expl[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.center

        self.frame = 0
        self.frame_rate = 1
        self.last_frame = pg.time.get_ticks()
        self.wait_time = 100

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_frame >= self.wait_time:
            self.last_frame = now
            self.frame += self.frame_rate
            self.image = expl[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = self.center

        if self.frame + self.frame_rate >= len(expl):
            self.kill()
            self.frame = 0
