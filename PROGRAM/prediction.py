
class Restriction:
    def __init__(self, left_point, right_point):
        self.left_point = left_point
        self.right_point = right_point


class ParentInfo:
    def __init__(self, parent_name, u):
        self.parent_name = parent_name  # если точка первая, то родителя нет
        self.u = u

class Prediction:
    def __init__(self,  parent_info, restriction, val):
        self.parent_info = parent_info
        self.restriction = restriction
        self.val = val

    def get_parent_name(self):
        return self.parent_info.parent_name

    def get_val(self):
        return self.val

