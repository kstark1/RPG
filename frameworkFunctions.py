'''
Title: Framework Functions
Author: Daniel Bentley and Kaitlyn Stark
Date Created: 2019-06-03
'''
from entityConcepts import *
import pygame, time
pygame.init()
def getPlayerData(): #Creates a new player object if there is no file, otherwise pulls the data from that file
    try:
        fil = open("savedata.txt", "x")
        fil.close()
        return player("player.png", 0, 0, 80, 1, 0, 0, 2), 0
    except:
        fil = open("savedata.txt", "r")
        data = fil.read()
        fil.close()
        data = data.split(",")
        for i in range(len(data)):
            data[i] = int(data[i])
        return player("player.png", 0, 0, data[0], data[1], data[2], data[3], data[4]), data[5]
def savePlayerData(p, level): #Saves all needed player data to a file
    data = [p.getHitChance(), p.getLevel(), p.getXP(), p.getInventory()[0], p.getInventory()[1], level]
    for i in range(len(data)):
        data[i]=str(data[i])
    fil = open("savedata.txt", "w")
    fil.write(",".join(data))
    fil.close()
def addToScoreBoard(level, score): #For use at the end of the program only. Places the player score in a leaderboard, then displays the board, highlighting the player in green
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("SCOREBOARD")
    screen.fill((0,0,0))
    # - Unpack Data - #
    try:
        fil = open("scoreboard.txt", "x")
        fil.close()
        fil = open("scoreboard.txt", "w")
        data = []
        for i in range(10):
            data.append(["AAA", "0", "0"])
        fil.write("AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0")
        fil.close()
    except FileExistsError:
        fil=open("scoreboard.txt", "r")
        data = fil.read()
        data = data.split("|")
        for i in range(len(data)):
            data[i] = data[i].split(",")
    # - Add Score - #
    found = False
    place = "NONE"
    for i in range(len(data)-1):
        if score > int(data[i][2]) and not found:
            found = True
            place = i
    if found:
        data.pop()
        inputBox = text(">")
        instructions = text("Input Name (AAA) and press ENTER")
        instructions.set_pos(300-instructions.get_width()/2, 300-instructions.get_height())
        inputBox.set_pos(300-inputBox.get_width()/2, 300)
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if len(inputBox.getContents()) < 4 and (event.key == pygame.K_q or event.key == pygame.K_w or event.key == pygame.K_e or event.key == pygame.K_r or event.key == pygame.K_t or event.key == pygame.K_y or event.key == pygame.K_u or event.key == pygame.K_i or event.key == pygame.K_o or event.key == pygame.K_p or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d or event.key == pygame.K_f or event.key == pygame.K_g or event.key == pygame.K_h or event.key == pygame.K_j or event.key == pygame.K_k or event.key == pygame.K_l or event.key == pygame.K_z or event.key == pygame.K_x or event.key == pygame.K_c or event.key == pygame.K_v or event.key == pygame.K_b or event.key == pygame.K_n or event.key == pygame.K_m):
                        inputBox.set_text((inputBox.getContents()+event.unicode).upper())
                    elif event.key == pygame.K_RETURN and len(inputBox.getContents()) == 4:
                        exit = True
                    elif event.key == pygame.K_BACKSPACE:
                        inputBox.set_text(inputBox.getContents()[:-1])
            inputBox.set_pos(300 - inputBox.get_width() / 2, 300)
            screen.fill((0,0,0))
            screen.blit(inputBox.get_text(), inputBox.get_pos())
            screen.blit(instructions.get_text(), instructions.get_pos())
            pygame.display.flip()
        data.insert(place, [inputBox.getContents()[1:], str(level), str(score)])
        while len(data) > 10:
            data.pop()
    # - Ready Board Display - #
    nameColumn = [text("PLAYER")]
    nameColumn[0].set_pos(100-nameColumn[0].get_width()/2, 9)
    nameColumn[0].set_colour((255, 0, 0))
    levelColumn = [text("LEVEL")]
    levelColumn[0].set_pos(300 - levelColumn[0].get_width()/2, 9)
    levelColumn[0].set_colour((255, 0, 0))
    scoreColumn = [text("SCORE")]
    scoreColumn[0].set_pos(500 - scoreColumn[0].get_width()/2, 9)
    scoreColumn[0].set_colour((255, 0, 0))
    for i in range(len(data)):
        nameColumn.append(text(data[i][0]))
        nameColumn[i+1].set_pos(100-nameColumn[i+1].get_width()/2, nameColumn[i].get_Y()+nameColumn[i].get_height()+18)
        levelColumn.append(text(data[i][1]))
        levelColumn[i+1].set_pos(300-levelColumn[i+1].get_width()/2, levelColumn[i].get_Y() +levelColumn[i].get_height()+ 18)
        scoreColumn.append(text(data[i][2]))
        scoreColumn[i+1].set_pos(500-levelColumn[i+1].get_width()/2, scoreColumn[i].get_Y()+scoreColumn[i].get_height()+18)
        if i == place:
            nameColumn[i+1].set_colour((0, 255, 0))
            levelColumn[i+1].set_colour((0, 255, 0))
            scoreColumn[i+1].set_colour((0, 255, 0))
    instructions = text("You may close this window at any time")
    instructions.set_pos(300-instructions.get_width()/2, nameColumn[-1].get_Y()+nameColumn[-1].get_height()+18)
    # - Repack Data - #
    for i in range(len(data)):
        data[i] = ",".join(data[i])
    data = "|".join(data)
    fil = open("scoreboard.txt", "w")
    fil.write(str(data))
    fil.close()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                screen.fill((0,0,0))
                for i in range(len(nameColumn)):
                    screen.blit(nameColumn[i].get_text(), nameColumn[i].get_pos())
                    screen.blit(levelColumn[i].get_text(), levelColumn[i].get_pos())
                    screen.blit(scoreColumn[i].get_text(), scoreColumn[i].get_pos())
                screen.blit(instructions.get_text(), instructions.get_pos())
                pygame.display.flip()

