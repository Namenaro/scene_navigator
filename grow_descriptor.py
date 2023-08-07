from scene import Scene
from utils import get_mini_ECG


import matplotlib.pyplot as plt
from matplotlib.pyplot import text


class Grower:
    def __init__(self, signal):
        self.scene = Scene(signal)

    def step(self):
        # находим пик ошибки на кущей сцене
        # если там есть точка, то назначаем рабочей ее. Иначе -стаивм новую
        current_point_name = self._select_current_point()

        # для текущей рабочей точки определеяем горизонт ее действия
        #  этом горизонтке находим индексы-кандидаты
        indexes = self._select_indexes_candidates()

        # для каждого кандидата делаем слепок сцены с добавленнымс сегментом и замеряем q
        scene_winner = self._get_winner_candidate(indexes)

        # выбираем победителя и заменяем текущую сцену на него
        self.scene = scene_winner

    def _select_current_point(self):
        index_max_err = self.scene.get_err_max_index()
        name_in_index = self.scene.get_name_by_index(index_max_err)
        if name_in_index is not None:
            return name_in_index
        new_point_name = self.scene.add_point(index_max_err)
        return new_point_name

    def _select_indexes_candidates(self):
        return indexes

    def _get_winner_candidate(self, index_candidates):
        return scene_winner




if __name__ == '__main__':
    signal = get_mini_ECG()


    grower = Grower(signal)

    # логгер шагов роста: каждый шаг в хтмл (визуальная отладка)
    for i in range(4):
        grower.step()
        fig, axs = plt.subplots()
        grower.scene.draw(axs)

        plt.show()
