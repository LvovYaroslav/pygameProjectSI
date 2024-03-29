import pygame
import random

pygame.init()


class enemy:
    def __init__(self, size, x, y, cost):
        self.size = size
        self.x = x
        self.y = y
        self.cost = cost

    def draw(self):
        pygame.draw.rect(game["screen"], (255, 255, 255), (self.x, self.y, self.size, self.size))

    def move(self):
        if self.x >= 770:
            game["movement"] = False
            game["descend"] = True
        elif self.x <= 30:
            game["movement"] = True
            game["descend"] = True

        if game["movement"]:
            self.x += 1
        else:
            self.x -= 1

        if game["descend"]:
            for row in game["enemies"]:
                for elem in row:
                    elem.y += 30
            game["descend"] = False

    def scoreup(self):
        game["score"] += self.cost


class bullet:
    def __init__(self, x, y, width, hight, color):
        self.x = x
        self.y = y
        self.width = width
        self.hight = hight
        self.color = color

    def check(self, object):
        if self.x + self.width >= object.x and self.x <= object.x + object.width and \
                self.y + self.hight >= object.y and self.y <= object.y + object.hight:
            return True
        else:
            return False

    def draw(self):
        pygame.draw.rect(game["screen"], self.color, (self.x, self.y, self.width, self.hight))


class herobullet(bullet):
    def move(self):
        self.y -= 30

    def checkenemy(self, object):
        if self.x + self.width >= object.x and self.x <= object.x + object.size and \
                self.y + self.hight >= object.y and self.y <= object.y + object.size:
            return True
        else:
            return False

    def deletus(self):
        for i in game["herobullet"]:
            if i.y <= 0:
                game["herobullet"].remove(i)


class enemybullet(bullet):
    def move(self):
        self.y += 20

    def checkhero(self, object):
        if self.x + self.width >= object[0] and self.x <= object[0] + object[2] and \
                self.y + self.hight >= object[1] and self.y <= object[1] + object[3]:
            return True
        else:
            return False


class block:
    def __init__(self, x, y, width, hight, durability):
        self.x = x
        self.y = y
        self.width = width
        self.hight = hight
        self.durability = durability

    def draw(self):
        for i in game["block"]:
            if i.durability == 4:
                pygame.draw.rect(game["screen"], (0, 255, 0), (i.x, i.y, i.width, i.hight))
            elif i.durability == 3:
                pygame.draw.rect(game["screen"], (255, 255, 0), (i.x, i.y, i.width, i.hight))
            elif i.durability == 2:
                pygame.draw.rect(game["screen"], (255, 165, 0), (i.x, i.y, i.width, i.hight))
            elif i.durability == 1:
                pygame.draw.rect(game["screen"], (255, 0, 0), (i.x, i.y, i.width, i.hight))
            else:
                game["block"].remove(i)


class button:
    def __init__(self, x, y, width, hight, active, text):
        self.x = x
        self.y = y
        self.width = width
        self.hight = hight
        self.active = active
        self.text = text

    def draw(self):
        if self.active:
            pygame.draw.rect(game["screen"], (50, 255, 50), (self.x, self.y, self.width, self.hight))
        else:
            pygame.draw.rect(game["screen"], (130, 130, 130), (self.x, self.y, self.width, self.hight))
        if self.y == 200:
            game["screen"].blit(
                pygame.font.Font(None, 50).render(
                    f"{self.text}", True, (0, 0, 0)), (360, 225))
        elif self.y == 400:
            game["screen"].blit(
                pygame.font.Font(None, 50).render(
                    f"{self.text}", True, (0, 0, 0)), (330, 425))
        elif self.y == 600:
            game["screen"].blit(
                pygame.font.Font(None, 50).render(
                    f"{self.text}", True, (0, 0, 0)), (360, 625))


    def press(self):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_s:
                    for j in range(2):
                        if game["button"][j].active:
                            game["button"][j].active = False
                            game["button"][j + 1].active = True
                            break

                if i.key == pygame.K_w:
                    for j in range(1, 3):
                        if game["button"][j].active:
                            game["button"][j].active = False
                            game["button"][j - 1].active = True
                            break

                for j in game["button"]:
                    if i.key == pygame.K_SPACE and j.active:
                        if j.y == 200:
                            gameloop()
                        elif j.y == 400:
                            if game["settings"] == 0:
                                game["settings"] = 1
                            else:
                                game["settings"] = 0
                        elif j.y == 600:
                            exit()


