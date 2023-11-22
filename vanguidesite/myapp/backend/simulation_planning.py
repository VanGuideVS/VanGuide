from gridmap import OccupancyGridMap
import matplotlib.pyplot as plt
from a_star import a_star
from utils import plot_path
import pandas as pd

def main(position, room_destination):

    #load the map
    #Scenario map
    s_map = r'Floor_Plans\floorplannumsINVERTED.png'
    gmap0 = OccupancyGridMap.from_png(s_map, 1)
    gmap0_manip = OccupancyGridMap.from_png(s_map, 1)
    gmap = OccupancyGridMap.from_png(s_map, 1)
    gmap_manip = OccupancyGridMap.from_png(s_map, 1)
    gmap1 = OccupancyGridMap.from_png(s_map, 1)
    gmap2 = OccupancyGridMap.from_png(s_map, 1)
    gmap1_manip = OccupancyGridMap.from_png(s_map, 1)
    gmap2_manip = OccupancyGridMap.from_png(s_map, 1)


 
    df = pd.read_csv(r'Text_Detecting\CSV_FILES\floorplan_GoogleVision')
    room = list(df['room_number'].to_numpy())
    coordinates = list(df['coordinates'].to_numpy())
    x = [int(eval(sublist)[0][0]) for sublist in coordinates]
    y = [int(eval(sublist)[0][1]) for sublist in coordinates]
    
    for i in room:
        if i == int(room_destination):
            index = room.index(i)
            # print("The rooms details are:", (x[index],y[index],room[index]))
            # print("The room number is:", i)
            # print(f"x-coordinate is: {x[index]}, y-coordinate is: {y[index]}")
            x_goal = x[index]
            y_goal = y[index]
            break 
        else:
            continue   
    
    #set a start and an end node (in meters)
    goal_node = (x_goal, y_goal)
    start_node = (position[0], -position[1]+450)
    obj_param = [0.8, 0.9]


    gmap.plot()
    plt.show()

    start_node_px = gmap.get_index_from_coordinates(start_node[0], start_node[1])
    goal_node_px = gmap.get_index_from_coordinates(goal_node[0], goal_node[1])

    plt.plot(start_node_px[0], start_node_px[1], 'ro')
    plt.plot(goal_node_px[0], goal_node_px[1], 'go')

    # run A*
    path, path_px = a_star(start_node, goal_node, gmap_manip,movement='8N')
   
    
    return(path_px)
    
    





    
    