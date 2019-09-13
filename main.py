'''
Title: PyGame Template
Author: Daniel Bentley and Kaitlyn Stark
Date Created: 2019-04-08
'''
import pygame, time, os
from LevelGenConcept import *
from entityConcepts import *
from frameworkFunctions import *
pygame.init() # Loads the pygame module commands into the program

# Display Variables
TITLE = "Dungeon of RPGing" # Window title
tileSize =32
FPS = 15
WIDTH = (25*tileSize)
HEIGHT = WIDTH+100
SCREENDIM = (WIDTH, HEIGHT)

# Colour Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (75, 75, 75)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Creating the Window

screen = pygame.display.set_mode(SCREENDIM) #Creates the main surface where all other assets are placed on top
pygame.display.set_caption(TITLE) #Sets the window title
screen.fill(BLACK) #fills the surface with the colour. Erase/Clear
clock = pygame.time.Clock() #Starts a clock object to measure time
### --- CODE STARTS HERE --- ###
run = True
map = []
level = 1
enemy_li = []
playerObj, level = getPlayerData() #DEV
savePlayerData(playerObj, level)

## Text for player stats
player_stats = [text('HP: '+str(playerObj.getCurrentHP())), text("Gold: "+str(playerObj.getInventory()[0])), text("Healing Potions: "+str(playerObj.getInventory()[1])),  text('XP: '+str(playerObj.getXP()))]
player_stats[0].set_pos(0, HEIGHT - 2*player_stats[0].get_height())
player_stats[1].set_pos(player_stats[0].get_width()+player_stats[0].get_pos()[0]+10, HEIGHT - 2*player_stats[1].get_height())
player_stats[2].set_pos(player_stats[1].get_width()+player_stats[1].get_pos()[0]+10, HEIGHT - 2*player_stats[2].get_height())
player_stats[3].set_pos(player_stats[2].get_width()+player_stats[2].get_pos()[0]+10, HEIGHT - 2*player_stats[3].get_height())
blackout2 = 0

