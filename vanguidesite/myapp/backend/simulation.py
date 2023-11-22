import pygame
import sys
from gridmap import OccupancyGridMap
import matplotlib.pyplot as plt
from simulation_planning import main
from utils import plot_path
import pandas as pd
import numpy as np
from pygame.math import Vector2
import math
from a_star import B_spline

s_map = r'Floor_Plans\floorplannumsINVERTED.png'

# Define the threshold for an occupied cell
OCCUPIED_THRESHOLD = 0.4

# Define Global Variables
dst_pos_path = []
corrected_path = []

num_paths = 0
directions_ind = 0

screen_not_filled = True

right_held = False
left_held = False
up_held = False
down_held = False

path_north = False
path_south = False
path_west = False
path_east = False
path_north_west = False
path_north_east = False
path_south_west = False
path_south_east = False

# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("VanGuide by The Vanguard Spectrum")

#Second Screen
screen_two = pygame.Surface((100, 100))
screen_two.fill((255, 255, 255))
screen_two_rect = screen_two.get_rect()
screen_two_rect.center = ((50,50))

#Button in Second screen
button_rect = pygame.Rect(0, 0, 20, 20)
button_rect.center = screen_two_rect.center

# Load an image to represent the point
point_size = 2
point_image = pygame.Surface((point_size*2, point_size*2), pygame.SRCALPHA)
pygame.draw.rect(point_image, (255, 0, 0), (0, 0, point_size*2, point_size*2))

curr_pos_image = pygame.Surface((point_size*2, point_size*2), pygame.SRCALPHA)
pygame.draw.rect(curr_pos_image, (0, 255, 0), (0, 0, point_size*2, point_size*2))

# Set the initial position of the point
clock =pygame.time.Clock()
# Create a 2D list to represent the occupancy grid
occupancy_grid = np.flip((OccupancyGridMap.from_png(s_map, 1)).data, axis = 0)
map_shape = occupancy_grid.shape
GRID_WIDTH = map_shape[1]
GRID_HEIGHT = map_shape[0]

point_position = (190, -280+GRID_HEIGHT)
curr_pos = point_position
prev_pos = curr_pos

