from SCENE import Scene, WScene
from PROGRAM import Restriction, Program, ParentInfo
from .predict import PredictionInContext
from MEASURE_INFO import get_profit_koef_of_prediction

from copy import deepcopy

class RecogniserEngine:
    def __init__(self, signal, program):
        self.scene = Scene(signal)
        self.program = program

        self.current_point = 0
        # добавляем в сцену первое событие из программы


    def get_evaluated_childrens_scenes_for_scene(self, parent_scene):
        child_scenes = []
        child_ws = []
        child_coeffs = []

        prediction_contexted = PredictionInContext(self.current_point)
        prediction_contexted.fill(parent_scene, self.program)
        name = self.current_point


        # находим все максимумы ошибки в области, заданной ограничениями
        # это и есть наши кандидаты:
        error_maxes_allowed = parent_scene.get_all_maxes_of_err_in_area(prediction_contexted.left_resctiction, prediction_contexted.right_rescriction)
        if error_maxes_allowed is None:
            return None, None, None

        # у них всех одинаковый бассейн, координата родителя и предсказанное отклонение от описания
        bassin_coords_for_coord = parent_scene.get_bassin_coords_for_coord(error_maxes_allowed[0])
        parent_coord = parent_scene.get_index_by_name(prediction_contexted.get_parent_name_for_child_name(name))
        val_predicted= self.program.get_predicted_val_for_name(name)

        # обертка для сцены, которая умеет мерять w
        w_scene = WScene(parent_scene, bassin_coords=bassin_coords_for_coord, parent_coord=parent_coord, val_predicted=val_predicted)

        for candidate_coord in error_maxes_allowed:
            # cоздаем сцену-ребенка
            child_scene = deepcopy(parent_scene)
            child_scene.add_point(coord=candidate_coord, name=name)
            child_scene.add_parent(child_name=name, parent_name=self.program.get_parent_name_for_child_name(name))
            child_scenes.append(child_scene)

            # меряем w_unnormed
            w = w_scene.measure_w_unnormed(candidate_coord)
            child_ws.append(w)

            # меряем коэф-т значительности ошибки предсказания по сравнению к ошибке порожденного им описания в контексе физ-единиц
            err_of_old_description = parent_scene.get_err_sum()
            err_after_update_description = child_scene.get_err_sum()
            koef = get_profit_koef_of_prediction(err_of_old_description=err_of_old_description, err_after_update_description=err_after_update_description)
            child_coeffs.append(koef)

        self.current_point += 1

        return child_scenes, child_ws, child_coeffs


