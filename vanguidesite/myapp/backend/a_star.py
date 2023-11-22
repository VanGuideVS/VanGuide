import math
from scipy import interpolate
import numpy as np
from heapq import heappush, heappop
from myapp.backend.utils import dist2d

def B_spline(waypoints):
    smooth=[]
    arr= np.array(waypoints)
    x,y =zip(*arr)
    
    tck, *rest = interpolate.splprep([x, y], s=0,per=False )
    u = np.linspace(0,1,int(len(waypoints)/10))
    xint,yint = interpolate.splev(u, tck)
    for i in range(len(xint)):
        smooth.append((xint[i],yint[i]))
    return smooth

def _get_movements_4n():
    """
    Get all possible 4-connectivity movements.
    :return: list of movements with cost [(dx, dy, movement_cost)]
    """
    return [(1, 0, 1.0),
            (0, 1, 1.0),
            (-1, 0, 1.0),
            (0, -1, 1.0)]

def _get_movements_8n():
    """
    Get all possible 8-connectivity movements.
    :return: list of movements with cost [(dx, dy, movement_cost)]
    """
    s2 = math.sqrt(2)
    return [(1, 0, 1.0),
            (0, 1, 1.0),
            (-1, 0, 1.0),
            (0, -1, 1.0),
            (1, 1, s2),
            (-1, 1, s2),
            (-1, -1, s2),
            (1, -1, s2),]

s2 = math.sqrt(2)
def calculate_deltacost(current_node, neighbor_node, obstacle, max_deltacost=100000):
    radius =150
    # Calculate the Euclidean distance between the current node and the neighbor node
    distance = math.sqrt((neighbor_node[0] - current_node[0]) ** 2 + (neighbor_node[1] - current_node[1]) ** 2)
    # Calculate the distance to the nearest obstacle
    min_distance = float("inf")
    if len(obstacle) != 0:
        for obs in obstacle:
            obstacle_distance = math.sqrt((neighbor_node[0] - obs[0]) ** 2 + (neighbor_node[1] - obs[1]) ** 2) - radius
            min_distance = min(min_distance, obstacle_distance)
        # Calculate the deltacost based on the distance to the nearest obstacle
        deltacost = max(0, min_distance) * max_deltacost / distance
        return deltacost
    elif len(obstacle) == 0:
        obstacle_distance = 0
        min_distance = min(min_distance, obstacle_distance)
        # Calculate the deltacost based on the distance to the nearest obstacle
        deltacost = max(0, min_distance) * max_deltacost / distance
        return deltacost
    




def a_star(start_m, goal_m, gmap, movement='8N', occupancy_cost_factor=10000):
   

    # get array indices of start and goal
    start = gmap.get_index_from_coordinates(start_m[0], start_m[1])
    goal = gmap.get_index_from_coordinates(goal_m[0], goal_m[1])

    # check if start and goal nodes correspond to free spaces
    if gmap.is_occupied_idx(start):
        raise Exception('Start node is not traversable')

    if gmap.is_occupied_idx(goal):
        raise Exception('Goal node is not traversable')

    # obstacles = []
    # for y, x_val in enumerate(gmap.data):
    #     for x, y_val in enumerate(x_val):
            
    #         occupied_position = (x,y)
    #         if gmap.is_occupied_idx(occupied_position):
    #             obstacles.append(occupied_position)
                
    # print("point id occupied")
    # print(f"{occupied_position}")
    # print(obstacles)
    # add start node to front
    # front is a list of (total estimated cost to goal, total cost from start to node, node, previous node)
    start_node_cost = 0
    start_node_estimated_cost_to_goal = dist2d(start, goal) + start_node_cost
    front = [(start_node_estimated_cost_to_goal, start_node_cost, start, None)]

    # use a dictionary to remember where we came from in order to reconstruct the path later on
    came_from = {}

    # get possible movements
    if movement == '4N':
        movements = _get_movements_4n()
    elif movement == '8N':
        movements = _get_movements_8n()
    else:
        raise ValueError('Unknown movement')

    # while there are elements to investigate in our front.
    while front:
        # get smallest item and remove from front.
        element = heappop(front)

        # if this has been visited already, skip it
        total_cost, cost, pos, previous = element
        if gmap.is_visited_idx(pos):
            continue

        # now it has been visited, mark with cost
        gmap.mark_visited_idx(pos)

        # set its previous node
        came_from[pos] = previous

        # if the goal has been reached, we are done!
        if pos == goal:
            break

        # check all neighbors
        for dx, dy, deltacost in movements:
            # determine new position
            new_x = pos[0] + dx
            new_y = pos[1] + dy
            new_pos = (new_x, new_y)

            # check whether new position is inside the map
            # if not, skip node
            if not gmap.is_inside_idx(new_pos):
                continue
            
            obstacle = []
            # add node to front if it was not visited before and is not an obstacle
            if (not gmap.is_visited_idx(new_pos)):
                if (gmap.is_occupied_idx(new_pos)):
                    obstacle.append(new_pos)
                else:
                    potential_function_cost = gmap.get_data_idx(new_pos)*occupancy_cost_factor
                    delta_cost = deltacost #+ calculate_deltacost(pos, new_pos, obstacle)
                    new_cost = cost + delta_cost + potential_function_cost
                    new_total_cost_to_goal = new_cost + dist2d(new_pos, goal) + potential_function_cost

                    heappush(front, (new_total_cost_to_goal, new_cost, new_pos, pos))

    # reconstruct path backwards (only if we reached the goal)
    path = []
    path_idx = []

    if pos == goal:    
        while pos:
            path_idx.append(pos)
            # transform array indices to meters
            pos_m_x, pos_m_y = gmap.get_coordinates_from_index(pos[0], pos[1])
            path.append((pos_m_x, pos_m_y))
            pos = came_from[pos]

        # reverse so that path is from start to goal.
        path.reverse()
        path_idx.reverse()

         
    

    return path, path_idx
