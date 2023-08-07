from scene import Scene
from utils import get_mini_ECG, HtmlLogger


import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from copy import deepcopy


# АЛГОРИТМ: два этажа соревнования:
# 1) из какого максимума ошибки расти (соревнование максимумов ошибки)  ---> отбор итога по W
# 2) куда расти из конкретноко максимума  ---> соревнование по w_step

# Соревнование [1]: чтобы обработать случай "ступеньки"(зашумленного плато), стоит выбирать максимумы по устойчивости w к джиттеру u.
#        Сортируем
# Соревнование [2][внутренний цикл соревнования_1]:
# для данного максимума ошибки определяем ограничители бассейна (слева, справа)
#    если расстояние до них ноль, то сегмент не наращивается едиснтвенным образом без соревнования (просто он состоит из 1 точки)
#    иначе внутри  бассейна берем все экстремумы и гриничные точки бассейна - это кандиадты на встраивание в сегмент
# ЗАМЕЧАНИЕ_1: ведем соревнование либо по Err (просто сичтаем ошибку измененного предсказания), либо по w сегмента
# (однако, в w участвует err, так что он в любом случае будет учтен). Второе, вероятно, предпочтительнее,
# потому что, кажется, w- это генеральный способ учесть err.
# ЗАМЕЧАНИЕ_2: в соревновании 2, возможно, стоит расть на m сегментов вперед по минимизации Err


# --------------
# Рабочий план:
# Сначала реализуем Соревнование 2 при заданном кол-ве шагов: с выбором бассейна, в котором определяются точки/индексы кандидаты, пока что с Errr.
# Gосле этого реализуем w (т.к. генератор сцен уже есть, а тестировать работу  w надо на "боевых" сценах, т.к. бассейны меняются)
# Класс сцены доработать так, чтобб получать выборки для расчета w предсказания (вероятно, то, что уже накрыто сегментами, надо убирать из выборки,
# на которой расчитвыается w). Протестить джиттер w.
# ЗАМЕЧАНИЕ: при  придсказании внутри  сегмента наш сигнал это отклонение от интерполяционной линии??? Или предсказывать абсолютно?


class Grower:
    def __init__(self, signal):
        self.scene = Scene(signal)

    def step(self):
        # находим пик ошибки на кущей сцене
        index_max_err = self.scene.get_err_max_index()

        # если там есть точка, то назначаем рабочей ее. Иначе -стаивм новую

        current_point_name = self._select_current_point()

        # для текущей рабочей точки определеяем горизонт ее действия
        #  этом горизонтке находим индексы-кандидаты
        indexes = self._select_indexes_candidates()

        # для каждого кандидата делаем слепок сцены с добавленнымс сегментом и замеряем q
        # выбираем победителя
        self._get_winner_candidate(indexes, current_point_name)



    def _select_indexes_candidates(self):
        indexes_candidates=[]

        # TODO пока будем проверять избыточное кол-во кандидатов:

        # Первый пул: точки-кандидаты
        coords_of_points = self.scene.get_points_coords()
        indexes_candidates = indexes_candidates + coords_of_points

        # Второй пул: экстремумы сигнала
        coords_of_extrms = self.scene.get_all_extemums_of_signal()
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

    grower = Grower(signal)

    # логгер шагов роста: каждый шаг в хтмл (визуальная отладка)
    for i in range(10):

        grower.step()
        fig, axs = plt.subplots()
        grower.scene.draw(axs)
        log.add_text("ШАГ: "+ str(i))
        log.add_fig(fig)


