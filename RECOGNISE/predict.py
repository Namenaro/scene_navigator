from PROGRAM import Program, Prediction, ParentInfo
from SCENE import scene

# получаем контекстное предсказание (без проверки)

class PredictionInContext: #предсказанная кордната точки, предсказанное значение, левое и правое ограничение
    def __init__(self, name):
        self.predicted_coord = None
        self.preedicted_val = None
        self.left_resctiction = None
        self.right_rescriction = None
        self.name = name

    def fill(self, scene, program):
        # находим родителя и откладываем от него u
        # получаем координаты ограничений
        # подправляем u, если вылезло за ограничения

        pass