def buttoncreate():
    if len(game["button"]) == 0:
        game["button"].append(button(300, 200, 200, 90, True, "Start"))
        game["button"].append(button(300, 400, 200, 90, False, "Controls"))
        game["button"].append(button(300, 600, 200, 90, False, "Quit"))


def buttondraw():
    for i in game["button"]:
        i.draw()


def enemiescreate():
    for row in range(5):
        line = []
        for col in range(game["level"]):
            if row == 0:
                line.append(enemy(25, (770 - 40 * game["level"]) // 2 + 8 + 50 * col, 8 + 50 * row, 40))
            elif row == 1 or row == 2:
                line.append(enemy(32, (770 - 40 * game["level"]) // 2 + 4 + 50 * col, 4 + 50 * row, 20))
            else:
                line.append(enemy(40, (770 - 40 * game["level"]) // 2 + 50 * col, 50 * row, 10))
        game["enemies"].append(line)


def controls():
    game["coordsbase"] = list(game["coordsbase"])
    game["coordscannon"] = list(game["coordscannon"])
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                game["movehero"][2] = True
            if i.key == pygame.K_d:
                game["movehero"][1] = True
            elif i.key == pygame.K_a:
                game["movehero"][0] = True

        elif i.type == pygame.KEYUP:
            if i.key == pygame.K_SPACE:
                game["movehero"][2] = False
            if i.key == pygame.K_d:
                game["movehero"][1] = False
            elif i.key == pygame.K_a:
                game["movehero"][0] = False

    if game["movehero"][2] and len(game["herobullet"]) == 0:
        game["herobullet"].append(herobullet(game["coordscannon"][0] + 3, game["coordscannon"][1] - 15,
                                             4, 15, (0, 255, 0)))
    if game["coordsbase"][0] < 730 and game["movehero"][1]:
        game["coordsbase"][0] += 10
        game["coordscannon"][0] += 10
    if game["coordsbase"][0] > 20 and game["movehero"][0]:
        game["coordsbase"][0] -= 10
        game["coordscannon"][0] -= 10

    game["coordsbase"] = tuple(game["coordsbase"])
    game["coordscannon"] = tuple(game["coordscannon"])


def drawherobullet():
    for i in game["herobullet"]:
        i.draw()
        i.move()
        i.deletus()


def drawenemybullet():
    for i in game["enemybullet"]:
        i.draw()
        i.move()


def enemyshoot():
    for row in game["enemies"]:
        for elem in row:
            i = random.randrange(game["level"] * 90)
            if i == 0:
                if row == game["enemies"][0]:
                    game["enemybullet"].append(enemybullet(
                        elem.x + 13, elem.y + 15, 4, 15, (255, 255, 255)))
                elif row == game["enemies"][1] or row == game["enemies"][2]:
                    game["enemybullet"].append(enemybullet(
                        elem.x + 13, elem.y + 15, 4, 15, (255, 255, 255)))
                else:
                    game["enemybullet"].append(enemybullet(
                        elem.x + 13, elem.y + 15, 4, 15, (255, 255, 255)))


def moveenemies():
    for i in game["enemies"]:
        for j in i:
            j.move()


def drawcannon():
    pygame.draw.rect(game["screen"], (0, 255, 0), game["coordsbase"])
    pygame.draw.rect(game["screen"], (0, 255, 0), game["coordscannon"])


def blockcreate():
    for i in range(4):
        game["block"].append(block(25 * 3 + i * 180, 25 * 23, 25, 25, 4))
        game["block"].append(block(25 * 6 + i * 180, 25 * 23, 25, 25, 4))

        game["block"].append(block(25 * 3 + i * 180, 25 * 22, 25, 25, 4))
        game["block"].append(block(25 * 4 + i * 180, 25 * 22, 25, 25, 4))
        game["block"].append(block(25 * 5 + i * 180, 25 * 22, 25, 25, 4))
        game["block"].append(block(25 * 6 + i * 180, 25 * 22, 25, 25, 4))

        game["block"].append(block(25 * 3 + i * 180, 25 * 21, 25, 25, 4))
        game["block"].append(block(25 * 4 + i * 180, 25 * 21, 25, 25, 4))
        game["block"].append(block(25 * 5 + i * 180, 25 * 21, 25, 25, 4))
        game["block"].append(block(25 * 6 + i * 180, 25 * 21, 25, 25, 4))


def drawblock():
    for i in game["block"]:
        i.draw()


def blockupdate():
    for block in game["block"]:
        for bullet in game["herobullet"]:  # булет
            if bullet.check(block):
                block.durability -= 1
                game["herobullet"].remove(bullet)
        for bullet in game["enemybullet"]:
            if bullet.check(block):
                block.durability -= 1
                game["enemybullet"].remove(bullet)


def buttonpress():
    for i in game["button"]:
        i.press()


def drawenemies():
    for i in game["enemies"]:
        for j in i:
            j.draw()


def drawmenu():
    pygame.draw.rect(game["screen"], (0, 0, 0), (0, 745, 800, 100))
    pygame.draw.rect(game["screen"], (255, 255, 255), (0, 745, 800, 1))
    pygame.draw.rect(game["screen"], (255, 255, 255), (145, 745, 1, 60))
    pygame.draw.rect(game["screen"], (255, 255, 255), (575, 745, 1, 60))

    pygame.draw.rect(game["screen"], (0, 255, 0), (10, 777, 60, 10))
    pygame.draw.rect(game["screen"], (0, 255, 0), (35, 767, 10, 10))
    game["screen"].blit(pygame.font.Font(None, 50).render(
        f"x {game['lives']}", True, (255, 255, 255)), (80, 760))

    game["screen"].blit(pygame.font.Font(None, 50).render(
        f"score: {game['score']}", True, (255, 255, 255)), (600, 760))


def drawmainmenu():
    buttondraw()


def drawsettings():
    img = pygame.font.Font(None, 90).render('SPACE INVADERS', True, (0, 255, 0))
    if game["settings"] == 0:
        if game["controls"] == 0:
            text = "S, W - select, Space - choose"
        else:
            img = pygame.font.Font(None, 90).render('', True, (0, 255, 0))
            text = "A, D - move, Space - shoot"
    else:
        if game["controls"] == 1:
            img = pygame.font.Font(None, 90).render('', True, (0, 255, 0))
        text = ""
    game["screen"].blit(img, (140, 50))
    game["screen"].blit(pygame.font.Font(None, 45).render(
        f"{text}", True, (255, 255, 255)), (165, 765))


def createstars():
    for i in range(150):
        a = random.randrange(800)
        b = random.randrange(745)
        game["stars"].append([a, b])


def drawstars():
    for i in range(len(game["stars"])):
        pygame.draw.rect(game["screen"], (255, 255, 255),
                         (game["stars"][i][0], game["stars"][i][1], 1, 1))


def draweverything():
    game["screen"].fill((0, 0, 0))
    drawstars()
    drawcannon()
    drawenemies()
    drawenemybullet()
    drawherobullet()
    drawblock()
    drawmenu()


def gameloop():
    screen = game["screen"]
    pygame.display.set_caption("Space Invaders")
    pygame.time.Clock().tick(60)
    game["controls"] = 1
    blockcreate()
    count = 0
    createstars()
    while True:
        for row in game["enemies"]:
            for element in row:
                for i in game["herobullet"]:
                    if herobullet.checkenemy(i, element):
                        element.scoreup()
                        row.remove(element)
                        game["herobullet"].remove(i)

        for bul in game["enemybullet"]:
            if bul.checkhero(game["coordsbase"]):
                game["enemybullet"].remove(bul)
                game["lives"] -= 1
                if game["lives"] == 0:
                    quit()

        for i in game["enemies"]:
            count += len(i)
        if count == 0:
            game["level"] += 1
            enemiescreate()
        count = 0

        controls()
        moveenemies()
        enemyshoot()
        draweverything()
        blockupdate()
        drawsettings()
        pygame.display.update()
        pygame.time.delay(50)


def mainmenu():
    screen = game["screen"]
    pygame.display.set_caption("Space Invaders")
    pygame.time.Clock().tick(60)
    buttoncreate()

    while True:
        game["screen"].fill((0, 0, 0))
        buttondraw()
        buttonpress()
        drawsettings()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()

        pygame.display.update()
        pygame.time.delay(50)


game = {"screen": pygame.display.set_mode((810, 810)),
        "status": True,
        "coordsbase": (375, 705, 60, 10),
        "coordscannon": (400, 695, 10, 10),
        "movehero": [False, False, False],
        "enemies": [],
        "movement": True,
        "descend": False,
        "herobullet": [],
        "enemybullet": [],
        "block": [],
        "lives": 3,
        "level": 3,
        "score": 0,
        "button": [],
        "settings": 0,
        "controls": 0,
        "stars": []}

mainmenu()
