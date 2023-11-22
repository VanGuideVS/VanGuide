from gridmap import OccupancyGridMap
import matplotlib.pyplot as plt
from a_star import a_star
from utils import plot_path



def manip_planner(gmap0,gmap,s_map,gmap2_manip,obj_param,start_node,goal_node,x1,x2,y1,y2):
    nodes=[start_node]
    gmap_manip=gmap2_manip
    if gmap0 != gmap:
        for o in obj_param:
            obj_x = []
            obj_y = []
            for y, x_val in enumerate(gmap.data):
                for x, y_val in enumerate(x_val):
                    if y_val != 0 and y_val == o:
                        obj_x.append(x)
                        obj_y.append(y)
            if max(obj_x) - min(obj_x) > max(obj_y) - min(obj_y):
                x_manip, y_manip = (sum(obj_x) / len(obj_x)), min(obj_y) - 3
            else:
                x_manip, y_manip = min(obj_x) - 3, (sum(obj_y) / len(obj_y))

            start_node_new = gmap.get_index_from_coordinates(x_manip, y_manip)
            nodes.append(start_node_new)
    nodes.append(goal_node)
    # run A*
    # for x in len(ojects)
    #     for y in len(ojects)
    #     path, path_px, cost_astar = a_star(start_node(x), goal_node(y), gmap_manip, movement='4N')
    #     cost
    #print(nodes)
    path, path_px, cost_astar = a_star(start_node, goal_node, gmap_manip, movement='4N')
    gmap_manip = OccupancyGridMap.from_png(s_map, 1)
    for i in range(73, 113):
        for j in range(155, 165):
            gmap_manip.set_data((i, j), 0.8)

    for i in range(113, 130):
        for j in range(135, 165):
            gmap_manip.set_data((i, j), 0.9)
    if not path:

        cost = [10e6 for _ in range (0,len(obj_param)+2)]
        cost[0]=0
        last = [-1 for _ in range(0, len(obj_param) + 2)]

        for start in range(0,len(obj_param)+2):
            # A for loop for column entries
            for finish in range(start+1,len(obj_param)+2):
                #if count == 0
                gmap_manip = OccupancyGridMap.from_png(s_map, 1)
                if start < 1:
                    for i in range(x1[0], x1[1]):
                        for j in range(y1[0], y1[1]):
                            gmap_manip.set_data((i, j), 0.8)
                if start < 2:
                    for i in range(x2[0],x2[1]):
                        for j in range(y2[0], y2[1]):
                            gmap_manip.set_data((i, j), 0.9)
                path, path_px, cost_astar = a_star(nodes[start], nodes[finish], gmap_manip, movement='4N')


                #elif count == 1
                #path, path_px, cost_astar = a_star(nodes[start], nodes[finish], gmap_manip, movement='4N')
                if path:
                    if cost_astar+cost[start]<cost[finish]:
                        cost[finish]=cost_astar+cost[start]
                        last[finish]=start
                #count = count + 1
            #a.append(cost_astar+cost(column))
        #cost.append(a)
        print(last)
    i=last[-1]
    order_path = []
    while i != 0:
        order_path.append(obj_param[i - 1])
        i=last[i]
    return order_path.__reversed__()

    




    