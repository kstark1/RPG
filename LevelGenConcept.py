'''
Title: Level Generator
Author: Daniel Bentley and Kaitlyn Stark
Date Created: 2019-05-14
'''
import random
from entityConcepts import *
class room:
    def __init__(self, dim, coords = (0, 0)):
        self.dim = (dim, dim)
        self.pos = coords
        self.connected = False
    def getDIM(self):
        return self.dim
    def getPOS(self):
        return self.pos
    def getAllTiles(self):
        output = []
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                output.append((self.pos[0]+i, self.pos[1]+j))
        return output
    def connect(self):
        self.connected = True
    def getConnect(self):
        return self.connected
    def getX(self):
        return self.pos[0]
    def getY(self):
        return self.pos[1]
    def getWidth(self):
        return self.dim[0]
    def getHeight(self):
        return self.dim[1]

def placeRooms():
    map = []
    mapSize = 25
    for i in range(mapSize):
        map.append([])
        for j in range(mapSize):
            map[i].append(0)
    roomCount = random.randrange(5, 8)
    rooms = []
    for i in range(roomCount):
        dim = random.randrange(5, 8)
        rooms.append(room(dim , (random.randrange(len(map)-dim), random.randrange(len(map)-dim))))
        tiles = rooms[i].getAllTiles()
        for j in range(len(tiles)):
            if map[tiles[j][1]][tiles[j][0]] != 0: #If the new room would replace a non-empty tile, recur
                return placeRooms()
            elif tiles[j][0] == rooms[i].getX() and tiles[j][1]==rooms[i].getY() or tiles[j][0] == rooms[i].getX()+rooms[i].getWidth()-1 and tiles[j][1]==rooms[i].getY() or tiles[j][0] == rooms[i].getX() and tiles[j][1]==rooms[i].getY()+rooms[i].getHeight()-1or tiles[j][0] == rooms[i].getX()+rooms[i].getWidth()-1 and tiles[j][1]==rooms[i].getY()+rooms[i].getHeight()-1:
                map[tiles[j][1]][tiles[j][0]] = "C"
            elif tiles[j][0] == rooms[i].getX() or tiles[j][0] == rooms[i].getX()+rooms[i].getWidth()-1 or tiles[j][1] == rooms[i].getY() or tiles[j][1] == rooms[i].getY()+rooms[i].getHeight()-1:
                map[tiles[j][1]][tiles[j][0]] = i+1
            else:
                map[tiles[j][1]][tiles[j][0]] = "F"
    return (map, rooms)

