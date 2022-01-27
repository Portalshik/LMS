import pygame
import os


class MainMenu:
    def __init__(self, name_of_file, coords=(0, 0)):
        self.button = pygame.sprite.Sprite()
        self.func = None
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
        print(args)
        for button in args:
            self.group[button] = [range(button.button.rect.x, button.button.rect.x + list(button.button.rect)[2]),
                                  range(button.button.rect.y, button.button.rect.y + list(button.button.rect)[3])]

    def on_click(self, mouse_pos):
        for i in self.group:
            if mouse_pos[0] in self.group[i][0] and mouse_pos[1] in self.group[i][1]:
                i.function()


running = True
size = (800, 700)
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
group = ButtonGroup()
play_button = MainMenu("DATA/play_button.png", (size[0] // 2, size[1] // 2))
settings = MainMenu("DATA/settings.png", (700, 10))


@play_button.add_function
def play():
    print("Game In Work")
    running = False
    os.system("python game.py")


@settings.add_function
def setting():
    os.system("python settings.py")


group.add(play_button, settings)
all_sprites.add(play_button.button, settings.button)
screen.fill((255, 255, 255))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            group.on_click(event.pos)
    all_sprites.draw(screen)
    pygame.display.flip()
