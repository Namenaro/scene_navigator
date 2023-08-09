from grow_nsteps_simple import Grower
from utils import HtmlLogger, get_mini_ECG
from scene import Scene


import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from copy import deepcopy

class FullGrow:
    def __init__(self, signal):
        self.scene = Scene(signal)

    def step(self):
        # выбираем максимумы ошибки
        indexes = self.scene.get_all_maxes_of_err()

        # проращиваем их каждый roll forward на маленькое кол-во шагов в отдельных экземплярах сцены

        best_scene = self.scene
        min_err = self.scene.get_err_sum()
        for index in indexes:
            grower = Grower(self.scene)
            grower.make_grow(index, nsteps=2)
            res_scene = grower.get_result_scene()
            err_in_scene = res_scene.get_err_sum()
            if err_in_scene < min_err:
                min_err = err_in_scene
                best_scene = res_scene

        # сцену победитель  делаем ее текущей
        self.scene = best_scene


if __name__ == '__main__':
    log = HtmlLogger("FULL_grower_TEST")

    signal = get_mini_ECG()

    grower = FullGrow(signal)

    # логгер шагов роста: каждый шаг в хтмл (визуальная отладка)
    for i in range(8):

        grower.step()
        fig, axs = plt.subplots()
        grower.scene.draw(axs)
        log.add_text("ШАГ: "+ str(i))
        log.add_fig(fig)
