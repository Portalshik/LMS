import pygame
import json

with open('config.json') as cat_file:
    data = json.load(cat_file)

VOLUME = list(data.items())[0][1]
PLAYER_PICTURE = list(data.items())[1][1]


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 50
        self.all_sprites = pygame.sprite.Group()

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surface):
        for i in range(0, self.width):
            for j in range(0, self.height):
                temp = pygame.sprite.Sprite()
                if self.board[i][j] == ".":
                    temp.image = pygame.image.load("DATA/grass.png")
                if self.board[i][j] == "@":
                    temp.image = pygame.image.load("DATA/grass.png")
                if self.board[i][j] == "#":
                    temp.image = pygame.image.load("DATA/box.png")
                if self.board[i][j] == "*":
                    temp.image = pygame.image.load("DATA/grass.png")
                if self.board[i][j] == "+":
                    temp.image = pygame.image.load("DATA/grass.png")
                if self.board[i][j] == "-":
                    temp.image = pygame.image.load("DATA/grass.png")
                if self.board[i][j] == "/":
                    temp.image = pygame.image.load("DATA/grass.png")

                temp.image = pygame.transform.scale(temp.image, (50, 50))
                temp.rect = temp.image.get_rect()
                temp.rect.x = self.left + self.cell_size * j
                temp.rect.y = self.top + self.cell_size * i
                self.all_sprites.add(temp)
        self.all_sprites.draw(surface)

    def get_cell(self, pos: tuple, box=True, alive=False, special=False):
        x = int(pos[0] // self.cell_size)
        y = int(pos[1] // self.cell_size)
        if x >= self.height or y >= self.width or x < 0 or y < 0:
            return False
        else:
            if special:
                return x, y
            elif alive:
                return self.alive(x, y)
            elif box:
                return self.chekBox(x, y)

    def alive(self, x, y):
        if self.board[y][x] == "*" or self.board[y][x] == "+" or self.board[y][x] == "-" or self.board[y][x] == "/":
            with open('DATA/map.txt', 'r', encoding='utf-8') as mapFile:
                res = ""
                mp = mapFile.readlines()
                for i in range(len(mp)):
                    if i == y:
                        if self.board[y][x] == "*":
                            res += mp[y].replace("*", '.')
                        elif self.board[y][x] == "-":
                            res += mp[y].replace("-", '.')
                        elif self.board[y][x] == "+":
                            res += mp[y].replace("+", '.')
                        elif self.board[y][x] == "/":
                            res += mp[y].replace("/", '.')
                    else:
                        res += "".join(mp[i])
                with open("DATA/map.txt", "w", encoding="utf-8") as f:
                    f.write(res)
            self.render(screen)
            return True
        return False

    def chekBox(self, x, y):
        if self.board[y][x] == "#":
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
        size = list(map(lambda x: list(x.ljust(max_width, '.')), level_map))
        self.__create(size)
        return len(size[0]) * 50, len(size) * 50

    def __create(self, temp_map):
        self.map = Board(len(temp_map), len(temp_map[0]))
        self.map.board = temp_map
        self.map.render(self.screen)


class Fon:
    def __init__(self, file, coords: tuple):
        self.group = pygame.sprite.Group()
        self.fon = pygame.sprite.Sprite()
        self.flag = True
        image = pygame.image.load(file)
        image = pygame.transform.scale(image, coords)
        self.fon.image = image
        self.fon.rect = self.fon.image.get_rect()
        self.group.add(self.fon)

    def draw(self, _screen):
        self.group.draw(_screen)


class PersonObject:
    def __init__(self, x, y, obj, nameOfFile="DATA/box.png"):
        self.nameOfFile = nameOfFile
        self.group = pygame.sprite.Group()
        self.player = pygame.sprite.Sprite()
        self.flag = True
        self.obj = obj
        image = pygame.image.load(nameOfFile)
        image = pygame.transform.scale(image, (50, 50))
        self.player.image = image
        self.player.rect = self.player.image.get_rect()
        self.player.rect.x = x
        self.player.rect.y = y
        self.group.add(self.player)

    def changeImage(self, nameOfFile):
        self.nameOfFile = nameOfFile
        image = pygame.image.load(nameOfFile)
        image = pygame.transform.scale(image, (50, 50))
        self.player.image = image

    def dead(self):
        self.player.rect.x += 100
        self.obj.load_level()
        deaded.play()
        deaded.set_volume(VOLUME)
        self.changeImage("DATA/grass.png")
        self.draw()
        self.flag = False

    def draw(self):
        if self.flag:
            self.group.draw(screen)

    def moveX(self, x):
        self.player.rect.x += x
        self.draw()

    def moveY(self, y):
        self.player.rect.y += y
        self.draw()


class Player(PersonObject):
    def __init__(self, x, y, obj):
        super().__init__(x, y, obj, nameOfFile=f"DATA/{PLAYER_PICTURE}_right.png")


class Enemy(PersonObject):
    def __init__(self, x, y, obj, picture="up"):
        super().__init__(x, y, obj, nameOfFile=f"DATA/Enemy_{picture}.png")


class GroupOfCreatures:
    def __init__(self, creatures: list):
        self.creatures = creatures
        self.positions = []

    def add(self, obj):
        self.creatures.append(obj[0])
        self.positions.append(obj[1])

    def draw(self):
        for i in self.creatures:
            i.draw()

    def findX(self, x):
        x = int(x // 50)
        for i in self.positions:
            if i[0] == x:
                res = self.creatures[self.positions.index(i)]
                return res

    def findY(self, y):
        y = int(y // 50)
        for i in self.positions:
            if i[1] == y:
                res = self.creatures[self.positions.index(i)]
                return res


flag = True
flag1 = True
count = 0


class Strike:
    def __init__(self, coords: tuple, side="right"):
        self.x, self.y = coords
        self.side = side
        self.distance = 0
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites1 = pygame.sprite.Group()
        self.all_sprites2 = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite()
        self.sprite1 = pygame.sprite.Sprite()
        self.sprite2 = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load(f"DATA/roket_{self.side}.png")
        self.sprite1.image = pygame.image.load(f"DATA/roket_{self.side}_d.png")
        self.sprite2.image = pygame.image.load(f"DATA/roket_{self.side}_z.png")
        self.sprite.rect = self.sprite.image.get_rect(center=(self.x, self.y))
        self.sprite1.rect = self.sprite1.image.get_rect(center=(self.x, self.y))
        self.sprite2.rect = self.sprite2.image.get_rect(center=(self.x, self.y))
        self.all_sprites.add(self.sprite)
        self.all_sprites1.add(self.sprite1)
        self.all_sprites2.add(self.sprite2)

    def shoot(self, move, board: Game):
        global flag, flag1, count
        if self.distance >= 1000:
            flag1 = True
            return False

        if self.side == 'right':
            if flag1:
                self.sprite.rect.x += move
                self.sprite.rect.y = self.y + 10
                self.sprite1.rect.x += move
                self.sprite1.rect.y = self.y + 10
                self.sprite2.rect.x += move
                self.sprite2.rect.y = self.y + 10
                self.all_sprites2.draw(screen)
                count += 1
                if count == 5:
                    count = 0
                    flag1 = False
            else:
                if flag:
                    self.sprite.rect.x += move
                    self.sprite.rect.y = self.y + 10
                    self.sprite1.rect.x += move
                    self.sprite1.rect.y = self.y + 10
                    self.sprite2.rect.x += move
                    self.sprite2.rect.y = self.y + 10
                    self.all_sprites.draw(screen)
                    count += 1
                    if count == 2:
                        count = 0
                        flag = False
                else:
                    self.sprite1.rect.x += move
                    self.sprite1.rect.y = self.y + 10
                    self.sprite.rect.x += move
                    self.sprite.rect.y = self.y + 10
                    self.sprite2.rect.x += move
                    self.sprite2.rect.y = self.y + 10
                    self.all_sprites1.draw(screen)
                    count += 1
                    if count == 3:
                        count = 0
                        flag = True
        elif self.side == 'left':
            if flag1:
                self.sprite.rect.x -= move
                self.sprite.rect.y = self.y + 10
                self.sprite1.rect.x -= move
                self.sprite1.rect.y = self.y + 10
                self.sprite2.rect.x -= move
                self.sprite2.rect.y = self.y + 10
                self.all_sprites2.draw(screen)
                count += 1
                if count == 5:
                    count = 0
                    flag1 = False
            else:
                if flag:
                    self.sprite.rect.x -= move
                    self.sprite.rect.y = self.y + 10
                    self.sprite1.rect.x -= move
                    self.sprite1.rect.y = self.y + 10
                    self.sprite2.rect.x -= move
                    self.sprite2.rect.y = self.y + 10
                    self.all_sprites.draw(screen)
                    count += 1
                    if count == 2:
                        count = 0
                        flag = False
                else:
                    self.sprite1.rect.x -= move
                    self.sprite1.rect.y = self.y + 10
                    self.sprite.rect.x -= move
                    self.sprite.rect.y = self.y + 10
                    self.sprite2.rect.x -= move
                    self.sprite2.rect.y = self.y + 10
                    self.all_sprites1.draw(screen)
                    count += 1
                    if count == 3:
                        count = 0
                        flag = True
        elif self.side == 'up':
            if flag1:
                self.sprite.rect.x = self.x + 10
                self.sprite.rect.y -= move
                self.sprite1.rect.x = self.x + 10
                self.sprite1.rect.y -= move
                self.sprite2.rect.x = self.x + 10
                self.sprite2.rect.y -= move
                self.all_sprites2.draw(screen)
                count += 1
                if count == 5:
                    count = 0
                    flag1 = False
            else:
                if flag:
                    self.sprite.rect.x = self.x + 10
                    self.sprite.rect.y -= move
                    self.sprite1.rect.x = self.x + 10
                    self.sprite1.rect.y -= move
                    self.sprite2.rect.x = self.x + 10
                    self.sprite2.rect.y -= move
                    self.all_sprites.draw(screen)
                    count += 1
                    if count == 2:
                        count = 0
                        flag = False
                else:
                    self.sprite1.rect.x = self.x + 10
                    self.sprite1.rect.y -= move
                    self.sprite.rect.x = self.x + 10
                    self.sprite.rect.y -= move
                    self.sprite2.rect.x = self.x + 10
                    self.sprite2.rect.y -= move
                    self.all_sprites1.draw(screen)
                    count += 1
                    if count == 3:
                        count = 0
                        flag = True
        elif self.side == 'down':
            if flag1:
                self.sprite.rect.x = self.x + 10
                self.sprite.rect.y += move
                self.sprite1.rect.x = self.x + 10
                self.sprite1.rect.y += move
                self.sprite2.rect.x = self.x + 10
                self.sprite2.rect.y += move
                self.all_sprites2.draw(screen)
                count += 1
                if count == 5:
                    count = 0
                    flag1 = False
            else:
                if flag:
                    self.sprite.rect.x = self.x + 10
                    self.sprite.rect.y += move
                    self.sprite1.rect.x = self.x + 10
                    self.sprite1.rect.y += move
                    self.sprite2.rect.x = self.x + 10
                    self.sprite2.rect.y += move
                    self.all_sprites.draw(screen)
                    count += 1
                    if count == 2:
                        count = 0
                        flag = False
                else:
                    self.sprite1.rect.x = self.x + 10
                    self.sprite1.rect.y += move
                    self.sprite.rect.x = self.x + 10
                    self.sprite.rect.y += move
                    self.sprite2.rect.x = self.x + 10
                    self.sprite2.rect.y += move
                    self.all_sprites1.draw(screen)
                    count += 1
                    if count == 3:
                        count = 0
                        flag = True
        self.distance += move

        if board.map.get_cell((self.sprite.rect.x + 100, self.sprite.rect.y + 13), alive=True) and self.side == "right":
            try:
                enemies.findX(self.sprite.rect.x + 100).dead()
                enemies.findY(self.sprite.rect.y + 13).dead()
            except AttributeError:
                pass
            self.distance = 1000

        if board.map.get_cell((self.sprite.rect.x, self.sprite.rect.y + 13), alive=True) and self.side == "left":
            try:
                enemies.findX(self.sprite.rect.x).dead()
                enemies.findY(self.sprite.rect.y + 13).dead()
            except AttributeError:
                pass
            self.distance = 1000

        if board.map.get_cell((self.sprite.rect.x + 13, self.sprite.rect.y), alive=True) and self.side == "up":
            try:
                enemies.findX(self.sprite.rect.x + 13).dead()
                enemies.findY(self.sprite.rect.y).dead()
            except AttributeError:
                pass
            self.distance = 1000

        if board.map.get_cell((self.sprite.rect.x + 13, self.sprite.rect.y + 100), alive=True) and self.side == "down":
            try:
                enemies.findX(self.sprite.rect.x + 13).dead()
                enemies.findY(self.sprite.rect.x + 100).dead()
            except AttributeError:
                pass
            self.distance = 1000

        if not board.map.get_cell((self.sprite.rect.x + 116, self.sprite.rect.y + 13)) and self.side == "right":
            self.distance = 1000

        if not board.map.get_cell((self.sprite.rect.x - 16, self.sprite.rect.y + 13)) and self.side == "left":
            self.distance = 1000

        if not board.map.get_cell((self.sprite.rect.x + 13, self.sprite.rect.y - 16)) and self.side == "up":
            self.distance = 1000

        if not board.map.get_cell((self.sprite.rect.x + 13, self.sprite.rect.y + 100)) and self.side == "down":
            self.distance = 1000

        return True

    def draw(self, surface):
        global flag, flag1
        if flag1:
            self.all_sprites2.draw(surface)
        else:
            if flag:
                self.all_sprites.draw(surface)
            else:
                self.all_sprites1.draw(screen)


def allIndexes(data: list, elem):
    result = []
    for i in range(data.count(elem)):
        result.append(data.index(elem))
        data[data.index(elem)] = None
    return result


running = True
size = (700, 700)
FPS = 60
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
game = Game("DATA/map.txt", screen)
pygame.mixer.music.load('DATA/music_fon.wav')
shot = pygame.mixer.Sound('DATA/shot.wav')
deaded = pygame.mixer.Sound('DATA/dead.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(VOLUME)
size = game.load_level()
screen = pygame.display.set_mode(size)
strike = None
enemies = GroupOfCreatures([])
fon = Fon("DATA/fon.png", size)
with open("DATA/map.txt", 'r') as mapFile:
    level_map = [line.strip() for line in mapFile]
temp = [(level_map.index(i), i.index("@")) for i in level_map if "@" in i]
enemy = [(level_map.index(i), i.index("*")) for i in level_map if "*" in i]
x, y = temp[0][1] * 50, temp[0][0] * 50
player = Player(x, y, game)

for i in range("".join(level_map).count("*")):
    enemies.add([Enemy(enemy[i][1] * 50, enemy[i][0] * 50, game), enemy[i]])

enemy = [(level_map.index(i), i.index("+")) for i in level_map if "+" in i]
for i in range("".join(level_map).count("+")):
    enemies.add([Enemy(enemy[i][1] * 50, enemy[i][0] * 50, game, picture="right"), enemy[i]])

enemy = [(level_map.index(i), i.index("-")) for i in level_map if "-" in i]
for i in range("".join(level_map).count("-")):
    enemies.add([Enemy(enemy[i][1] * 50, enemy[i][0] * 50, game, picture="left"), enemy[i]])

enemy = [(level_map.index(i), i.index("/")) for i in level_map if "/" in i]
for i in range("".join(level_map).count("/")):
    enemies.add([Enemy(enemy[i][1] * 50, enemy[i][0] * 50, game, picture="down"), enemy[i]])

moving = 15
rightMove = False
leftMove = False
upMove = False
downMove = False
shoot = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot and not fon.flag:
                strike = Strike(
                    (player.player.rect.x, player.player.rect.y), player.nameOfFile.split("_")[-1][:-4])
                shot.play()
                shot.set_volume(0.2)
                shoot = True
            fon.flag = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.changeImage(f"DATA/{PLAYER_PICTURE}_right.png")
                rightMove = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.changeImage(f"DATA/{PLAYER_PICTURE}_left.png")
                leftMove = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.changeImage(f"DATA/{PLAYER_PICTURE}_up.png")
                upMove = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.changeImage(f"DATA/{PLAYER_PICTURE}_down.png")
                downMove = True
            if event.key == pygame.K_m:
                breakpoint()
                game.load_level()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                rightMove = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                leftMove = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                upMove = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                downMove = False

    if rightMove and game.map.get_cell(
            (player.player.rect.x + 49, player.player.rect.y)) and game.map.get_cell(
            (player.player.rect.x + 49, player.player.rect.y + 49)):
        player.moveX(moving)
    elif leftMove and game.map.get_cell(
            (player.player.rect.x, player.player.rect.y)) and game.map.get_cell(
            (player.player.rect.x, player.player.rect.y + 49)):
        player.moveX(-moving)
    elif upMove and game.map.get_cell(
            (player.player.rect.x, player.player.rect.y)) and game.map.get_cell(
            (player.player.rect.x + 49, player.player.rect.y)):
        player.moveY(-moving)
    elif downMove and game.map.get_cell(
            (player.player.rect.x, player.player.rect.y + 49)) and game.map.get_cell(
            (player.player.rect.x + 49, player.player.rect.y + 49)):
        player.moveY(+moving)

    screen.fill((0, 0, 0))
    game.load_level()
    player.draw()
    enemies.draw()
    if fon.flag:
        fon.draw(screen)
    if shoot:
        shoot = strike.shoot(40, game)
        strike.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
