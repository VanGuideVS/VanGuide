import numpy
import matplotlib.pyplot as plt
from myapp.backend.utils import png_to_ogm


class OccupancyGridMap:
    def __init__(self, data_array, cell_size, occupancy_threshold=0.4):

        self.data = data_array
        self.dim_cells = data_array.shape
        self.dim_meters = (self.dim_cells[1] * cell_size, self.dim_cells[0] * cell_size)
        self.cell_size = cell_size
        self.occupancy_threshold = occupancy_threshold
        # 2D array to mark visited nodes (in the beginning, no node has been visited)
        self.visited = numpy.zeros(self.dim_cells, dtype=numpy.float32)

    def mark_visited_idx(self, point_idx):

        x_index, y_index = point_idx
        if x_index < 0 or y_index < 0 or x_index >= self.dim_cells[1] or y_index >= self.dim_cells[0]:
            raise Exception('Point is outside map boundary')

        self.visited[y_index][x_index] = 1.0

    def mark_visited(self, point):

        x, y = point
        x_index, y_index = self.get_index_from_coordinates(x, y)

        return self.mark_visited_idx((x_index, y_index))

    def is_visited_idx(self, point_idx):

        x_index, y_index = point_idx
        if x_index < 0 or y_index < 0 or x_index >= self.dim_cells[1] or y_index >= self.dim_cells[0]:
            raise Exception('Point is outside map boundary')

        if self.visited[y_index][x_index] == 1.0:
            return True
        else:
            return False

    def is_visited(self, point):

        x, y = point
        x_index, y_index = self.get_index_from_coordinates(x, y)

        return self.is_visited_idx((x_index, y_index))

    def get_data_idx(self, point_idx):

        x_index, y_index = point_idx
        if x_index < 0 or y_index < 0 or x_index >= self.dim_cells[1] or y_index >= self.dim_cells[0]:
            raise Exception('Point is outside map boundary')

        return self.data[y_index][x_index]

    def get_data(self, point):

        x, y = point
        x_index, y_index = self.get_index_from_coordinates(x, y)

        return self.get_data_idx((x_index, y_index))

    def set_data_idx(self, point_idx, new_value):

        x_index, y_index = point_idx
        if x_index < 0 or y_index < 0 or x_index >= self.dim_cells[1] or y_index >= self.dim_cells[0]:
            raise Exception('Point is outside map boundary')

        self.data[y_index][x_index] = new_value

    def set_data(self, point, new_value):

        x, y = point
        x_index, y_index = self.get_index_from_coordinates(x, y)

        self.set_data_idx((x_index, y_index), new_value)

    def is_inside_idx(self, point_idx):

        x_index, y_index = point_idx
        if x_index < 0 or y_index < 0 or x_index >= self.dim_cells[1] or y_index >= self.dim_cells[0]:
            return False
        else:
            return True

    def is_inside(self, point):

        x, y = point
        x_index, y_index = self.get_index_from_coordinates(x, y)

        return self.is_inside_idx((x_index, y_index))

    def is_occupied_idx(self, point_idx):

        x_index, y_index = point_idx
        if self.get_data_idx((x_index, y_index)) >= self.occupancy_threshold:
            return True
        else:
            return False

    def is_occupied(self, point):

        x, y = point
        x_index, y_index = self.get_index_from_coordinates(x, y)

        return self.is_occupied_idx((x_index, y_index))

    def get_index_from_coordinates(self, x, y):

        x_index = int(round(x/self.cell_size))
        y_index = int(round(y/self.cell_size))

        return x_index, y_index

    def get_coordinates_from_index(self, x_index, y_index):

        x = x_index*self.cell_size
        y = y_index*self.cell_size

        return x, y

    def plot(self, alpha=1, min_val=0, origin='lower'):

        plt.imshow(self.data, vmin=min_val, vmax=1, origin=origin, interpolation='none', alpha=alpha)
        plt.draw()

    @staticmethod
    def from_png(filename, cell_size):

        ogm_data = png_to_ogm(filename, normalized=True)
        ogm_data_arr = numpy.array(ogm_data)
        ogm = OccupancyGridMap(ogm_data_arr, cell_size)
        return ogm