def placeTunnels(data):
    map = data[0]
    rooms = data[1]
    startCorner = random.randrange(4) # 0 = Northwest(start east), 1 = Northeast(start south), 2 = Southeast (start west), 3 = Southwest (Start north)
    if startCorner == 0:
        corner = (0, 0)
    elif startCorner == 1:
        corner = (0, len(map)-1)
    elif startCorner == 2:
        corner = (len(map)-1, len(map)-1)
    else:
        corner = (len(map)-1, 0)
    # Find room closest to chosen corner
    closest = (-1, 100) #Room index, distance
    for i in range(len(rooms)):
        if startCorner == 0:
            distance = sum(rooms[i].getPOS())
        elif startCorner == 1:
            distance = rooms[i].getX()+(len(map)-rooms[i].getY()-rooms[i].getHeight())
        elif startCorner == 2:
            distance = (len(map)-rooms[i].getY()-rooms[i].getHeight())+(len(map)-rooms[i].getX()-rooms[i].getWidth())
        else:
            distance = (len(map)-rooms[i].getX()-rooms[i].getWidth())+rooms[i].getY()
        if distance < closest[1]:
            closest = (i, distance)
    current = closest[0]
    rooms[current].connect()
    stairPos = (random.randrange(rooms[current].getWidth()-4), random.randrange(rooms[current].getHeight()-4))
    map[stairPos[1]+rooms[current].getY()+2][stairPos[0]+rooms[current].getX()+2] = "U"
    for roomCount in range(len(rooms) - 1):
        roomFound = False
        stop = False
        dirLooped = False
        dir = startCorner
        # This Tuple stores the maximum values in each direction that a tunnel could go
        limit = (len(map) + 1 - rooms[current].getX() - rooms[current].getWidth(),len(map) + 1 - rooms[current].getY() - 1 - rooms[current].getHeight(), rooms[current].getX() + 1,rooms[current].getY() + 1)
        sideOffset = random.randrange(rooms[current].getWidth() - 2)  # Determines which segment of the wall to start on
        while not dirLooped and not roomFound:
            for i in range(rooms[current].getWidth() - 2):  # Tile on this side of the room
                distances = []
                for x in range(limit[dir]):
                    distances.append(x)
                random.shuffle(distances) #this takes all the possible values that the length of the tunnel can be reduced by, and randomizes them
                if not roomFound:
                    tunnelTiles = []
                    i += sideOffset
                    if i >= rooms[current].getWidth() - 2:
                        i -= rooms[current].getWidth() - 2
                    for p in range(limit[dir]):  # Distance to remove from the max
                        p = distances[p]
                        if not roomFound:
                            stop = False
                            tunnelTiles = []
                        for l in range(limit[dir] - p):  # Distance in indicated direction
                            if not stop:
                                # Add a tile to the end of a tunnel
                                if dir == 0:
                                    tunnelTiles.append((rooms[current].getX() + rooms[current].getWidth() - 1 + l,rooms[current].getY() + 1 + i))
                                elif dir == 1:
                                    tunnelTiles.append((rooms[current].getX() + 1 + i,rooms[current].getY() + rooms[current].getHeight() - 1 + l))
                                elif dir == 2:
                                    tunnelTiles.append((rooms[current].getX() - l, rooms[current].getY() + 1 + i))
                                else:
                                    tunnelTiles.append((rooms[current].getX() + 1 + i, rooms[current].getY() - l))
                                try: #Checks if the tunnel is off the map
                                    currentTile = map[tunnelTiles[-1][1]][tunnelTiles[-1][0]]
                                except IndexError:
                                    tunnelTiles.pop()
                                if map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] == "C":
                                    stop = True
                                elif map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] == "F" or map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] == "U" or map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] == "D" or map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] == "T":
                                    pass  # Exists to remove all strings from next checks to prevent typeError
                                elif not rooms[map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] - 1].getConnect() and isinstance(map[tunnelTiles[-1][1]][tunnelTiles[-1][0]], int) and map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] != 0 and map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] != current + 1:
                                    rooms[map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] - 1].connect()
                                    stop = True
                                    roomFound = True
                                elif rooms[map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] - 1].getConnect() and map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] != 0 and map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] != current + 1:
                                    stop = True
                        straightLength = len(tunnelTiles)
                        for l in range(limit[(dir + 1) % 4]):  # Turn tunnel Right
                            if not stop:
                                if dir == 0:
                                    tunnelTiles.append((tunnelTiles[-1][0], tunnelTiles[-1][1] + 1))
                                elif dir == 1:
                                    tunnelTiles.append((tunnelTiles[-1][0] - 1, tunnelTiles[-1][1]))
                                elif dir == 2:
                                    tunnelTiles.append((tunnelTiles[-1][0], tunnelTiles[-1][1] - 1))
                                else:
                                    tunnelTiles.append((tunnelTiles[-1][0] + 1, tunnelTiles[-1][1]))
                                try:
                                    currentTile = map[tunnelTiles[-1][1]][tunnelTiles[-1][0]]
                                except IndexError:
                                    tunnelTiles.pop()
                                    currentTile = map[tunnelTiles[-1][1]][tunnelTiles[-1][0]]
                                if map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] == "C":
                                    stop = True
                                elif map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] == "F" or map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] == "U" or map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] == "D" or map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] == "T":
                                    pass  # Exists to remove all strings from next checks to prevent typeError
                                elif not rooms[
                                    map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] - 1].getConnect() and isinstance(map[tunnelTiles[-1][1]][tunnelTiles[-1][0]], int) and map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] != 0 and map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] != current + 1:
                                    rooms[map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] - 1].connect()
                                    stop = True
                                    roomFound = True
                                elif rooms[map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] - 1].getConnect() and map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] != 0 and map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] != current + 1:
                                    stop = True
                        if not roomFound:
                            while len(tunnelTiles) > straightLength:
                                tunnelTiles.pop()
                        for l in range(limit[dir - 1]):  # Turn tunnel Left
                            if not stop:
                                if dir == 0:
                                    tunnelTiles.append((tunnelTiles[-1][0], tunnelTiles[-1][1] - 1))
                                elif dir == 1:
                                    tunnelTiles.append((tunnelTiles[-1][0] + 1, tunnelTiles[-1][1]))
                                elif dir == 2:
                                    tunnelTiles.append((tunnelTiles[-1][0], tunnelTiles[-1][1] + 1))
                                else:
                                    tunnelTiles.append((tunnelTiles[-1][0] - 1, tunnelTiles[-1][1]))
                                try:
                                    currentTile = map[tunnelTiles[-1][1]][tunnelTiles[-1][0]]
                                except IndexError:
                                    tunnelTiles.pop() #removes the last value if the tunnel has gone off the map
                                if map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] =="C":
                                    stop = True
                                elif map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] =="F" or map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] =="U" or map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] =="D"or map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] =="T":
                                    pass #Exists to remove all strings from next checks to prevent typeError
                                elif not rooms[map[tunnelTiles[-1][1]][tunnelTiles[-1][0]]-1].getConnect() and isinstance(map[tunnelTiles[-1][1]][tunnelTiles[-1][0]], int) and map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] != 0 and map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] != current + 1:
                                    rooms[map[tunnelTiles[-1][1]][tunnelTiles[-1][0]]-1].connect()
                                    stop = True
                                    roomFound = True
                                elif rooms[map[tunnelTiles[-1][1]][tunnelTiles[-1][0]]-1].getConnect() and map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] !=0 and map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] != current + 1:
                                    stop = True
                        if not roomFound:
                            while len(tunnelTiles) > straightLength:
                                tunnelTiles.pop()
                    if not roomFound:
                        dir += 1
                        if dir == 4:
                            dir = 0
                        if dir == startCorner:
                            dirLooped = True
        if roomFound:
            current = map[tunnelTiles[-1][1]][tunnelTiles[-1][0]] - 1
            for i in range(len(tunnelTiles)):
                map[tunnelTiles[i][1]][tunnelTiles[i][0]] = "T"
            tunnelTiles = []
    check = True
    for i in range(len(rooms)): #Makes sure all rooms are connected, otherwise recurs program back from placeRooms()
        if not rooms[i].getConnect():
            check = False
    if check:
        stairPos = (random.randrange(rooms[current].getWidth() - 4), random.randrange(rooms[current].getHeight() - 4))
        map[stairPos[1] + rooms[current].getY() + 2][stairPos[0] + rooms[current].getX() + 2] = "D"
        return map
    else:
        return placeTunnels(placeRooms())