def menu(menu_text, screen): #For choices
    choice = pygame.key.get_pressed()
    for i in range(len(menu_text)):
        screen.blit(menu_text[i].get_text(), menu_text[i].get_pos())
    return choice

def blackout_sub(WIDTH, HEIGHT, screen): #Subroutine for blackout as opposed to recoding
    fade = True
    while fade:
        blackout1 = rectangle(WIDTH, HEIGHT - 100)
        blackout1.changeAlpha(0)
        count = 0
        while count < 255:
            count += 51
            blackout1.setColour((0, 0, 0, count))
            screen.blit(blackout1.get_surface(), blackout1.get_pos())
            time.sleep(0.01)
            pygame.display.flip()
        fade = False
def viewScoreBoard(): #Displays scoreboard in new window, returns to game window when closed
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("SCOREBOARD")
    screen.fill((0, 0, 0))
    # - Unpack Data - #
    try:
        fil = open("scoreboard.txt", "x")
        fil.close()
        fil = open("scoreboard.txt", "w")
        data = []
        for i in range(10):
            data.append(["AAA", "0", "0"])
        fil.write("AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0|AAA,0,0")
        fil.close()
    except FileExistsError:
        fil = open("scoreboard.txt", "r")
        data = fil.read()
        data = data.split("|")
        for i in range(len(data)):
            data[i] = data[i].split(",")
        # - Ready Board Display - #
        nameColumn = [text("PLAYER")]
        nameColumn[0].set_pos(100 - nameColumn[0].get_width() / 2, 9)
        nameColumn[0].set_colour((255, 0, 0))
        levelColumn = [text("LEVEL")]
        levelColumn[0].set_pos(300 - levelColumn[0].get_width() / 2, 9)
        levelColumn[0].set_colour((255, 0, 0))
        scoreColumn = [text("SCORE")]
        scoreColumn[0].set_pos(500 - scoreColumn[0].get_width() / 2, 9)
        scoreColumn[0].set_colour((255, 0, 0))
        for i in range(len(data)):
            nameColumn.append(text(data[i][0]))
            nameColumn[i + 1].set_pos(100 - nameColumn[i + 1].get_width() / 2,nameColumn[i].get_Y() + nameColumn[i].get_height() + 18)
            levelColumn.append(text(data[i][1]))
            levelColumn[i + 1].set_pos(300 - levelColumn[i + 1].get_width() / 2,levelColumn[i].get_Y() + levelColumn[i].get_height() + 18)
            scoreColumn.append(text(data[i][2]))
            scoreColumn[i + 1].set_pos(500 - levelColumn[i + 1].get_width() / 2,scoreColumn[i].get_Y() + scoreColumn[i].get_height() + 18)
        instructions = text("Close this window to return to menu")
        instructions.set_pos(300 - instructions.get_width() / 2,nameColumn[-1].get_Y() + nameColumn[-1].get_height() + 18)
    view = True
    while view:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                view = False
                return False
        screen.fill((0,0,0))
        for i in range(len(nameColumn)):
            screen.blit(nameColumn[i].get_text(), nameColumn[i].get_pos())
            screen.blit(levelColumn[i].get_text(), levelColumn[i].get_pos())
            screen.blit(scoreColumn[i].get_text(), scoreColumn[i].get_pos())
        screen.blit(instructions.get_text(), instructions.get_pos())
        pygame.display.flip()
    #Reset Window
    TITLE = "Dungeon of RPGing"
    tileSize = 32
    WIDTH = (25 * tileSize)
    HEIGHT = WIDTH + 100
    SCREENDIM = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(SCREENDIM)
    pygame.display.set_caption(TITLE)