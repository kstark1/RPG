"""
Title: PyGame Template
Author: Kaitlyn Stark and Daniel Bentley
Date Created: 2019-04-08
"""

import pygame
pygame.init() # loads pygame module commands in the program

import math, random

class myClass:
    def __init__(self, x=0, y=0, colour = (255, 0, 0)):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.surface = pygame.Surface((0, 0), pygame.SRCALPHA, 32)
        self.colour = colour
    def set_surface(self, surface):
        self.surface = surface
    def get_surface(self):
        return self.surface
    def get_pos(self):
        return self.pos

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.surface.get_width()

    def get_height(self):
        return self.surface.get_height()

    def set_pos(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
    def changeAlpha(self, int):
        self.surface.set_alpha(int)
class rectangle(myClass): ## used for blackout
    def __init__(self, width, height, x = 0, y = 0, colour = (0,0,0)):
        myClass.__init__(self, x, y, colour)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.surface.fill(colour)
    def setColour(self, colour = (0,0,0)):
        self.surface.fill(colour)

class tile(myClass):
    def __init__(self,fileName, x = 0, y = 0, feature = 0):
        myClass.__init__(self, x, y, (0,0,0))
        self.surface = pygame.image.load("media/" + fileName)
        self.feature = feature
        self.fileName = fileName
    def set_feature(self, feature):
        self.feature = feature
    def get_feature(self):
        return self.feature
    def resetSurface(self):
        self.surface = pygame.image.load("media/" + self.fileName)

class entity(myClass):
    def __init__(self, fileName, x = 0, y = 0, hit = 25):
        myClass.__init__(self, x, y)

        self.surface = pygame.image.load("media/"+fileName)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.dim = (self.width, self.height)
        self.currentHP = 100
        self.maxHP = 100
        self.hitChance = hit

    def setHP(self):
        self.hp -= 10

    def getCurrentHP(self):
        return self.currentHP

    def setCurrentHP(self, var):
        self.currentHP += var

    def getMaxHP(self):
        return self.maxHP

    def getDamage(self):
        damage = random.randrange(0, 100)
        if damage <= self.hitChance:
            return -damage
        else:
            return 0

    def setHitChance(self, var):
        self.hitChance = var

    def check_enemy_pos(self, e_li, num): # checks if entity will overlap with eachother
        for i in range(len(e_li)):
            if self.x == e_li[i].get_x() and self.y == e_li[i].get_y() and i != num:
                return False
        return True

class enemy(entity):
    def __init__(self, fileName, x = 0, y= 0):
        entity.__init__(self, fileName, x, y)
        self.active = False

    def AI_move(self, player, e_li, num, map, spd = 50):
        if self.active == True:
            for i in range(len(map)):
                for j in range(len(map[i])):
                    if map[i][j].get_x() == self.get_x() and map[i][j].get_y() == self.get_y():
                        if player.get_x() >= self.x + self.get_width()  and map[i + 1][j].get_feature() != 'Wall': ## enemy cannot move onto wall
                            self.x += spd
                        elif player.get_x() <= self.x - self.get_width()  and map[i-1][j].get_feature() != 'Wall':
                            self.x -= spd
                        elif player.get_y() >= self.y + self.get_height()  and map[i][j+1].get_feature() != 'Wall':
                            self.y += spd
                        elif player.get_y() <= self.y -self.get_height()  and map[i][j-1].get_feature() != "Wall":
                            self.y -= spd
                        if (self.x != player.get_x() or self.y != player.get_y()) and self.check_enemy_pos(e_li, num): # if the player and enemy would be on the same spot or another enemy, the enemy does not move
                            self.set_pos(self.x, self.y)
                        else:
                            self.x = self.pos[0]
                            self.y = self.pos[1]
                        return


    def setActive(self, var):
        self.active = var

    def getActive(self):
        return self.active

class player(entity):
    def __init__(self, fileName, x, y, hit, level, xp, gold, potions):
        entity.__init__(self, fileName, x, y, hit)
        self.level = level
        self.xp = xp
        self.inventory = [gold,potions] #gold, healing potions

    def player_move(self, pressedKeys, e_li, map, spd):
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j].get_x() == self.get_x() and map[i][j].get_y() == self.get_y():
                    if pressedKeys[pygame.K_a] and map[i-1][j].get_feature() != 'Wall': ## checks if next tile if a wall
                        self.x -= spd
                    elif pressedKeys[pygame.K_d] and map[i+1][j].get_feature() != 'Wall':
                        self.x += spd
                    elif pressedKeys[pygame.K_w] and map[i][j-1].get_feature() != 'Wall':
                        self.y -= spd
                    elif pressedKeys[pygame.K_s] and map[i][j+1].get_feature() != 'Wall':
                        self.y += spd

                    if self.check_enemy_pos(e_li, -1): #player will not move onto enemy
                        self.pos = (self.x, self.y)
                    else:
                        self.x = self.pos[0] # resets x and y to original position
                        self.y = self.pos[1]
                    return


    def getLevel(self):
        return self.level

    def getXP(self):
        return self.xp

    def setXP(self, var):
        self.xp += var # if var is + the add. If var is - then subtract

    def setLevel(self, var):
        self.level += var
    def getLoot(self):
        self.inventory[0] += random.randrange(71)
        potions = random.randrange(-2, 3)
        if potions > 0:
            self.inventory[1]+=potions
    def setInventory(self, li):
        self.inventory = li
    def getInventory(self):
        return self.inventory
    def getHitChance(self):
        return self.hitChance
    def useItem(self, item = 1):
        if self.inventory[item] > 0:
            if item == 1 and self.currentHP < self.maxHP:
                self.inventory[item] -= 1
                self.currentHP +=50
                if self.currentHP > self.maxHP:
                    self.currentHP = self.maxHP

    def set_colour(self, colour):
        self.surface.fill(colour)
class text:
    def __init__(self, text, x = 0, y = 0):
        self.text = text
        self.colour = (255, 255, 255)
        self.size = 28
        self.x = x
        self.y = y
        self.pos = (self.x, self.y) #position of top left corner of text
        self.fontFam = 'Arial'
        self.font = pygame.font.SysFont(self.fontFam, self.size)
        self.surface = self.font.render(self.text, 1, self.colour)


    def get_text(self):
        return self.surface

    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, 1, self.colour)

    def get_pos(self):
        return self.pos

    def set_colour(self, colour):
        self.colour = colour
        self.surface = self.font.render(self.text, 1, self.colour)

    def set_size(self, size):
        self.size = size
        self.font = pygame.font.SysFont(self.fontFam, self.size)
        self.surface = self.font.render(self.text, 1, self.colour)

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
    def get_Y(self):
        return self.y
    def get_X(self):
        return self.x

    def get_height(self):
        return self.surface.get_height()
    def get_width(self):
        return self.surface.get_width()
    def changeAlpha(self, int):
        self.surface.set_alpha(int)
    def getContents(self):
        return self.text


def getCollision(p, e):
    if p.get_x() <= e.get_x() + e.get_width() <= p.get_x() + p.get_width() + e.get_width() and p.get_y() <= e.get_y() + e.get_height() <= p.get_y() + p.get_height() + e.get_height():
        if p.get_y() == e.get_y() or p.get_x() == e.get_x(): # only consider collisions with the faces of the sprites
            return True
        else:
            return False #return false if sprites collide with the corners
    else:
        return False

def getDistance(p, e):
    if math.fabs(p.get_x() - e.get_x()) < 160 and math.fabs(p.get_y() - e.get_y()) < 160: ## absoulte distance between objects
        e.setActive(True) # activates the enemy
    else:
        e.setActive(False)