# text for intro
intro_text = [text('Dungeons of RPGing'), text('Press ENTER to continue')]
intro_text[0].set_colour(RED)
intro_text[0].set_size(50)
intro_text[0].set_pos(WIDTH//2 - intro_text[0].get_width()//2, HEIGHT//2 - intro_text[0].get_height()//2)
intro_text[1].set_pos(WIDTH//2 - intro_text[1].get_width()//2, HEIGHT - intro_text[1].get_height() - 100)

# Text for menu
menu_text = [text('Menu'), text('1. View Instructions'), text('2. View Highscores'), text('3. Start New Game'),  text('4. Load Game')]
menu_text[0].set_colour(RED)
for i in range(len(menu_text)):
    menu_text[i].set_size(40)

menu_text[0].set_pos(WIDTH//2 - menu_text[0].get_width()//2, 300)
for i in range(1, 5):
    menu_text[i].set_pos(250, menu_text[i-1].get_Y() + menu_text[i-1].get_height() + 20)

## Text for instructions
inst_text = [text('Instructions for play') ,text("Use 'W', 'A', 'S', 'D' to move"), text("Use 'SPACE' to attack enemies"),
text("Use 'H' to use healing potion"), text('Your progress is automatically saved after each level'), text('Press ENTER to return to menu')]
inst_text[0].set_colour(RED)
for i in range(len(inst_text)):
    inst_text[i].set_size(30)

inst_text[0].set_pos(WIDTH //2 - inst_text[0].get_width() //2, 300)
for i in range(1, 6):
    inst_text[i].set_pos(WIDTH // 2 - inst_text[i].get_width() // 2, inst_text[i-1].get_Y() + inst_text[i-1].get_height() + 20)


start = False
fade = True
intro = True
menu_var = True

while run:
    pressedKeys = pygame.key.get_pressed()
    for event in pygame.event.get(): # Returns all inputs and triggers into an array
        if event.type == pygame.QUIT: # if the window X is pressed
            run = False

    if start == False:
        if intro:
            screen.blit(intro_text[0].get_text(), intro_text[0].get_pos())
            screen.blit(intro_text[1].get_text(), intro_text[1].get_pos())

            if pressedKeys[pygame.K_RETURN]:
                blackout_sub(WIDTH, HEIGHT, screen)
                if level == 0: ## cannot load game if no data is saved
                    menu_text.pop()
                intro = False
        else:
            if menu_var:
                choice = menu(menu_text, screen)
                if choice[pygame.K_1] or choice[pygame.K_2] or choice[pygame.K_3] or (choice[pygame.K_4] and level != 0):
                    blackout_sub(WIDTH, HEIGHT, screen)
                    menu_var = False
            else:
                if choice[pygame.K_1]: ## View Instructions
                    for i in range(len(inst_text)):
                        screen.blit(inst_text[i].get_text(), inst_text[i].get_pos())
                    return_keys = pygame.key.get_pressed()
                    if return_keys[pygame.K_RETURN]:
                        blackout_sub(WIDTH, HEIGHT, screen)
                        menu_var = True
                elif choice[pygame.K_2]: # View High Score
                    if viewScoreBoard() == False:
                        screen = pygame.display.set_mode(SCREENDIM)
                        pygame.display.set_caption(TITLE)
                        #screen.fill(BLACK)  # fills the surface with the colour. Erase/Clear
                        menu_var = True
                elif choice[pygame.K_3]:
                    os.remove('savedata.txt')
                    playerObj, level = getPlayerData()
                    level = 0
                    start = True
                elif choice[pygame.K_4]: # Start New/Load Game
                    start = True

    else:
        if len(map) != 0: #Prevents errors in first iteration
            if map[int(playerObj.get_pos()[0] / tileSize)][int(playerObj.get_pos()[1] / tileSize)].get_feature() == "Down":
                map = []
                level +=1
        if len(map) == 0: #Creating a new level
            savePlayerData(playerObj, level)
            check = True
            blackout2 = rectangle(WIDTH, HEIGHT - 100)
            levelTxt = text("LEVEL " + str(level + 1))
            levelTxt.set_pos(WIDTH / 2 - levelTxt.get_width() / 2, (HEIGHT - 100) / 2 + levelTxt.get_height() / 2)
            blackout2.changeAlpha(0)
            levelTxt.changeAlpha(0)
            levelTxt.set_colour(RED)
            count = 0
            while count < 255:
                count += 1
                blackout2.setColour((0, 0, 0, count))
                levelTxt.set_colour((255, 0, 0, count))
                screen.blit(blackout2.get_surface(), blackout2.get_pos())
                screen.blit(levelTxt.get_text(), levelTxt.get_pos())
                time.sleep(0.01)
                pygame.display.flip()
            while check:
                try:
                    map = placeTunnels(placeRooms())
                    check = False
                except RecursionError:
                    pass
            enemies = populateLevel(map, level)
            enemy_li = [] # deletes all enemies from previous level
            for i in range(len(map)):
                for j in range(len(map[i])):
                    #Convert map into simple notation
                    if map[i][j] == "T":
                        map[i][j] ="F"
                    if isinstance(map[i][j], int) or map[i][j] == "C":
                        map[i][j] = 0
                    if map[i][j] == "F":
                        map[i][j] = tile("floor.png", i*tileSize, j*tileSize)
                    elif map[i][j] == "D":
                        map[i][j] = tile("down.png",i * tileSize, j * tileSize, "Down")
                    elif map[i][j] == "U":
                        map[i][j] = tile("floor.png", i * tileSize, j * tileSize, "Up")
                        playerObj.set_pos(i*tileSize, j*tileSize)
                    else:
                        map[i][j] = tile("bricks.png", i * tileSize, j * tileSize, "Wall")
            for i in range(len(enemies)):
                for j in range(len(enemies[i])):
                    if enemies [i][j] =="L":
                        map[i][j].set_feature("Loot")
                        map[i][j].get_surface().blit(pygame.image.load("media/loot.png"), (0,0))
                    elif enemies[i][j] == '!':
                        enemy_li.append(enemy("enemy.png", i*tileSize, j*tileSize))
            fogOfWar = createFOW(map, tileSize)
        ###################### Moving and Items
        fogOfWar = checkFogOfWar(playerObj.get_pos(), fogOfWar, tileSize, map)
        for i in range(len(enemy_li)):
            getDistance(playerObj, enemy_li[i])
        playerObj.player_move(pressedKeys, enemy_li, map, tileSize)
        if pressedKeys[pygame.K_a] or pressedKeys[pygame.K_s] or pressedKeys[pygame.K_d] or pressedKeys[pygame.K_w]:
            for i in range(len(enemy_li)):
                enemy_li[i].AI_move(playerObj, enemy_li, i, map, tileSize)
        elif pressedKeys[pygame.K_h]:
            for i in range(len(enemy_li)):
                enemy_li[i].AI_move(playerObj, enemy_li, i, map, tileSize)
            playerObj.useItem(1)
        if map[int(playerObj.get_pos()[0]/tileSize)][int(playerObj.get_pos()[1]/tileSize)].get_feature() == "Loot":
            map[int(playerObj.get_pos()[0] / tileSize)][int(playerObj.get_pos()[1] / tileSize)].set_feature(0)
            map[int(playerObj.get_pos()[0] / tileSize)][int(playerObj.get_pos()[1] / tileSize)].resetSurface()
            playerObj.getLoot()

        ######################## Attacking
        for i in range(len(enemy_li)):
            if getCollision(playerObj, enemy_li[i]):
                if pressedKeys[pygame.K_a] or pressedKeys[pygame.K_s] or pressedKeys[pygame.K_d] or pressedKeys[pygame.K_w] or pressedKeys[pygame.K_SPACE] or pressedKeys[pygame.K_h]:
                    playerObj.setCurrentHP(enemy_li[i].getDamage())
                if pressedKeys[pygame.K_SPACE]:
                    enemy_li[i].setCurrentHP(playerObj.getDamage())
        toPop = []
        for i in range(len(enemy_li)):
            if enemy_li[i].getCurrentHP() <= 0:
                toPop.append(i)
                playerObj.setXP(20)
        toPop.sort(reverse = True)
        for i in range(len(toPop)):
            enemy_li.pop(toPop[i])
        ### --- OUTPUTS --- ###
        if playerObj.getCurrentHP() >=0:
            player_stats[0].set_text('HP: ' + str(playerObj.getCurrentHP()))
        else:
            player_stats[0].set_text('HP: 0') # ensures that screen does not display -hp
        player_stats[1].set_text("Gold: "+str(playerObj.getInventory()[0]))
        player_stats[2].set_text("Healing Potions: "+str(playerObj.getInventory()[1]))
        player_stats[3].set_text('XP: '+str(playerObj.getXP()))
        player_stats[1].set_pos(player_stats[0].get_width() + player_stats[0].get_pos()[0] + 10,HEIGHT - 2 * player_stats[1].get_height())
        player_stats[2].set_pos(player_stats[1].get_width() + player_stats[1].get_pos()[0] + 10,HEIGHT - 2 * player_stats[2].get_height())
        player_stats[3].set_pos(player_stats[2].get_width() + player_stats[2].get_pos()[0] + 10, HEIGHT - 2*player_stats[3].get_height())
        screen.fill(BLACK)
        ## Blitting
        for i in range(len(map)):
            for j in range(len(map[i])):
                screen.blit(map[i][j].get_surface(), map[i][j].get_pos())
        for i in range(len(enemy_li)):
            screen.blit(enemy_li[i].get_surface(), enemy_li[i].get_pos())
        for i in range(len(fogOfWar)):
            for j in range(len(fogOfWar[i])):
                if fogOfWar[i][j] != 0:
                    screen.blit(fogOfWar[i][j].get_surface(), fogOfWar[i][j].get_pos())
        screen.blit(playerObj.get_surface(), playerObj.get_pos())
        for i in range(len(player_stats)):
            screen.blit(player_stats[i].get_text(), player_stats[i].get_pos())

        if playerObj.getCurrentHP() <= 0: # player if defeated
            os.remove("savedata.txt")
            run = False
            blackout2 = rectangle(WIDTH, HEIGHT - 100)
            levelTxt = text("YOU DIED")
            scoreTxt = text("FINAL SCORE: "+str(playerObj.getXP()+playerObj.getInventory()[0]))
            levelTxt.set_pos(WIDTH / 2 - levelTxt.get_width() / 2, (HEIGHT - 100) / 2 - (levelTxt.get_height()+scoreTxt.get_height()) / 2)
            scoreTxt.set_pos(WIDTH / 2 - scoreTxt.get_width() / 2, (HEIGHT - 100) / 2 + (levelTxt.get_height()+scoreTxt.get_height()) / 2)
            blackout2.changeAlpha(0)
            levelTxt.changeAlpha(0)
            levelTxt.set_colour(RED)
            count = 0
            while count < 255:
                count += 1
                blackout2.setColour((0, 0, 0, count))
                levelTxt.set_colour((255, 0, 0, count))
                scoreTxt.set_colour((255, 0, 0, count))
                screen.blit(blackout2.get_surface(), blackout2.get_pos())
                screen.blit(levelTxt.get_text(), levelTxt.get_pos())
                screen.blit(scoreTxt.get_text(), scoreTxt.get_pos())
                time.sleep(0.01)
                pygame.display.flip()
            addToScoreBoard(level + 1, playerObj.getInventory()[0] + playerObj.getXP())
    clock.tick(FPS) #Pause game until the FPS time is reached
    pygame.display.flip() #Like sync() is AGK, updates the screen
pygame.quit()