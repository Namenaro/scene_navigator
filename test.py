from GROW import FullGrow

from utils import HtmlLogger, get_mini_ECG

import matplotlib.pyplot as plt


def grow_etalon_scene(signal):
    log = HtmlLogger("FULL_grower_TEST")
    grower = FullGrow(signal)

    # логгер шагов роста: каждый шаг в хтмл (визуальная отладка)
    for i in range(8):
        grower.step()
        fig, axs = plt.subplots()
        grower.scene.draw(axs)
        log.add_text("ШАГ: " + str(i))
        log.add_fig(fig)

    return grower.get_scene()


if __name__ == '__main__':
    train_signal = get_mini_ECG()

    # ВЫРАЩИВАНИЕ НЕРЕЛАКСИРОВАННОЙ ЭТАЛОННОЙ СЦЕНЫ И ПРОГРАММЫ
    etalon_scene = grow_etalon_scene(train_signal)

    # запускаем RECOGNISER на эталонном сигнале(на котором шло обучение). В реализации-победителе точки
    # должны расставиться как на эталоннной сцене




