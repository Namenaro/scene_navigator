from utils import InterpolationSegment, Distr, get_distr_of_min_statistics

import numpy as np


class MeasurerWUnnormed: # не получает ни самого сигнала, ни предсказания
    def __init__(self, u_err, v_errs_on_segment, bassin_vs):
        self.u_err = u_err
        self.v_errs_on_segment = v_errs_on_segment
        self.bassin_vs = bassin_vs

    def get_p_of_so_good_rescription(self):
        # ШАГ БЕЗ УЧЕТА U_ERR:
        # без возвращения выбираем два значния (b и c) из бассейна + segment_len штук др. значений
        # по значениям b, c строим интерполяцию (длиной в накрытый по факту сегмент) над "случайно построенным" сегментом
        # замеряем ошибку этого случайного интерполятора над этим случаным сегментом и складываем в контейнер ERRS

        sample_ERRS = self._fill_sample_of_errs_of_random_decriptions()
        distr_ERRs = Distr(sample_ERRS)

        # УЧЕТ U_ERR:
        # отвечаем на вопрос: если посзолить себе u_err штук попыток "так хорошо" интерполяировать, и взять
        # лучший рез-т из этих попыток, то такова вероятность, что он будет хуже данного?

        distr_of_mins = get_distr_of_min_statistics(distr_ERRs, self.u_err)
        w = 1 - distr_of_mins.get_p_of_event(0, sum(self.v_errs_on_segment))
        return w

    def _fill_sample_of_errs_of_random_decriptions(self):
        sample = []
        N = 50
        for _ in range(0, N):
            segment_len = len(self.v_errs_on_segment)
            random_vs = np.random.choice(self.bassin_vs, segment_len + 2, replace=False)
            val1 = random_vs[0]
            val2 = random_vs[1]
            random_segment_vs = random_vs[2:]

            interpolator = InterpolationSegment(coord1=0, val1=val1, coord2=len(random_segment_vs)-1, val2=val2)
            vals_predicted = interpolator.get_vals_from_left()

            errs_sum = 0
            for i in range(len(vals_predicted)):
                abs_err_in_index = abs(random_segment_vs[i] - vals_predicted[i])
                errs_sum += abs_err_in_index
            sample.append(errs_sum)
        return sample



