print("Starting")

from time import sleep, process_time
from random import randint
from os import system, name
#from math import abs

WIDTH, HEIGHT = 80, 43
generation = 0
population = 0
totalbirths, totaldeaths = 0, 0
minbirths, mindeaths = WIDTH*HEIGHT, WIDTH*HEIGHT
maxbirths, maxdeaths = 0, 0

board = []
for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
        if randint(0,7) == 0:
            row.append(True)
        else:
            row.append(False)
    board.append(row)
   
# startLiving = [(50,10),(51,11),(50,11),(51,10),(48,9),(49,8)]

# for point in startLiving:
#     board[point[1]][point[0]] = True



while True:
    tick_start = process_time()
    frame = "{0:^{1}}\n".format("Generation: {}".format(generation), WIDTH * 2)
    tempboard = board
    births, deaths = 0, 0
    prev_population = population
    population = 0
    isDead = True
    for y, row in enumerate(board):
        line = ""
        for x, item in enumerate(row):
            # Count neighbors #
            living_neighbors = 0
            for rel_y in range(-1,2):
                for rel_x in range(-1,2):
                    if (x + rel_x >= 0 and  # If outside of board, val = 0
                        y + rel_y >= 0 and
                        x + rel_x < WIDTH and
                        y + rel_y < HEIGHT and
                        not(rel_y==0 and rel_x==0) ): # Don't count self!
                        # and abs(rel_x) != abs(rel_y) ): # Dont count diagonals
                        if board[y + rel_y][x + rel_x]:
                            living_neighbors += 1
            # Make decision
            if living_neighbors < 2 and tempboard[y][x]:
                tempboard[y][x] = False
                deaths += 1
            elif living_neighbors > 3 and tempboard[y][x]:
                tempboard[y][x] = False
                deaths += 1
            elif living_neighbors == 3 and not tempboard[y][x]:
                tempboard[y][x] = True
                births += 1
           
            if tempboard[y][x] and randint(0, ((WIDTH*HEIGHT)-prev_population) // 125) == 0:
                tempboard[y][x] = False
                deaths += 1
           
            # Paint self to line
            if tempboard[y][x]:
                line += "██"
                population += 1
                isDead = False
            else:
                line += "  "
       
        frame += line + "\n"
           
    totaldeaths += deaths
    totalbirths += births
    minbirths = min(minbirths, births)
    mindeaths = min(mindeaths, deaths)
    maxbirths = max(maxbirths, births)
    maxdeaths = max(maxdeaths, deaths)
   
    frame += "{0:^{1}}\n".format("Population: {}  Births: {}  Deaths: {}  Total Births: {}  Total Deaths: {}".format(population, births, deaths, totalbirths, totaldeaths), WIDTH * 2)
   
    if isDead:
        break
   
    board = tempboard
    system('cls' if name == 'nt' else 'clear')
    print(frame)
    generation += 1
    sleep(max(0, 0.1 - (process_time()-tick_start)))

print("{0:^{1}}\n".format("Average births per gen: {}  Average deaths per gen: {}  Most births in gen: {}  Most deaths in gen: {}  Least births in gen: {}  Least deaths in gen: {}".format(totalbirths//generation, totalbirths//generation, maxbirths, maxdeaths, minbirths, mindeaths), WIDTH * 2))