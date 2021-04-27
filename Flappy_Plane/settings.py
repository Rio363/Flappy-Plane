from random import randint, random
import pygame as pg
from os import path

pg.mixer.init()

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snds")

WIDTH, HEIGHT = 900, 600
FPS = 60
TITLE = "Flappy Plane"
ICON = pg.image.load(path.join(img_dir, "icon.png"))

# Starting vars....
GRAVITY = 0.7
BACKGROUND_SPEED = -1.5
PLAYER_POS = (100, 300)
OBSTACLES_SPEED = -14
# OBSTACLE_X_PAD = 200
# OBSTACLE_Y_PAD = 200


# Define Colors....
BLACK = (0, 0, 0)

# Some VARS...
weather = "grass"  # grass/dirt/snow/ice
plane_color = "red"  # red/yellow/blue/green
pow_color = "gold"  # gold/silver/bronze

# load all image files...
background = pg.transform.scale(pg.image.load(path.join(img_dir, "background.png")), (WIDTH, HEIGHT))
ground_height = 100
ground = pg.transform.scale(pg.image.load(path.join(img_dir, f"ground{weather}.png")), (WIDTH, ground_height))
plane_imgs = [pg.transform.scale(pg.image.load(path.join(img_dir, "planes", f"Plane{plane_color}{i}.png")), (82, 68))
              for i in range(1, 4)]
obstacle_ch = pg.transform.scale(pg.image.load(path.join(img_dir, f"rock{weather}.png")), (126, 280))

# number0.png
nums = [pg.image.load(path.join(img_dir, "numbers", f"number{i}.png")) for i in range(10)]
num_dict = {str(k): v for k, v in zip(range(10), nums)}

# letterA.png
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "o", "p", "q", "r", "s", "t", "u", "v", "w",
           "x", "y", "z"]
letter_imgs = [pg.image.load(path.join(img_dir, 'letters', f"Letter{l}.png")) for l in letters]
letter_dict = {k: v for k, v in zip(letters, letter_imgs)}

# Combine them all in one dict for chars....
char_dict = {}
char_dict.update(num_dict)
char_dict.update(letter_dict)

power_up = pg.transform.scale(pg.image.load(path.join(img_dir, "ui", f"medal{pow_color}.png")), (50, 56))

tapLeft = pg.image.load(path.join(img_dir, "ui", "tapLeft.png"))
tapRight = pg.image.load(path.join(img_dir, "ui", "tapRight.png"))
tapTick = pg.image.load(path.join(img_dir, "ui", "tapTick.png"))

expl = [pg.image.load(path.join(img_dir, "expl", f"sonicExplosion0{i}.png")) for i in range(9)]

# load all sound files...
import os

snds = {k: pg.mixer.Sound(path.join(snd_dir, snd)) for k, snd in zip(os.listdir("snds"), os.listdir("snds"))}
