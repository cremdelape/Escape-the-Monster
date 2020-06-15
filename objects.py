import pygame
import math
from conf import *

vec = pygame.math.Vector2
center = vec(WIDTH // 2, HEIGHT // 2)


class Boat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load('ship.png')
        self.image_org = image
        self.image = self.image_org.copy()
        self.rect = self.image.get_rect()
        self.hitbox = self.image.get_rect()
        self.pos = vec(WIDTH // 2, HEIGHT // 2)
        self.vel = vec(0, 0)
        self.rot = 0

    def move(self, mouse_pos):
        if math.hypot((mouse_pos[0] - self.pos.x), (mouse_pos[1] - self.pos.y)) > 30:
            self.vel = vec(BOAT_SPEED, 0).rotate(-self.rot)
            self.pos += self.vel

    def update(self, mouse_pos):
        self.rot = (mouse_pos - self.pos).angle_to(vec(1, 0))
        self.image = self.image_org.copy()
        self.image = pygame.transform.rotate(self.image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hitbox.center = self.pos


class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load('monster.png')
        self.image_org = image
        self.image = self.image_org.copy()
        self.rect = self.image.get_rect()
        self.hitbox = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = 0
        self.ang = math.pi / 2
        self.rot = 0

    # Turn towards the boat
    def turn(self, pos):
        self.rot = (pos - self.pos).angle_to(vec(1, 0))
        self.image = self.image_org.copy()
        self.image = pygame.transform.rotate(self.image, self.rot)
        self.rect = self.image.get_rect()

    # Find the closest point to the enemy
    def locate(self, pos):
        target = (pos - center).angle_to(vec(1, 0))
        if target <= 0:
            target += 360
        target = math.radians(target)
        # print(angle, self.ang)
        if math.radians(5) < (target - self.ang + math.pi * 2) % (math.pi * 2) < math.pi:
            self.vel = MONSTER_SPEED / RADIUS
        elif math.pi * 2 - math.radians(5) > (target - self.ang + math.pi * 2) % (math.pi * 2) > math.pi:
            self.vel = -MONSTER_SPEED / RADIUS
        else:

            self.vel = 0

            # Move towards the target

    def move(self, pos):
        self.locate(pos)
        self.ang += self.vel
        self.pos.x = center.x + math.cos(self.ang) * RADIUS
        self.pos.y = center.y - math.sin(self.ang) * RADIUS

    def update(self, pos):
        self.turn(pos)
        self.move(pos)
        self.ang = self.ang % (2 * math.pi)
        self.rect.center = self.pos
        self.hitbox.center = self.pos

# class Monster(pygame.sprite.Sprite):
# def __init__(self):
#     super().__init__()
#     image = pygame.image.load('monster.png')
#     self.image_org = image
#     self.image = self.image_org.copy()
#     self.rect = self.image.get_rect()
#     self.pos = vec(WIDTH // 2, HEIGHT // 2 - RADIUS)
#     self.vel = 0
#     self.ang = 90
#     self.rot = 0
#
# # Turn towards the boat
# def turn(self, pos):
#     self.rot = (pos - self.pos).angle_to(vec(1, 0))
#     self.image = self.image_org.copy()
#     self.image = pygame.transform.rotate(self.image, self.rot)
#     self.rect = self.image.get_rect()
#
# # Find the closest point to the enemy
# def locate(self, pos):
#     target = (pos - center).angle_to(vec(1, 0))
#     if target <= 0:
#         target += 360
#     # print(angle, self.ang)
#     if MONSTER_SPEED < (target - self.ang + 360) % 360 < 180:
#         self.vel = MONSTER_SPEED
#     elif 360 - MONSTER_SPEED > (target - self.ang + 360) % 360 > 180:
#         self.vel = -MONSTER_SPEED
#     else:
#         self.vel = 0
#
# # Move towards the target
# def move(self, pos):
#     self.locate(pos)
#     self.ang += self.vel
#     self.pos.x = center.x + math.cos(math.radians(self.ang)) * RADIUS
#     self.pos.y = center.y - math.sin(math.radians(self.ang)) * RADIUS
#
# def update(self, pos):
#     self.turn(pos)
#     self.move(pos)
#     self.ang = self.ang % 360
#     self.rect.center = self.pos
