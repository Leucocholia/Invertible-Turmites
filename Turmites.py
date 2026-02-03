import numpy as np
import turtle
import tkinter
import time
import os
import pygame
import sys
from math import ceil, floor
from random import randint

def add(l1, l2):
    out = []
    for i in range(len(l1)):
        out[i] = l1[i] + l2[i]
    return out

def add_evil(l1, l2):
    for i in range(len(l1)):
        l1[i] += l2[i]

def rotate(list, angle):
    return [list[(i+angle) % len(list)] for i in range(len(list))]

pygame.init()
screen = pygame.display.set_mode((600, 600))


color_scheme = [
    (0,0,0),
    (0,0,255),
    (0,255,0),
    (0,255,255),
    (255,0,0),
    (255,0,255),
    (255,255,0),
    (255,255,255)]

# color_scheme = [
#     (0,0,0),
#     (32,32,32),
#     (64,64,64),
#     (96,96,96),
#     (128,128,128),
#     (160,160,160),
#     (192,192,192),
#     (224,224,224),
#     (255,255,255)
# ]

# color_scheme.reverse()

# color_scheme = (
#     (0,0,0),
#     (0,0,0),
#     (64,0,0),
#     (0,96,0),
#     (128,0,0),
#     (0,0,0),
#     (192,192,0),
#     (0,0,0),
#     (255,0,0)
# )

# color_scheme = (
#     (0,0,0),
#     (255,32,32),
#     (255,64,64),
#     (255,96,96),
#     (255,128,128),
#     (255,160,160),
#     (255,192,192),
#     (255,224,224),
#     (255,255,255)
# )

class World:
    def __init__(self, vals, camera, screen, colors=color_scheme):
        self.vals = vals
        self.camera = camera #Formatted as rect
        self.screen = screen
        self.colors = colors
    def redraw(self):
        self.screen.fill((0,0,0))
        cell_width = self.screen.get_width() / self.camera[2]
        cell_height = self.screen.get_height() / self.camera[3]
        for y in range(self.camera[3]):
            for x in range(self.camera[2]):
                pygame.draw.rect(
                    self.screen,
                    self.colors[
                        self.vals[(x + self.camera[0]) % self.vals.shape[1]][(y + self.camera[1]) % self.vals.shape[0]]],
                    (x * cell_width,
                     y * cell_height,
                     cell_width,
                     cell_height)
                )
        pygame.display.flip()

class Turmite:
    def __init__(self, world, pos, facing, turn_reacts, jump_dists, max_dist, jump_dist=1, increment=1):
        self.world = world
        self.pos = pos
        self.facing = facing
        self.turn_reacts = turn_reacts
        self.jump_dists = jump_dists
        self.max_dist = max_dist
        self.jump_dist = jump_dist
        # It would be really cool to add modular multiplication
        self.increment = increment # What it changes the input color by
        # If divides #colors in the world, creates equal isolated cycles
        self.memory = 0 # Probably unnecessary but makes for better code
    def reposition(self):
        self.facing = (self.facing + (self.turn_reacts[self.memory])) % 4
        self.jump_dist += self.jump_dists[self.memory]
        self.jump_dist %= self.max_dist
        print(self.jump_dist, end='\r')
    def move(self):
        for _ in range(self.jump_dist):
            add_evil(self.pos, [[0,-1], [1,0], [0,1], [-1,0]][self.facing])
            self.pos[0] = self.pos[0] % self.world.vals.shape[0]
            self.pos[1] = self.pos[1] % self.world.vals.shape[1]
    def update(self):
        return (self.memory + self.increment) % len(self.world.colors)
    def draw(self):
        cell_width = self.world.screen.get_width() / self.world.camera[2]
        cell_height = self.world.screen.get_height() / self.world.camera[3]
        for y_i in range(ceil(self.world.camera[3] / self.world.vals.shape[0])):
            for x_i in range(ceil(self.world.camera[2] / self.world.vals.shape[1])):
                pixel = (
                    (self.pos[0] - self.world.camera[0] + x_i * self.world.vals.shape[1]) % self.world.camera[2] * cell_width,
                    (self.pos[1] - self.world.camera[1] + y_i * self.world.vals.shape[0]) % self.world.camera[3] * cell_height,
                    cell_width,
                    cell_height)
                pygame.draw.rect(
                    self.world.screen,
                    self.world.colors[
                                self.world.vals[(self.pos[0]) % self.world.camera[2]][(self.pos[1]) % self.world.camera[3]]],
                    pixel
                    )
                pygame.display.update(pixel)

