class ExtremumFinder:
    def __init__(self, signal):
        self.signal = signal

        self.extremums_coords = []

        for index in range(len(self.signal)):
            if self._is_coord_extremum(index):
                self.extremums_coords.append(index)

    def get_coords_extremums(self):
        return self.extremums_coords

    ######################################################
    def _is_coord_extremum(self, coord):
        val = self.signal[coord]

        r_index = coord + 1
        l_index = coord - 1

        if l_index<0:
            lval = None
        else:
            lval = self.signal[l_index]

        if r_index>=len(self.signal):
           rval = None
        else:
            rval = self.signal[r_index]

        res = self.is_max(lval, val, rval) or self.is_min(lval, val, rval) or self.is_plato(lval, val, rval)
        return res


    def is_min(self,lval, val, rval):
        min_than_left = True
        if lval is not None:
            if lval < val:
                min_than_left = False
        min_than_r = True
        if rval is not None:
            if rval < val:
                min_than_r = False
        return min_than_left and min_than_r

    def is_max(self, lval, val, rval):
        max_than_left = True
        if lval is not None:
            if lval > val:
                max_than_left = False
        max_than_r = True
        if rval is not None:
            if rval > val:
                max_than_r = False
        return max_than_left and max_than_r

    def is_plato(self, lval, val, rval):
        pl_left = True
        if lval is not None:
            if lval != val:
                pl_left = False

        pl_right = True
        if rval is not None:
            if rval != val:
                pl_right = False

        return pl_right and pl_left


