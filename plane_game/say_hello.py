# -*- coding: utf-8 -*-

import pygame
import random
from sys import exit

class Bullet:
    def __init__(self):
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('bullet.png').convert_alpha()
        # 默认不激活
        self.active = False

    def move(self):
        if self.active:
            self.y -= 60
        if self.y < 0:
            self.active = False

    def restart(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.image.get_width() / 2
        self.y = mouseY - self.image.get_height() / 2

        self.active = True

    # def move(self):
    #     if self.y < 0:
    #         mouseX, mouseY = pygame.mouse.get_pos()
    #         self.x = mouseX - self.image.get_width() / 2
    #         self.y = mouseY - self.image.get_height() / 2
    #     else:
    #         self.y -= 5


# bullet = pygame.image.load('bullet.png').convert_alpha()
# # 初始化子弹位置
# bullet_x = 0
# bullet_y = -1


class Enemy:
    #     让敌机的出现位置和速度有变化
    def restart(self):
        self.x = random.randint(50, 1280)
        self.y = random.randint(-200, -50)
        self.speed = random.random() + 5

    # 初始化
    def __init__(self):
        # self.x = 600
        # self.y = -50
        self.restart()
        self.image = pygame.image.load('enemyplane.png').convert_alpha()

    def move(self):
        if self.y < 674:
            # self.y += 10
            self.y += self.speed
        else:
            # self.y = -50
            self.restart()

class Plane:
    def restrat(self):
        self.x = 200
        self.y = 600

    def __init__(self):
        self.restrat()
        self.image = pygame.image.load('plane.png').convert_alpha()

    def move(self):
        x, y = pygame.mouse.get_pos()
        x -= self.image.get_width() / 2
        y -= self.image.get_height() / 2

        self.x = x
        self.y = y




def checkHit(enemy, bullet):
    if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width()) \
and (bullet.y > enemy.y and bullet.y < bullet.y + enemy.image.get_height()):
        enemy.restart()
        bullet = False
        return True
    return False


def checkCrash(enemy, plane):
    if (plane.x + 0.7 * plane.image.get_width() > enemy.x) \
        and (plane.x + 0.3 * plane.image.get_width() < enemy.x + enemy.image.get_width()) \
        and (plane.y + 0.7 * plane.image.get_height() > enemy.y) \
        and (plane.y + 0.3 * plane.image.get_width() < enemy.y + enemy.image.get_height()):
        return True
    return False


pygame.init()
screen = pygame.display.set_mode((1280, 674), 0,32)
pygame.display.set_caption("Hello! This is my game!")

# 加载图片
background = pygame.image.load('planebg.jpeg').convert()
# plane = pygame.image.load('plane.png').convert_alpha()

plane = Plane()

# bullet = Bullet()
bullets = []
for i in range(5):
    bullets.append(Bullet())

count_bullet = len(bullets)
index_bullet = 0
interval_bullet = 0


enemies = []
for i in range(5):
    enemies.append(Enemy())






# """
# 点击换图
# """
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             background = pygame.image.load('pygame_180.jpg').convert()
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()

# enemy = Enemy()








# 增加一架飞机，并且用鼠标来控制飞机的位置

# 主循环
gameover = False
score = 0
font = pygame.font.Font(None, 32)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gameover and event.type == pygame.MOUSEBUTTONUP:
            # 重置游戏
            plane.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active = False
            score = 0
            gameover = False
    screen.blit(background, (0, 0))

    if not gameover:
        interval_bullet -= 3
        if interval_bullet < 0:
            bullets[index_bullet].restart()

            interval_bullet = 1
            index_bullet = (index_bullet+1) % count_bullet

        for bullet in bullets:
            if bullet.active:
                for enemy in enemies:
                    if checkHit(enemy, bullet):
                        score += 100
                bullet.move()
                screen.blit(bullet.image, (bullet.x, bullet.y))
        for enemy in enemies:
            if checkCrash(enemy, plane):
                gameover = True
            enemy.move()
            screen.blit(enemy.image, (enemy.x, enemy.y))
        plane.move()
        screen.blit(plane.image, (plane.x, plane.y))

        text = font.render("Score: %d" % score, 1, (0, 0, 0))
        screen.blit(text, (0, 0))

    else:
        text = font.render("Score: %d" % score, 1, (0, 0, 0))
        screen.blit(text, (600, 200))
        pass






    # if bullet_y < 0:
    #     bullet_x = x - bullet.get_width()/2
    #     bullet_y = y - bullet.get_height()/2
    # else:
    #     bullet_y -= 10

    # bullet.move()
    # # screen.blit(bullet, (bullet_x, bullet_y))
    # screen.blit(bullet.image, (bullet.x, bullet.y))

    # enemy.move()
    # screen.blit(enemy.image, (enemy.x, enemy.y))



    # screen.blit(plane, (x, y))

    pygame.display.update()

