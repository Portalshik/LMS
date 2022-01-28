import pygame
import os
import json


with open('config.json') as cat_file:
    data = json.load(cat_file)
volume = data["volume"]
playerPicture = data["playerPicture"]
levelNum = data["levelNum"]


class MainMenu:
    def __init__(self, name_of_file, coords=(0, 0), resize=None, special=None):
        self.button = pygame.sprite.Sprite()
        self.func = None
        self.special = special
        if resize is not None:
            name_of_file = pygame.image.load(name_of_file)
            name_of_file = pygame.transform.scale(name_of_file, resize)
            self.button.image = name_of_file
        else:
            self.button.image = pygame.image.load(name_of_file)
        self.button.rect = self.button.image.get_rect()
        self.button.rect.x = coords[0] - list(self.button.rect)[2] // 2
        self.button.rect.y = coords[1]

    def add_function(self, func):
        self.func = func

    def function(self):
        self.func()


class ButtonGroup:
    def __init__(self):
        self.group = {}

    def add(self, *args):
        for button in args:
            self.group[button] = [range(button.button.rect.x, button.button.rect.x + list(button.button.rect)[2]),
                                  range(button.button.rect.y, button.button.rect.y + list(button.button.rect)[3])]

    def on_click(self, mouse_pos):
        for i in self.group:
            if mouse_pos[0] in self.group[i][0] and mouse_pos[1] in self.group[i][1]:
                i.function()


running = True
flag = False
size = (800, 700)
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
group = ButtonGroup()
levels = ButtonGroup()
levelSprites = pygame.sprite.Group()
play_button = MainMenu("DATA/play_button.png", (size[0] // 2, size[1] // 2))
settings = MainMenu("DATA/settings.png", (700, 10))
chooseLevel = MainMenu("DATA/menu.png", (75, 10), resize=(100, 100))


@play_button.add_function
def play():
    os.system("python game.py")


@settings.add_function
def setting():
    os.system("python settings.py")


@chooseLevel.add_function
def choose_level():
    global flag
    flag = not flag


group.add(play_button, settings, chooseLevel)
all_sprites.add(play_button.button, settings.button, chooseLevel.button)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            group.on_click(event.pos)
            levels.on_click(event.pos)
    screen.fill("white")
    if flag:
        screen.fill("white")

        first = MainMenu("DATA/1.png", (50 + 100 * 1, 150), (75, 75))
        second = MainMenu("DATA/2.png", (50 + 100 * 2, 150), (75, 75))
        third = MainMenu("DATA/3.png", (50 + 100 * 3, 150), (75, 75))
        fourth = MainMenu("DATA/4.png", (50 + 100 * 4, 150), (75, 75))
        fifth = MainMenu("DATA/5.png", (50 + 100 * 5, 150), (75, 75))

        @first.add_function
        def _first():
            global data
            data = {
                "volume": data["volume"],
                "playerPicture": data["playerPicture"],
                "levelNum": 1
            }
            with open("config.json", "w") as file:
                json.dump(data, file)


        @second.add_function
        def _second():
            global data
            data = {
                "volume": data["volume"],
                "playerPicture": data["playerPicture"],
                "levelNum": 2
            }
            with open("config.json", "w") as file:
                json.dump(data, file)


        @third.add_function
        def _third():
            global data
            data = {
                "volume": data["volume"],
                "playerPicture": data["playerPicture"],
                "levelNum": 3
            }
            with open("config.json", "w") as file:
                json.dump(data, file)


        @fourth.add_function
        def _fourth():
            global data
            data = {
                "volume": data["volume"],
                "playerPicture": data["playerPicture"],
                "levelNum": 4
            }
            with open("config.json", "w") as file:
                json.dump(data, file)


        @fifth.add_function
        def _fifth():
            global data
            data = {
                "volume": data["volume"],
                "playerPicture": data["playerPicture"],
                "levelNum": 5
            }
            with open("config.json", "w") as file:
                json.dump(data, file)


        levels.add(first, second, third, fourth, fifth)
        levelSprites.add(first.button, second.button, third.button, fourth.button, fifth.button)
        levelSprites.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()
