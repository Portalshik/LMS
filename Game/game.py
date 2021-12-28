import pygame
import math
from cos import angles

size = (800, 800)
FPS = 120
running = True
screen = pygame.display.set_mode(size)
screen.fill("black")
x0, y0 = size[0] // 2, size[1] // 2
group = pygame.sprite.Group()
player = pygame.sprite.Sprite()
image = pygame.image.load("2143Transparent.png")
player.image = pygame.transform.scale(image, (100, 100))
player.rect = player.image.get_rect()
player.rect.x = x0 - 50
player.rect.y = y0 - 50
group.add(player)
clock = pygame.time.Clock()


def searchAngle(cos):
    temp = list(angles.values()).copy()
    temp.append(cos)
    temp.sort()
    return 180 - temp.index(cos) - 90


def surface(x, y):
    x1 = size[0] // 2
    y1 = size[1] // 2
    print(f"{x}: {x1}, {y}:{y1}")
    if x > x1 and y < y1:
        return 0
    elif x < x1 and y < y1:
        return 1
    elif x < x1 and y > y1:
        return 2
    elif x > x1 and y > y1:
        return 3
    else:
        return 0


def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


while running:
    image = pygame.image.load("2143Transparent.png")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            pygame.draw.line(screen, "white", (x0, y0), (x, y0), 1)  # a horisontal
            pygame.draw.line(screen, "white", (x0, y0), (x, y), 1)  # b angle
            pygame.draw.line(screen, "white", (x, y), (x, y0))  # c vertical
            screen.fill("black")

            a = round(math.sqrt((x - x0) ** 2 + (y0 - y0) ** 2))
            b = round(math.sqrt((x - x0) ** 2 + (y - y0) ** 2))
            c = round(math.sqrt((x - x) ** 2 + (y0 - y) ** 2))
            try:
                cosOfAngle = round((a ** 2 + b ** 2 - c ** 2) / (2 * a * b), 4)
            except ZeroDivisionError:
                cosOfAngle = 0
            print(rot_center(image, 90 - searchAngle(cosOfAngle) - 90, x0, y0))
            if surface(x, y) == 0:
                player.image = pygame.transform.scale(
                    rot_center(image, searchAngle(cosOfAngle), x0, y0)[0],
                    (100, 100))
            elif surface(x, y) == 1:
                player.image = pygame.transform.scale(
                    rot_center(image, 90 - searchAngle(cosOfAngle) + 90, x0, y0)[0],
                    (100, 100))
            elif surface(x, y) == 2:
                player.image = pygame.transform.scale(
                    rot_center(image, 90 + searchAngle(cosOfAngle) + 90, x0, y0)[0],
                    (100, 100))
            elif surface(x, y):
                player.image = pygame.transform.scale(
                    rot_center(image, 90 - searchAngle(cosOfAngle) - 90, x0, y0)[0],
                    (100, 100))
    group.draw(screen)
    pygame.display.flip()
    clock.tick(1000)
