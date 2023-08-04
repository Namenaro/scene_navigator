from utils import IdGenedator, get_mini_ECG, draw_ECG


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
        self.coords = None
        self.vals = None
        
        if coord1 == coord2:
            self.vals = []
            self.coords = []
        else:
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
        step = (self.right_val - self.left_val) / len(self.coords)
        for i in range(len(self.coords) + 1):
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