def main(rows, cols, colors=len(color_scheme), lag=0, draw=True):
    screen.fill(color_scheme[0])
    pygame.display.flip()
    world = World(np.full([rows,cols],0), [0,0,rows,cols], screen, color_scheme[:colors])
    turn_reacts = [randint(0,3) for _ in range(colors)]
    jump_dists = [randint(-1,1) for _ in range(colors)]
    max_dist = randint(2,12)
    # max_dist = 3
    # turn_reacts = [1, -1]
    # jump_dists = [0,0]
    print(turn_reacts)
    print(jump_dists)
    print(max_dist)
    ants = [
        # Turmite(
        #     world, 
        #     [0*world.vals.shape[1]//4, world.vals.shape[1]//2], 
        #     0,
        #     turn_reacts, 
        #     jump_dists, 
        #     max_dist,
        #     increment=1),
        # Turmite(
        #     world, 
        #     [1*world.vals.shape[1]//4, world.vals.shape[1]//2], 
        #     0, 
        #     turn_reacts, 
        #     jump_dists, 
        #     max_dist,
        #     increment=1),
        Turmite(
            world, 
            [2*world.vals.shape[1]//4, world.vals.shape[1]//2], 
            0, 
            turn_reacts, 
            jump_dists, 
            max_dist,
            increment=1),
        # Turmite(
        #     world, 
        #     [3*world.vals.shape[1]//4, world.vals.shape[1]//2], 
        #     0, 
        #     turn_reacts, 
        #     jump_dists, 
        #     max_dist,
        #     increment=1)
    ]

    # world.vals[ants[1].pos[0]][ants[1].pos[1]] = 1

    generation = 0

    while True:
        generation += 1
        for ant in ants:
            ant.memory = world.vals[ant.pos[0]][ant.pos[1]]
            ant.reposition()
            world.vals[ant.pos[0]][ant.pos[1]] = ant.update()
            if draw: ant.draw()
            # if draw: world.redraw()
            ant.move()
        time.sleep(lag)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for ant in ants:
                        ant.facing = (ant.facing + 2) % 4
                        ant.move()
                        # ant.move(world.vals[ant.pos[0]][ant.pos[1]])
                        ant.increment *= -1
                        ant.turn_reacts = rotate(ant.turn_reacts, ant.increment)
                        ant.turn_reacts = [-turn_react % 4 for turn_react in ant.turn_reacts]
                        ant.jump_dists = rotate(ant.jump_dists, ant.increment)
                        ant.jump_dists = [-dist for dist in ant.jump_dists]
                        # ant.turn(world.vals[ant.pos[0]][ant.pos[1]])
                        # ant.update(world.vals[ant.pos[0]][ant.pos[1]])
                    ants.reverse()
                # elif event.key == pygame.K_r:
                #     world.vals = np.full([rows,cols],0)
                #     ant.pos = [world.vals.shape[0]//2, world.vals.shape[1]//2]
                #     ant.facing = 0
                #     world.redraw()
                elif event.key == pygame.K_d:
                    draw = not draw
                elif event.key == pygame.K_p:
                    print(ants[0].reactions)
                elif event.key == pygame.K_s:
                    print("Skipped")
                    return "SKIPPED"
                # elif event.key == pygame.K_LEFT:
                #     ant.world.camera[0] -= 1
                #     ant.world.redraw()
                # elif event.key == pygame.K_RIGHT:
                #     ant.world.camera[0] += 1
                #     ant.world.redraw()
                # elif event.key == pygame.K_UP:
                #     ant.world.camera[1] -= 1
                #     ant.world.redraw()
                # elif event.key == pygame.K_DOWN:
                #     ant.world.camera[1] += 1
                #     ant.world.redraw()
                # elif event.key == pygame.K_MINUS:
                #     for i in [2, 3]: ant.world.camera[i] += 1
                #     ant.world.redraw()
                # elif event.key == pygame.K_EQUALS:
                #     for i in [2, 3]: ant.world.camera[i] -= 1
                #     ant.world.redraw()
                    

while True: main(150,150)

# index = [1,1]
# while True:
#     print(index)
#     print(main(index[0], index[1], 0, stylized=True))
#     print('\n')
#     for i in [0, 1]:
#         index[i] += 1
        # index[i] *= 1.05
        # index[i] = floor(index[i])
    # if index[1] == 1:
    #     index.reverse()
    #     index[1] += 1
    # elif index[0] < index[1]:
    #     index[0] += 1
    # else:
    #     index[1] -= 1
# index = [1, 1]
# with open("Langton numbers.txt", "a") as file:
#     while True:
#         if index[0] == index[1]:
#             index[0] = 1
#             index[1] += 1
#         else: 
#             index.reverse()
#             if index[0] < index[1]: index[0] += 1
#         result = main(index[0],index[1])
#         print(index)
#         print(result)
#         print("\n")
#         file.write(str(index))
#         file.write(str(result))
#         file.write("\n")

    # world.vals[world.vals.shape[0]//4][world.vals.shape[1]//4] = 1
#    zoomwindow = [0, 0, rows, cols]
#
#    cell_width = (screen.get_width() / world.vals.shape[0])
#    cell_height = (screen.get_height() / world.vals.shape[1])