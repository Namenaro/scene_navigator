# обертка для класса сцены, позволающая посчитать w для пары - предсказание: исполнение

from MEASURE_INFO import MeasurerWUnnormed
from .scene import Scene
from utils import get_coords_of_segment

class WScene:
    def __init__(self, parent_scene, bassin_coords, parent_coord,val_predicted):
        variation_signal = []
        for coord in range(parent_scene.get_size()):
            if coord not in bassin_coords:
                variation_signal.append(None)
            else:
                deviation_in_point = parent_scene.get_devation_in_coord(coord)
                variation_signal.append(deviation_in_point)

        self.two_points_scene = Scene(signal=variation_signal)
        self.parent_name = self.two_points_scene.add_point(parent_coord)

        self.val_predicted = val_predicted

        self.parent_coord = parent_coord
        self.bassin_errs = list([abs(self.two_points_scene.signal[i] - self.val_predicted) for i in bassin_coords])



    def measure_w_unnormed(self,  candidate_coord, u_err):
        child_name = self.two_points_scene.add_point(candidate_coord)
        self.two_points_scene.add_parent(child_name=child_name, parent_name=self.parent_name)

        segment_coords = get_coords_of_segment(self.parent_coord, candidate_coord)
        segment_errs = list([abs(self.two_points_scene.signal[i] - self.val_predicted) for i in segment_coords])
        w_measurer = MeasurerWUnnormed(u_err, v_errs_on_segment=segment_errs, bassin_vs=self.bassin_errs)
        w_unnormed = w_measurer.get_w()
        return w_unnormed