room_destination = input('Enter the room number you want to visit:\n')
path = main(point_position, room_destination)
# for i in range(len(path)):
#     corrected_path.append((path[i][0], -path[i][1]+GRID_HEIGHT))
path_instruct= B_spline(path)
print(len(path_instruct))
# Create a game loop
while True:
    while screen_not_filled:
        screen.fill((0, 0, 0))
        screen_not_filled = False
                
    for event in pygame.event.get():
        # Draw the occupancy grid       
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_UP and curr_pos[1] > 0 and occupancy_grid[curr_pos[1]-1][curr_pos[0]] < OCCUPIED_THRESHOLD:
                up_held = True
                prev_pos = curr_pos
                curr_pos = (curr_pos[0], curr_pos[1]-1)
            elif event.key == pygame.K_DOWN and curr_pos[1] < GRID_HEIGHT-1 and occupancy_grid[curr_pos[1]+1][curr_pos[0]] < OCCUPIED_THRESHOLD:
                down_held = True
                prev_pos = curr_pos
                curr_pos = (curr_pos[0], curr_pos[1]+1)
            elif event.key == pygame.K_LEFT and curr_pos[0] > 0 and occupancy_grid[curr_pos[1]][curr_pos[0]-1] < OCCUPIED_THRESHOLD:
                left_held = True
                prev_pos = curr_pos
                curr_pos = (curr_pos[0]-1, curr_pos[1])
            elif event.key == pygame.K_RIGHT and curr_pos[0] < GRID_WIDTH-1 and occupancy_grid[curr_pos[1]][curr_pos[0]+1] < OCCUPIED_THRESHOLD:
                right_held = True
                prev_pos = curr_pos
                curr_pos = (curr_pos[0]+1, curr_pos[1])
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and button_rect.collidepoint(event.pos):
                print("Are you lost?")
                point_position = curr_pos
                room_destination = input('Enter the room number you want to visit:\n')
                path = main(point_position, room_destination)
                path_north = False
                path_south = False
                path_east = False
                path_west = False
                directions_ind = 0
                num_paths = 0
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up_held = False
            elif event.key == pygame.K_DOWN:
                down_held = False
            elif event.key == pygame.K_LEFT:
                left_held = False
            elif event.key == pygame.K_RIGHT:
                right_held = False
            curr_pos = curr_pos
            prev_pos = curr_pos

        screen.blit(curr_pos_image, (curr_pos[0]*1, curr_pos[1]*1))
        pygame.display.flip()

        if num_paths == 0:
            x = [x[0] for x in path]
            y = [y[1] for y in path]

            bounding_area = [()]
            for i in range(len(path)):
                for j in range(1,20):
                    max_x = x[i]+j
                    min_x = x[i]-j
                    max_y = y[i]+j
                    min_y = y[i]-j

                    bounding_area.append((x[i], -y[i]+GRID_HEIGHT))
                    bounding_area.append((max_x, -max_y+GRID_HEIGHT))
                    bounding_area.append((min_x, -min_y+GRID_HEIGHT))
                    bounding_area.append((x[i], -max_y+GRID_HEIGHT))
                    bounding_area.append((x[i], -min_y+GRID_HEIGHT))
                    bounding_area.append((max_x, -y[i]+GRID_HEIGHT))
                    bounding_area.append((min_x, -y[i]+GRID_HEIGHT))
                    bounding_area.append((max_x, -min_y+GRID_HEIGHT))
                    bounding_area.append((min_x, -max_y+GRID_HEIGHT))

            print("the length of bounding area is: ", len(bounding_area))
            print("the length of the PATH is: ", len(path))
            point_start= point_position 
            point_inst = point_position
            screen.fill((0, 0, 0))
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if occupancy_grid[y][x] >= OCCUPIED_THRESHOLD:
                        pygame.draw.rect(screen, (255, 255, 255), (x*1, y*1, 1, 1))
                pygame.display.flip()
            count = 0
            for i in range (1,len(path)):
                # Get the current and next points in the path
                current_point = path[i - 1]
                next_point = path[i]

                # Calculate the distance and direction to the next point
                dx = next_point[0] - current_point[0]
                dy = (-next_point[1]+GRID_HEIGHT) - (-current_point[1]+GRID_HEIGHT)
                distance = ((dx ** 2) + (dy ** 2)) ** 0.5
                direction = Vector2(dx, dy).normalize()

                # Update the position of the point
                
                point_start+= direction * distance

                # Draw the point
                if count <= 0:
                    pygame.display.flip()
                    screen.blit(point_image, (point_start[0]*1, point_start[1]*1))
                    clock.tick(60)
                    
        
            for i in range (1,len(path_instruct)):
                # Get the current and next points in the path
                current_point = path_instruct[i - 1]
                next_point = path_instruct[i]

                # Calculate the distance and direction to the next point
                dx = next_point[0] - current_point[0]
                dy = (-next_point[1]+GRID_HEIGHT) - (-current_point[1]+GRID_HEIGHT)
                distance= ((dx ** 2) + (dy ** 2)) ** 0.5
                direction= Vector2(dx, dy).normalize()

                # Update the position of the point
                
                point_inst += direction * distance

                # Draw the point
                if count <= 0:
                    pygame.display.flip()
                    screen.blit(point_image, (point_inst[0]*1, point_inst[1]*1))
                    clock.tick(60)
                    
                    
                end_goal_area = []
                end_goal_area.append((int(point_position[0]), int(point_position[1])))
                for pos in range(1, 30):
                    for neg in range(1, 30):
                            end_goal_area.append((int(point_position[0]+pos), int(point_position[1]+pos)))
                            end_goal_area.append((int(point_position[0]-neg), int(point_position[1]-neg)))
                            end_goal_area.append((int(point_position[0]+pos), int(point_position[1])))
                            end_goal_area.append((int(point_position[0]), int(point_position[1]+pos)))
                            end_goal_area.append((int(point_position[0]-neg), int(point_position[1])))
                            end_goal_area.append((int(point_position[0]), int(point_position[1]-neg)))
                            end_goal_area.append((int(point_position[0]+pos), int(point_position[1]-neg)))
                            end_goal_area.append((int(point_position[0]-neg), int(point_position[1]+pos)))
            count =count+1   
            num_paths =+ 1
   
    if up_held == True and curr_pos[1] > 0 and occupancy_grid[curr_pos[1]-1][curr_pos[0]] < OCCUPIED_THRESHOLD:
        prev_pos = curr_pos
        curr_pos = (curr_pos[0], curr_pos[1]-1)
        clock.tick(60)
    if down_held == True and curr_pos[1] < GRID_HEIGHT-1 and occupancy_grid[curr_pos[1]+1][curr_pos[0]] < OCCUPIED_THRESHOLD:
        prev_pos = curr_pos
        curr_pos = (curr_pos[0], curr_pos[1]+1)
        clock.tick(60)
    if left_held == True and curr_pos[0] > 0 and occupancy_grid[curr_pos[1]][curr_pos[0]-1] < OCCUPIED_THRESHOLD:
        prev_pos = curr_pos
        curr_pos = (curr_pos[0]-1, curr_pos[1])
        clock.tick(60)
    if right_held == True and curr_pos[0] < GRID_WIDTH-1 and occupancy_grid[curr_pos[1]][curr_pos[0]+1] < OCCUPIED_THRESHOLD:
        prev_pos = curr_pos
        curr_pos = (curr_pos[0]+1, curr_pos[1])
        clock.tick(60)

    if curr_pos not in bounding_area:
            print("Rerouting")
            point_position = curr_pos
            path = main(point_position, room_destination)
            path = B_spline(path)
            path_north = False
            path_south = False
            path_east = False
            path_west = False
            directions_ind = 0
            num_paths = 0
    
    if directions_ind == 0:
        steps = 400
        for i in range(0,len(path) - steps, steps):
            
                if ((path[i][1] - path[i+steps][1]) <= -1) and ((path[i][0] - path[i+steps][0]) == 0) and path_north == False:
                    path_north = True
                    path_south = False
                    path_east = False
                    path_west = False
                    print("Move North")
                if ((path[i][1] - path[i+steps][1]) >= 1) and ((path[i][0] - path[i+steps][0]) == 0) and path_south == False:
                    path_north = False
                    path_south = True
                    path_east = False
                    path_west = False
                    print("Move South")
                if ((path[i][0] - path[i+steps][0]) <= -1) and ((path[i][1] - path[i+steps][1]) == 0) and path_east == False:
                    path_north = False
                    path_south = False
                    path_east = True
                    path_west = False
                    print("Move East")
                if ((path[i][0] - path[i+steps][0]) >= 1) and ((path[i][1] - path[i+steps][1]) == 0) and path_west == False:
                    path_north = False
                    path_south = False
                    path_east = False
                    path_west = True
                    print("Move West")

        path_north = False
        path_south = False
        path_east = False
        path_west = False

        directions_ind = 1
    
    for i in range(len(path)):
        dst_pos_path.append((((path[i][0] - curr_pos[0]) ** 2) + ((-path[i][1]+GRID_HEIGHT - curr_pos[1]) ** 2)) ** 0.5)
        
    min_dst_to_path = min(dst_pos_path)
    min_dst_to_path_index = dst_pos_path.index(min_dst_to_path)

    closest_point = Vector2(path[min_dst_to_path_index][0], -path[min_dst_to_path_index][1]+GRID_HEIGHT)

    direction_to_path = closest_point - Vector2(curr_pos)
    if direction_to_path.length() != 0:
        direction_to_path.normalize()
    
    if direction_to_path[0] > 0:
        print("the path is east")
    if direction_to_path[0] < 0:
        print("the path is west")
    if direction_to_path[1] > 1:
        print("the path is south")
    if direction_to_path[1] < 0:
        print("the path is north")

    if curr_pos in end_goal_area:
        print("POSITION: ", curr_pos)
        print("You reached your destination!")
        # pygame.quit()
        # sys.exit()

    screen.blit(curr_pos_image, (curr_pos[0]*1, curr_pos[1]*1))
    pygame.display.flip()

    screen.blit(screen_two, screen_two_rect)
    pygame.draw.rect(screen_two, (255, 0, 0), button_rect)
    pygame.display.flip()
    dst_pos_path = []