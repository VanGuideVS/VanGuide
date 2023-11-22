from myapp.backend.gridmap import OccupancyGridMap
import matplotlib.pyplot as plt
from myapp.backend.a_star import a_star
from myapp.backend.utils import plot_path
import pandas as pd

def map_and_csv_selection(room_number):
    print(room_number[0:2])
    
    if len(room_number) <=5:
        s_mapb= f'myapp\\backend\Floor_Plans\\atlas{room_number[0]}_b.png'
        s_mapt= f'myapp\\backend\Floor_Plans\\atlas{room_number[0]}_t.png'
        
        dfb = pd.read_csv(f'myapp\\backend\Text_Detecting\CSV_FILES\Atlas_{room_number[0]}_b', dtype={'room_number': str})
        roomb = list(dfb['room_number'].to_numpy())
        coordinates = list(dfb['coordinates'].to_numpy())
        xb = [int(eval(sublist)[0][0]) for sublist in coordinates]
        yb = [int(eval(sublist)[0][1]) for sublist in coordinates]
        
        dft = pd.read_csv(f'myapp\\backend\Text_Detecting\CSV_FILES\Atlas_{room_number[0]}_t', dtype={'room_number': str})
        roomt = list(dft['room_number'].to_numpy())
        coordinates = list(dft['coordinates'].to_numpy())
        xt = [int(eval(sublist)[0][0]) for sublist in coordinates]
        yt = [int(eval(sublist)[0][1]) for sublist in coordinates]
        
 
        
    else:
        s_mapb= f'myapp\\backend\Floor_Plans\\atlas{room_number[0:2]}_b.png'
        s_mapt= f'myapp\\backend\Floor_Plans\\atlas{room_number[0:2]}_t.png'
        
        dfb = pd.read_csv(f'myapp\\backend\Text_Detecting\CSV_FILES\Atlas_{room_number[0:2]}_b', dtype={'room_number': str})
        roomb = list(dfb['room_number'].to_numpy())
        coordinates = list(dfb['coordinates'].to_numpy())
        xb = [int(eval(sublist)[0][0]) for sublist in coordinates]
        yb = [int(eval(sublist)[0][1]) for sublist in coordinates]
        
        dft = pd.read_csv(f'myapp\\backend\Text_Detecting\CSV_FILES\Atlas_{room_number[0:2]}_t', dtype={'room_number': str})
        roomt = list(dft['room_number'].to_numpy())
        coordinates = list(dft['coordinates'].to_numpy())
        xt = [int(eval(sublist)[0][0]) for sublist in coordinates]
        yt = [int(eval(sublist)[0][1]) for sublist in coordinates]
            
    return s_mapb,s_mapt,roomb,roomt,xt,yt,xb,yb 
    
def loader(room_destination):
    s_mapb,s_mapt,roomb,roomt,xt,yt,xb,yb = map_and_csv_selection(room_destination)
    
    found_in_b = False
    found_int = False

    print(roomb)
    name = 'test.png'
    if not found_int:
        for i in roomb:
            if i == room_destination:
                index = roomb.index(i)
                print("The rooms details are:", (xb[index],yb[index],roomb[index]))
                print("The room number is:", i)
                print(f"x-coordinate is: {xb[index]}, y-coordinate is: {yb[index]}")
                x_goal = xb[index]
                y_goal = yb[index]
                found_in_b = True
                found_int = False
                break 
            #else:
                #print('couldnt find room in b')
        
    if not found_in_b:
        for i in roomt:
            if i == room_destination:
                index = roomt.index(i)
                print("The rooms details are:", (xt[index],yt[index],roomt[index]))
                print("The room number is:", i)
                print(f"x-coordinate is: {xt[index]}, y-coordinate is: {yt[index]}")
                x_goal = xt[index]
                y_goal = yt[index]
                found_int = True
                found_in_b = False
                break
            #else:
                #print('couldnt find room in t')
    
    print(f'found_in_t: {found_int}, found_in_b: {found_in_b}')
    if found_int:
        gmapb = OccupancyGridMap.from_png(s_mapb, 1)
        gmapt = OccupancyGridMap.from_png(s_mapt, 1)
        #set a start and an end node (in meters)
        gmapt.plot()
        print('loading top map')
        goal_node = (x_goal, y_goal)
        start_node = (196, 160)
    
        start_node_px = gmapb.get_index_from_coordinates(start_node[0], start_node[1])
        goal_node_px = gmapb.get_index_from_coordinates(goal_node[0], goal_node[1])

        plt.plot(start_node_px[0], start_node_px[1], 'ro')
        plt.plot(goal_node_px[0], goal_node_px[1], 'go')

        # run A*
        path, path_px= a_star(start_node, goal_node, gmapt, movement='8N')
        # print(cost_astar)
        if path:
            plot_path(path_px)
        #else:
            #plt.show()
        
        #plt.show()
        plt.savefig(name, dpi=900)
        found_int = False

    if found_in_b:
        #set a start and an end node (in meters)
        gmapb.plot()
        print('loading bottom map')
        goal_node = (x_goal, y_goal)
        start_node = (196, 160)
    
        start_node_px = gmapb.get_index_from_coordinates(start_node[0], start_node[1])
        goal_node_px = gmapb.get_index_from_coordinates(goal_node[0], goal_node[1])

        plt.plot(start_node_px[0], start_node_px[1], 'ro')
        plt.plot(goal_node_px[0], goal_node_px[1], 'go')

        # run A*
        path, path_px= a_star(start_node, goal_node, gmapb, movement='8N')
        # print(cost_astar)
        if path:
            plot_path(path_px)
        #else:
            #plt.show()
        
        #plt.show()
        plt.savefig(name, dpi=900)
        found_in_b = False