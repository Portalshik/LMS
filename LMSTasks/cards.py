import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [["."] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 50
        self.all_sprites = pygame.sprite.Group()

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surface):
        for i in range(0, self.height):
            for j in range(0, self.width):

                temp = pygame.sprite.Sprite()
                if self.board[i][j] == ".":
                    temp.image = pygame.image.load("data/grass.png")
                if self.board[i][j] == "@":
                    temp.image = pygame.image.load("data/grass.png")
                if self.board[i][j] == "#":
                    temp.image = pygame.image.load("data/box.png")

                temp.rect = temp.image.get_rect()
                temp.rect.x = self.left + self.cell_size * i
                temp.rect.y = self.top + self.cell_size * j
                self.all_sprites.add(temp)
        self.all_sprites.draw(surface)

    def get_cell(self, pos):
        x = int(pos[0] // self.cell_size)
        y = int(pos[1] // self.cell_size)
        if x >= self.height or y >= self.width or x < 0 or y < 0:
            return False
        else:
            return self.cheakBox(x, y)

    def cheakBox(self, x, y):
        if self.board[x][y] == "#":
            return False
        return True


class Game:
    def __init__(self, filename, _screen):
        self.filename = filename
        self.map = None
        self.screen = _screen

    def load_level(self):
        filename = self.filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))

        self.__create(list(map(lambda x: x.ljust(max_width, '.'), level_map)))

    def __create(self, temp_map):
        self.map = Board(len(temp_map[0]), len(temp_map))
        self.map.board = temp_map
        self.map.render(self.screen)


class Fon:
    def __init__(self, file):
        self.group = pygame.sprite.Group()
        self.fon = pygame.sprite.Sprite()
        self.flag = True
        image = pygame.image.load(file)
        image = pygame.transform.scale(image, (550, 550))
        self.fon.image = image
        self.fon.rect = self.fon.image.get_rect()
        self.group.add(self.fon)

    def draw(self, _screen):
        self.group.draw(_screen)


class Player:
    def __init__(self, x, y):
        self.group = pygame.sprite.Group()
        self.player = pygame.sprite.Sprite()
        self.player.image = pygame.image.load("data/mar.png")
        self.player.rect = self.player.image.get_rect()
        self.player.rect.x = x + 13
        self.player.rect.y = y
        self.group.add(self.player)

    def draw(self):
        self.group.draw(screen)

    def moveX(self, x):
        self.player.rect.x += x
        self.draw()

    def moveY(self, y):
        self.player.rect.y += y
        self.draw()


running = True
size = (550, 550)
screen = pygame.display.set_mode(size)
game = Game("data/map.txt", screen)
fon = Fon("data/fon.jpg")
with open("data/map.txt", 'r') as mapFile:
    level_map = [line.strip() for line in mapFile]
temp = [(level_map.index(i), i.index("@")) for i in level_map if "@" in i]
x, y = temp[0][0] * 50, temp[0][1] * 50
player = Player(x, y)
moving = 50
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            fon.flag = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if game.map.get_cell((player.player.rect.x + moving, player.player.rect.y)):
                    player.moveX(moving)
            if event.key == pygame.K_LEFT:
                if game.map.get_cell((player.player.rect.x - moving, player.player.rect.y)):
                    player.moveX(-moving)
            if event.key == pygame.K_UP:
                if game.map.get_cell((player.player.rect.x, player.player.rect.y - moving)):
                    player.moveY(-moving)
            if event.key == pygame.K_DOWN:
                if game.map.get_cell((player.player.rect.x, player.player.rect.y + moving)):
                    player.moveY(+moving)
    screen.fill((0, 0, 0))
    game.load_level()
    player.draw()
    if fon.flag:
        fon.draw(screen)
    pygame.display.flip()
