import pygame
import json

with open('config.json') as cat_file:
    data = json.load(cat_file)
volume = data["volume"]
playerPicture = data["playerPicture"]
selected = [True, playerPicture]

running = True
size = (500, 500)
FPS = 60
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
center = (volume * 400 + 50, size[1] // 2)
flag = False
tanks = pygame.sprite.Group()
basenn = pygame.sprite.Sprite(tanks)
btr = pygame.sprite.Sprite(tanks)
Pushka = pygame.sprite.Sprite(tanks)
basenn.image = pygame.image.load("DATA/bashenn_up.png")
btr.image = pygame.image.load("DATA/btr_up.png")
Pushka.image = pygame.image.load("DATA/Pushka_up.png")
basenn.rect = basenn.image.get_rect()
btr.rect = btr.image.get_rect()
Pushka.rect = Pushka.image.get_rect()
basenn.rect.x = 50
btr.rect.x = size[0] // 2 - 21
Pushka.rect.x = size[0] - 88
basenn.rect.y = 300
btr.rect.y = 300
Pushka.rect.y = 300
basennCoord = (range(basenn.rect.x, basenn.rect.x + 39), range(basenn.rect.y, basenn.rect.y + 63))
btrCoord = (range(btr.rect.x, btr.rect.x + 43), range(btr.rect.y, btr.rect.y + 57))
PushkaCoord = (range(Pushka.rect.x, Pushka.rect.x + 38), range(Pushka.rect.y, Pushka.rect.y + 62))
f1 = pygame.font.Font(None, 36)
text = f1.render(f"", True, "black")
if selected[0] and selected[1] == "bashenn":
    text = f1.render(f"Вы выбрали Т39!", True, "black")
    selected[0] = False
if selected[0] and selected[1] == "Pushka":
    text = f1.render(f"Вы выбрали Орту!", True, "black")
    selected[0] = False
if selected[0] and selected[1] == "btr":
    text = f1.render(f"Вы выбрали БТР!", True, "black")
    selected[0] = False


while running:
    screen.fill("white")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data = {
                "volume": volume,
                "playerPicture": playerPicture
            }
            with open("config.json", "w") as file:
                json.dump(data, file)
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag = True
            if event.pos[0] in basennCoord[0] and event.pos[1] in basennCoord[1]:
                f1 = pygame.font.Font(None, 36)
                text = f1.render(f"Вы выбрали Т39!", True, "black")
                playerPicture = "bashenn"
            if event.pos[0] in btrCoord[0] and event.pos[1] in btrCoord[1] or (selected[0] and selected[1] == "btr"):
                f1 = pygame.font.Font(None, 36)
                text = f1.render(f"Вы выбрали БТР!", True, "black")
                playerPicture = "btr"
            if event.pos[0] in PushkaCoord[0] and event.pos[1] in PushkaCoord[1] or (
                    selected[0] and selected[1] == "Pushka"):
                f1 = pygame.font.Font(None, 36)
                text = f1.render(f"Вы выбрали Орту!", True, "black")
                playerPicture = "Pushka"
        try:
            if flag:
                if size[0] - 50 >= event.pos[0] >= 50 and 280 >= event.pos[1] >= 230:
                    center = (event.pos[0], center[1])

                    pygame.display.update()
                    print((center[0] - 50) / 4)
        except AttributeError:
            pass
        if event.type == pygame.MOUSEBUTTONUP:
            flag = False
    tanks.draw(screen)
    f1 = pygame.font.Font(None, 36)
    text1 = f1.render(f"{(center[0] - 50) / 4}%", True, "black")
    volume = (center[0] - 50) / 400
    screen.blit(text1, (size[0] // 2 - 25, size[1] // 2 - 50))
    pygame.draw.line(screen, "black", (50, size[1] // 2), (size[1] - 50, size[1] // 2), 2)
    screen.blit(text, (size[0] // 2 - 100, 100))
    shaker = pygame.draw.circle(screen, "black", center, 7)
    pygame.display.flip()
    clock.tick(FPS)