def populateLevel(map, level):
    enemyOverlay =[]
    for i in range(len(map)):
        enemyOverlay.append([])
        for j in range(len(map[0])):
            enemyOverlay[i].append(0)
    for i in range(3+int(level/10)+random.randrange(3)):#(Generate 3-5 enemies, +1 for every 10 levels)
        enemyPos = (random.randrange(len(enemyOverlay[0])), random.randrange(len(enemyOverlay)))
        while map[enemyPos[1]][enemyPos[0]] != "F" or enemyOverlay[enemyPos[1]][enemyPos[0]] != 0 or checkPlayerStart(map, enemyOverlay, enemyPos):
            enemyPos = (random.randrange(len(enemyOverlay[0])), random.randrange(len(enemyOverlay)))
        enemyOverlay[enemyPos[1]][enemyPos[0]] = "!"
    for i in range(3+random.randrange(3)): #places 3-5 chests/loot piles on every level
        lootPos = (random.randrange(len(enemyOverlay[0])), random.randrange(len(enemyOverlay)))
        while map[lootPos[1]][lootPos[0]] != "F" or enemyOverlay[lootPos[1]][lootPos[0]] != 0:
            lootPos = (random.randrange(len(enemyOverlay[0])), random.randrange(len(enemyOverlay)))
        enemyOverlay[lootPos[1]][lootPos[0]] = "L"
    return enemyOverlay

def checkPlayerStart(map, enemyOverlay, enemyPos): ## prevent enemies from generating too close to player or too close to other enemies
    for i in range(-5, 5):
        try:
            if map[enemyPos[1] + i][enemyPos[0]] == 'U' or map[enemyPos[1]][enemyPos[0] + i] == 'U': #or enemyOverlay[enemyPos[1] + i][enemyPos[0]] == '!' or enemyOverlay[enemyPos[1]][enemyPos[0] + i] == '!'
                return True
            for j in range(-5, 5):
                if map[enemyPos[1] + i][enemyPos[0] + j] == 'U' or map[enemyPos[1] + j][enemyPos[0] + i] == 'U': #or enemyOverlay[enemyPos[1] + i][enemyPos[0] + j] == '!' or enemyOverlay[enemyPos[1] + j][enemyPos[0] + i]
                    return True
        except IndexError:
            pass
    return False
def createFOW(map, tileSize):
    FOW =[]
    for i in range(len(map)):
        FOW.append([])
        for j in range(len(map[0])):
            FOW[i].append(tile("fog.png", j*tileSize, i*tileSize))
    return FOW
def checkFogOfWar(playerPos, fogOfWar, tileSize, map):
    fogOfWar[playerPos[1]//tileSize][playerPos[0]//tileSize] = 0
    for i in range(4): #For each possible direction
        if i == 0:
            dirY = 1
            dirX = 0
        elif i ==1:
            dirY = 0
            dirX = 1
        elif i == 2:
            dirY = -1
            dirX = 0
        else:
            dirY = 0
            dirX = -1
        for offset in range(-1, 2):
            wall = False
            for dist in range(1,4):
                if not (offset != 0 and dist == 3) and not wall: #Reveals a tile, then stops in that line if that tile was a wall
                    if dirY == 0:
                        fogOfWar[playerPos[1]//tileSize+offset][playerPos[0]//tileSize+dist*dirX] = 0
                        if map[playerPos[0]//tileSize+dist*dirX][playerPos[1]//tileSize+offset].get_feature() == "Wall":
                            wall = True
                    else:
                        fogOfWar[playerPos[1]//tileSize+dist*dirY][playerPos[0]//tileSize+offset] = 0
                        if map[playerPos[0]//tileSize+offset][playerPos[1]//tileSize+dist*dirY].get_feature() == "Wall":
                            wall = True
    return fogOfWar

