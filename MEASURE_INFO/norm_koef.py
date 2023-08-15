from utils import get_mini_ECG

max_physical_val = max(get_mini_ECG())


def get_profit_koef_of_prediction(err_of_old_description, err_after_update_description):
    return (err_of_old_description - err_after_update_description)/max_physical_val
