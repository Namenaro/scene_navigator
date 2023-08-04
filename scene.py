from utils import IdGenedator, get_mini_ECG, draw_ECG

import matplotlib.pyplot as plt
from matplotlib.pyplot import text

class Point:
    def __init__(self, coord):
        self.parents_names = []
        self.coord = coord

    def add_parent(self, parent_name):
        self.parents_names.append(parent_name)

    def get_coord(self):
        return self.coord


class InterpolationSegment:
    def __init__(self, coord1, val1, coord2, val2):
        self.coords = []
        self.vals = []

        if coord1 != coord2:

            self.left_coord= coord1
            self.left_val = val1

            self.right_coord = coord2
            self.right_val = val2

            if coord2 < coord1:
                self.left_coord = coord2
                self.left_val = val2

                self.right_coord = coord1
                self.right_val = val1
            self._calculate_interpolation()

    def get_vals_from_left(self):
        return self.vals

    def get_indexes_from_left(self):
        return self.coords

    def _calculate_interpolation(self):
        self.coords = list(range(self.left_coord, self.right_coord + 1))
        step = (self.right_val - self.left_val) / (len(self.coords)-1)
        for i in range(len(self.coords) ):
            self.vals.append(self.left_val + i * step)

class Scene:
    def __init__(self, signal):
        self.signal = signal
        self.names_points = {}

        self.idgen = IdGenedator()

        self.coords_to_predictions = {}  # над любой точкой сцены самое новое предсказание (хронологичски добавленное)
        for coord in range(len(self.signal)):
            self.coords_to_predictions[coord] = 0

    def get_index_by_name(self, name):
        return self.names_points[name].get_coord()


    def add_point(self, coord):
        name = self.idgen.get_id()
        self.names_points[name] = Point(coord)
        self.coords_to_predictions[coord] = self.signal[coord]
        return name

    def add_parent(self, child_name, parent_name):
        self.names_points[child_name].add_parent(parent_name)

        index1 = self.get_index_by_name(child_name)
        index2 = self.get_index_by_name(parent_name)
        self._register_new_segment(index1, index2)

    def _register_new_segment(self, index1, index2):
        seg = InterpolationSegment(index1, self.signal[index1], index2, self.signal[index2])
        vals = seg.get_vals_from_left()
        indexes = seg.get_indexes_from_left()

        for i in range(len(vals)):
            coord = indexes[i]
            val = vals[i]

            self.coords_to_predictions[coord] = val

    def get_prediction(self):
        pointwise_prediction = []
        for coord in range(len(self.signal)):
            pointwise_prediction.append(self.coords_to_predictions[coord])

        return pointwise_prediction

    def draw(self, ax):
        draw_ECG(ax, self.signal)
        self.draw_points(ax)
        self.draw_preiction(ax)
        ax.legend(fancybox=True, framealpha=0.5)

    def draw_points(self, ax):
        for name, point in self.names_points.items():
            ax.vlines(x=point.coord, ymin=0, ymax=max(self.signal), colors='orange', lw=1, alpha=0.5)
            text(point.coord, max(self.signal)/2, str(name), rotation=0, verticalalignment='center')

    def draw_preiction(self, ax):
        ax.plot(self.get_prediction(), 'green', label='предсказание')

if __name__ == '__main__':
    signal = get_mini_ECG()


    scene = Scene(signal)
    name_1 = scene.add_point(coord=105)
    name_2 = scene.add_point(coord=94)
    scene.add_parent(parent_name=name_1, child_name=name_2)

    name_3 = scene.add_point(coord=53)
    scene.add_parent(parent_name=name_1, child_name=name_3)


    fig, axs = plt.subplots()
    scene.draw(axs)

    plt.show()



