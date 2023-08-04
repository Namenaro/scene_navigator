from utils import IdGenedator, get_mini_ECG, draw_ECG, InterpolationSegment, ExtremumFinder

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



class Scene:
    def __init__(self, signal):
        self.signal = signal
        self.names_to_points = {}
        self.indexes_to_names = {}

        self.idgen = IdGenedator()

        self.coords_to_predictions = {}  # над любой точкой сцены самое новое предсказание (хронологичски добавленное)
        for coord in range(len(self.signal)):
            self.coords_to_predictions[coord] = 0

        self.coords_of_extrms = self.get_all_extemums_of_signal()

    def get_index_by_name(self, name):
        return self.names_to_points[name].get_coord()


    def add_point(self, coord):
        name = self.idgen.get_id()
        self.names_to_points[name] = Point(coord)
        self.indexes_to_names[coord]=name
        self.coords_to_predictions[coord] = self.signal[coord]
        return name

    def add_parent(self, child_name, parent_name):
        self.names_to_points[child_name].add_parent(parent_name)

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

    def get_error_pointwise(self):
        errs = []
        prediction = self.get_prediction()
        for i in range(len(prediction)):
            errs.append(abs(self.signal[i] - prediction[i]))
        return errs

    def get_err_max_index(self):
        errs = self.get_error_pointwise()
        whorst_index = errs.index(max(errs))
        return whorst_index

    def get_err_sum(self):
        return sum(self.get_error_pointwise())

    def get_left_nearest_point(self, index):
        non_empty_indexes = self.indexes_to_names.keys()
        left_indexes = list([other_index for other_index in non_empty_indexes if other_index<index])
        if len(left_indexes) == 0:
            return None
        sorted_left_non_empy_indexes = sorted(left_indexes, reverse=True) #по убыванию
        nearest_index = sorted_left_non_empy_indexes[0]
        name_of_nearest = self.indexes_to_names[nearest_index]
        return self.names_to_points[name_of_nearest]

    def get_right_nearest_point(self, index):
        non_empty_indexes = self.indexes_to_names.keys()
        right_indexes = list([other_index for other_index in non_empty_indexes if other_index > index])
        if len(right_indexes) == 0:
            return None
        sorted_right_non_empy_indexes = sorted(right_indexes)  # по возрастанию
        nearest_index = sorted_right_non_empy_indexes[0]
        name_of_nearest = self.indexes_to_names[nearest_index]
        return self.names_to_points[name_of_nearest]

    def get_all_extemums_of_signal(self):
        finder = ExtremumFinder(self.signal)
        coords_of_extrms = finder.get_coords_extremums()
        return coords_of_extrms

    def get_extrms_in_interval(self, index1, index2):
        left = index1
        right = index2
        if index1>index2:
            left = index2
            right = index1
        coords_extrms = []
        for index in self.coords_of_extrms:
            if index>=left and index<=right:
                coords_extrms.append(index)
        return coords_extrms

    ########################################################################
    def draw(self, ax):
        draw_ECG(ax, self.signal)
        self.draw_points(ax)
        self.draw_preiction(ax)
        self.draw_err(ax)
        self.draw_extremums()
        ax.legend(fancybox=True, framealpha=0.5)

    def draw_extremums(self):
        indexes = self.get_extrms_in_interval(0, len(self.signal)-1)
        vals = [self.signal[index] for index in indexes]
        plt.scatter(indexes, vals, label="кстремумы сигнала")

    def draw_points(self, ax):
        for name, point in self.names_to_points.items():
            ax.vlines(x=point.coord, ymin=0, ymax=max(self.signal), colors='orange', lw=1, alpha=0.5)
            text(point.coord, max(self.signal)/2, str(name), rotation=0, verticalalignment='center')

    def draw_preiction(self, ax):
        ax.plot(self.get_prediction(),  'green',ls="--", label='предсказание')

    def draw_err(self, ax):
        ax.plot(self.get_error_pointwise(), 'red', label='ошибка', alpha=0.2)
        whorst_index = self.get_err_max_index()
        ax.vlines(x=whorst_index, ymin=0, ymax=max(self.signal), colors='red', lw=2, alpha=0.5)
        text(whorst_index, max(self.signal) / 2, str("худшее"), rotation=0, verticalalignment='center', color='red')


    def draw_situation_for_index(self, ax, index):
        ax.vlines(x=index, ymin=0, ymax=max(self.signal), colors='blue', lw=1, alpha=0.5, label="ТЕСТОВАЯ т.")

        nearest_left_point = self.get_left_nearest_point(index)
        if nearest_left_point is not None:
            l_index = nearest_left_point.coord
            ax.vlines(x=l_index, ymin=0, ymax=max(self.signal), colors='blue', lw=5, alpha=0.2, label="ближайший левый оп.")

        nearest_right_point = self.get_right_nearest_point(index)
        if nearest_right_point is not None:
            r_index = nearest_right_point.coord
            ax.vlines(x=r_index, ymin=0, ymax=max(self.signal), colors='blue', lw=5, alpha=0.2,
                      label="ближайший правый оп.")

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
    #scene.draw_situation_for_index(axs, index=50)

    plt.show()



