from SCENE.scene import Scene
from utils import get_mini_ECG, HtmlLogger


import matplotlib.pyplot as plt
from copy import deepcopy



# Жадная минимизации ошибки аппроксимации на сцене в физических единицах (никакой нормировки, никакого w)
# Жадность на 1 шаг (самая примитивная, не учитывает пологость максимумов ошибки, только амптитуду)

class Grower:
    def __init__(self, scene):
        self.scene = deepcopy(scene)
        # TODO отдельный проход по стр-ре: попытка уменьшить кол-во точек за счет слияния соседних (релаксация аппроксиматора)

    def get_result_scene(self):
        return self.scene

    def make_grow(self, start_index, nsteps):
        self.step(start_index)
        for i in range(1, nsteps):
            self.step()

    def step(self, index_max_err=None):
        # находим пик ошибки на кущей сцене (там точки быть не может)
        if index_max_err is None:
            index_max_err = self.scene.get_err_max_index()

        # ставим туда точку
        current_point_name = self.scene.add_point(index_max_err)

        # находим область ограничения поиска
        x_max, x_min = self.get_restriction(index_max_err)


        #  в этой обл. находим индексы-кандидаты
        indexes = self._select_indexes_candidates(x_max, x_min, index_max_err)

        # для каждого кандидата делаем слепок сцены с добавленнымс сегментом и замеряем err
        # выбираем победителя
        self._get_winner_candidate(indexes, current_point_name)


    def get_restriction(self, index):
        x_min_point = self.scene.get_left_nearest_point(index)
        x_max_point = self.scene.get_right_nearest_point(index)

        if x_min_point is None:
            x_min = 0
        else:
            x_min = x_min_point.get_coord()

        if x_max_point is None:
            x_max = self.scene.get_size() - 1
        else:
            x_max = x_max_point.get_coord()

        return x_max, x_min

    def _select_indexes_candidates(self, x_min, x_max, index_max_err):
        indexes_candidates=[ x_min, x_max, index_max_err]

        # экстремумы сигнала
        coords_of_extrms = self.scene.get_extrms_in_interval(x_min, x_max)
        indexes_candidates = indexes_candidates + coords_of_extrms

        return indexes_candidates


    def _get_winner_candidate(self, index_candidates, current_point_name):

        errs = []
        for index_candidate in index_candidates:
            scene = deepcopy(self.scene)
            name_in_index = scene.get_or_create_point(index_candidate)
            scene.add_parent(child_name=name_in_index, parent_name=current_point_name)
            err = scene.get_err_sum()
            errs.append(err)

        best_i = errs.index(min(errs))

        best_index = index_candidates[best_i]

        name_in_index = self.scene.get_or_create_point(best_index)
        self.scene.add_parent(child_name=name_in_index, parent_name=current_point_name)






if __name__ == '__main__':
    log = HtmlLogger("grower_TEST")

    signal = get_mini_ECG()
    scene = Scene(signal)

    grower = Grower(scene)

    # логгер шагов роста: каждый шаг в хтмл (визуальная отладка)
    for i in range(10):

        grower.step()
        fig, axs = plt.subplots()
        grower.scene.draw(axs)
        log.add_text("ШАГ: "+ str(i))
        log.add_fig(fig)


