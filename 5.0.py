print("Starting")

from time import sleep, process_time
from random import randint
#from math import abs

WIDTH, HEIGHT = 80, 30
generation = 0
TEMPLATE = {31: 0,
            32: 0,
            33: 0,
            34: 0}

population = {31: 0,
            32: 0,
            33: 0,
            34: 0}
alive = {31: True,
         32: True,
         33: True,
         34: True}
totalbirths = {31: 0,
            32: 0,
            33: 0,
            34: 0}
totaldeaths = {31: 0,
            32: 0,
            33: 0,
            34: 0}
minbirths = {31: WIDTH*HEIGHT,
            32: WIDTH*HEIGHT,
            33: WIDTH*HEIGHT,
            34: WIDTH*HEIGHT}
mindeaths = {31: WIDTH*HEIGHT,
            32: WIDTH*HEIGHT,
            33: WIDTH*HEIGHT,
            34: WIDTH*HEIGHT}
maxbirths = {31: 0,
            32: 0,
            33: 0,
            34: 0}
maxdeaths = {31: 0,
            32: 0,
            33: 0,
            34: 0}

board = []
for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
        if randint(0,5) == 0:
            if y < HEIGHT // 2 and x < WIDTH // 2:
                row.append(31)
            elif y >= HEIGHT // 2 and x < WIDTH // 2:
                row.append(32)
            elif y < HEIGHT // 2 and x >= WIDTH // 2:
                row.append(33)
            else:
                row.append(34)
        else:
            row.append(0)
    board.append(row)
   
# startLiving = [(50,10),(51,11),(50,11),(51,10),(48,9),(49,8)]

# for point in startLiving:
#     board[point[1]][point[0]] = True



while True:
    tick_start = process_time()
    frame = "{0:^{1}}\n".format("Generation: {}".format(generation), WIDTH * 2)
    tempboard = board
    births = {31: 0,
            32: 0,
            33: 0,
            34: 0}
    deaths = {31: 0,
            32: 0,
            33: 0,
            34: 0}
    prev_population = population
    for colour in population:
        if alive[colour]:
            population[colour] = 0
    isDead = True
    for y, row in enumerate(board):
        line = ""
        for x, item in enumerate(row):
            # Count neighbors #
            living_neighbors = TEMPLATE
            for rel_y in range(-1,2):
                for rel_x in range(-1,2):
                    if (x + rel_x >= 0 and  # If outside of board, val = 0
                        y + rel_y >= 0 and
                        x + rel_x < WIDTH and
                        y + rel_y < HEIGHT and
                        not(rel_y==0 and rel_x==0) ): # Don't count self!
                        # and abs(rel_x) != abs(rel_y) ): # Dont count diagonals
                        if board[y + rel_y][x + rel_x] != 0:
                            living_neighbors[board[y + rel_y][x + rel_x]] += 1
            # Make decision
            # if living_neighbors < 2 and tempboard[y][x]:
            #     tempboard[y][x] = False
            #     deaths += 1
            valid_underpopulation_colours = 0
            valid_overpopulation_colours = 0
            valid_take_control_colours = 0
            control_colour = 0
            for colour in living_neighbors:
                if living_neighbors[colour] < 2:
                    valid_underpopulation_colours += 1
                elif living_neighbors[colour] > 3:
                    valid_overpopulation_colours += 1
                elif living_neighbors[colour] == 3:
                    valid_take_control_colours += 1
                    control_colour = colour
            
            if valid_underpopulation_colours == 4 and tempboard[y][x] != 0:
                deaths[tempboard[y][x]] += 1
                tempboard[y][x] = 0
            
            elif valid_overpopulation_colours > 0 and tempboard[y][x] != 0:
                deaths[tempboard[y][x]] += 1
                tempboard[y][x] = 0
                
            elif valid_take_control_colours == 1 and tempboard[y][x] != control_colour:
                tempboard[y][x] = control_colour
                births[control_colour] += 1
                
            elif valid_take_control_colours > 1 and tempboard[y][x] != 0:
                deaths[tempboard[y][x]] += 1
                tempboard[y][x] = 0
                
            
                
            # elif living_neighbors > 3 and tempboard[y][x]:
            #     tempboard[y][x] = False
            #     deaths += 1
            # elif living_neighbors == 3 and not tempboard[y][x]:
            #     tempboard[y][x] = True
            #     births += 1
           
            # if tempboard[y][x] and randint(0, ((WIDTH*HEIGHT)-prev_population) // 125) == 0:
            #     tempboard[y][x] = 0
            #     deaths += 1
           
            # Paint self to line
            if tempboard[y][x] != 0:
                line += f"\033[1;{tempboard[y][x]}m██\033[1;37m"
                population[tempboard[y][x]] += 1
                isDead = False
            else:
                line += "  "
       
        frame += line + "\n"
           

    for colour in population:
        if alive[colour]:
            totaldeaths[colour] += deaths[colour]
            totalbirths[colour] += births[colour]
            minbirths[colour] = min(minbirths[colour], births[colour])
            mindeaths[colour] = min(mindeaths[colour], deaths[colour])
            maxbirths[colour] = max(maxbirths[colour], births[colour])
            maxdeaths[colour] = max(maxdeaths[colour], deaths[colour])
    
    for colour in population:
        if alive[colour] and population[colour] == 0:
            population[colour] = generation
            alive[colour] = False
   
    for colour in population:
        if alive[colour]:
            frame += "\033[1;{0}m{1:^{2}}\n".format(colour, "Population: {}  Births: {}  Deaths: {}  Total Births: {}  Total Deaths: {}".format(population[colour], births[colour], deaths[colour], totalbirths[colour], totaldeaths[colour]), WIDTH * 2)
        else:
            frame += "\033[1;{0}m{1:^{2}}\n".format(colour, "Survived until generation: {}  Average Births: {}  Average Deaths: {}  Total Births: {}  Total Deaths: {}".format(population[colour], births[colour]//max(1,population[colour]), deaths[colour]//max(1,population[colour]), totalbirths[colour], totaldeaths[colour]), WIDTH * 2)
    #frame += "\033[1;32m{0:^{1}}\n".format("Population: {}  Births: {}  Deaths: {}  Total Births: {}  Total Deaths: {}".format(population[32], births[32], deaths[32], totalbirths[32], totaldeaths[32]), WIDTH * 2)
    #frame += "\033[1;33m{0:^{1}}\n".format("Population: {}  Births: {}  Deaths: {}  Total Births: {}  Total Deaths: {}".format(population[33], births[33], deaths[33], totalbirths[33], totaldeaths[33]), WIDTH * 2)
    #frame += "\033[1;34m{0:^{1}}\n".format("Population: {}  Births: {}  Deaths: {}  Total Births: {}  Total Deaths: {}".format(population[34], births[34], deaths[34], totalbirths[34], totaldeaths[34]), WIDTH * 2)
   
    if isDead:
        break
   
    board = tempboard
    print(frame)
    generation += 1
    sleep(max(0, 0.2 - (process_time()-tick_start)))

#print("{0:^{1}}\n".format("Average births per gen: {}  Average deaths per gen: {}  Most births in gen: {}  Most deaths in gen: {}  Least births in gen: {}  Least deaths in gen: {}".format(totalbirths//generation, totalbirths//generation, maxbirths, maxdeaths, minbirths, mindeaths), WIDTH * 2))
