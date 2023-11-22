from gridmap import OccupancyGridMap
import matplotlib.pyplot as plt
from a_star import a_star
from utils import plot_path



if __name__ == '__main__':

    #load the map
    #Scenario map
    s_map = 'example_map_binary.png'
    gmap0 = OccupancyGridMap.from_png('example_map_binary.png', 1)
    gmap0_manip = OccupancyGridMap.from_png('example_map_binary.png', 1)
    gmap = OccupancyGridMap.from_png(s_map, 1)
    gmap_manip = OccupancyGridMap.from_png(s_map, 1)
    gmap1 = OccupancyGridMap.from_png(s_map, 1)
    gmap2 = OccupancyGridMap.from_png(s_map, 1)
    gmap1_manip = OccupancyGridMap.from_png(s_map, 1)
    gmap2_manip = OccupancyGridMap.from_png(s_map, 1)

    #object formulation 
    #object 1:
    for i in range (73,113):
        for j in range(155,165):
            gmap.set_data((i,j), 0.8)
            gmap1.set_data((i,j), 0.8)
            gmap2.set_data((i,j), 0.8)
            
    #object 2:
    for i in range (113,130):
        for j in range(135,165):
            gmap.set_data((i,j), 0.9)
            gmap1.set_data((i,j), 0.9)
            gmap2.set_data((i,j), 0.9)
        
            
    
    # set a start and an end node (in meters)
    goal_node = (50,200)
    start_node= (285.0, 86.0)

    

    gmap.plot()
    start_node_px = gmap.get_index_from_coordinates(start_node[0], start_node[1])
    goal_node_px = gmap.get_index_from_coordinates(goal_node[0], goal_node[1])

    plt.plot(start_node_px[0], start_node_px[1], 'ro')
    plt.plot(goal_node_px[0], goal_node_px[1], 'go')

    # run A*
    path, path_px, cost_astar = a_star(start_node, goal_node, gmap, movement='4N')

    

    if path:

        plot_path(path_px)
    else:
        plt.show()
        print("path is blocked, attempting to remove dynamic obstacles")
        if gmap0 != gmap:
            manip_plan = [0.8,0.9]
            count = 0
            for o in manip_plan:
                obj_x = []
                obj_y = []
                for y, x_val in enumerate(gmap.data):
                    for x, y_val in enumerate(x_val):
                        if y_val != 0 and  y_val == o:
                            obj_x.append(x)
                            obj_y.append(y)
                            gmap.set_data((x,y), 0)
                            if count == 0:
                                gmap2.set_data((x,y), 0)
                            if gmap.data[x, y] == gmap0.data[x, y]:
                                object_manip = True
                            else:
                                object_manip = False
                
                if len(obj_x) < 30 and len(obj_y) < 30:
                    print("object blocking path is static")
                else:
                    if max(obj_x)-min(obj_x) > max(obj_y)-min(obj_y):
                        x_manip, y_manip = (sum(obj_x)/len(obj_x)), min(obj_y)-3
                    else:
                        x_manip, y_manip = min(obj_x) - 3, (sum(obj_y) / len(obj_y))

                    start_node_new = gmap.get_index_from_coordinates(x_manip,y_manip)
                    if count == 0:
                        path_mid, path_px_mid, cost_midastr = a_star(start_node, start_node_new, gmap1, movement='4N')
                        new_node = start_node_new
                        gmap1.plot()
                        plot_path(path_px_mid)
                        plt.show()
                    else: 
                        path_mid, path_px_mid, cost_midstr2= a_star(new_node, start_node_new, gmap2, movement='4N')
                        gmap2.plot()
                        plot_path(path_px_mid)
                        plt.show()
                count+=1  

                if object_manip:
                    print("object removed")

            #gmap_manip = OccupancyGridMap.from_png('fig2', 1)
            path_rep, path_px_rep, cost_freepath = a_star(start_node_new, goal_node, gmap0, movement='4N')
            print(path_rep)
            print('cost:', cost_freepath)
            if path_rep:
                gmap.plot()
                plot_path(path_px_rep)
            else:
                print("didn't manipulate object successfully")






    
    
    