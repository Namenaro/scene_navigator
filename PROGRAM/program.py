from .prediction import Prediction, ParentInfo, Restriction


class Program:
    def __init__(self):
        self.names_to_predictions = {}  # name: Prediction

    def add_point_info(self, point_name, prediction):
        self.names_to_predictions[point_name] = prediction

    def get_parent_name_for_child_name(self, child_name):
        return self.names_to_predictions[child_name].get_parent_name()

    def get_predicted_val_for_name(self, name):
        return self.names_to_predictions[name].get_val()




