import time
import random

methods_run_information = {
    "iterations": {},
    "spent time": {}
}

numbers_after_point = 30


class Timer:
    def start(self):
        self._start_time = time.time()
        return

    def finish(self):
        end_time = time.time()
        return end_time - self._start_time


def _toFixed(number, digits=0):
    return int(number * (10 ** digits)) / (10 ** digits)


def _vectorSquareMatrixMultiplication(V1, M2):
    size = len(V1)
    M_result = [0 for i in range(size)]

    for i in range(size):
        sum = 0
        for k in range(size):
            sum += V1[k] * M2[k][i]
        M_result[i] = float(_toFixed(sum, numbers_after_point))
    return M_result


def _calculateComponentsDistance(v1, v2):
    if len(v1) != len(v2):
        raise Exception("Different length of vectors")

    dist = 0

    for i in range(len(v1)):
        dif = _toFixed(v1[i] - v2[i], numbers_after_point) ** 2
        dist += dif
    return dist ** 0.5


class MarkovChain:
    _timer = Timer()
    _iterating_run_time = None
    _stopping_run_time = None
    _stat_vector = None

    def __init__(self, tpmatrix, probability_start_stat_vector=None):
        self._d = tpmatrix._d
        pages_number = len(tpmatrix)
        self._matrix = tpmatrix
        if probability_start_stat_vector is None:
            self._stat_vector = [1 / pages_number for i in range(pages_number)]
        else:
            accuracy = 0.0001
            if abs(sum(probability_start_stat_vector) - 1) > accuracy:
                raise Exception("Wrong parameter 'probability_start_stat_vector': "
                                "sum does not equal ot 1. acc: {}".format(accuracy))

            self._stat_vector = probability_start_stat_vector
        return

    def _iteration(self):
        self._old_stat_vector = self._stat_vector
        self._stat_vector = _vectorSquareMatrixMultiplication(self._stat_vector,
                                                            self._matrix._matrix)
        return

    def iterating_run(self, iterations):
        self._timer.start()
        for i in range(iterations):
            self._iteration()
        self._srun_iteraions = iterations
        self._iterating_run_time = self._timer.finish()
        return

    def stopping_run(self, precision=0.01):
        self._timer.start()
        self._srun_iteraions = 0
        while True:
            self._iteration()
            self._srun_iteraions += 1
            if _calculateComponentsDistance(self._stat_vector, self._old_stat_vector) < precision:
                break
        self._stopping_run_time = self._timer.finish()
        return


class PowerMethod:
    _timer = Timer()
    _iterating_run_time = None
    _stopping_run_time = None
    _stat_vector = None

    def __init__(self, tmatrix, start_stat_vector=None, d=0.85):
        pages_number = len(tmatrix)
        self._matrix = tmatrix
        self._d = d
        if start_stat_vector is None:
            self._stat_vector = [1 for i in range(pages_number)]
        else:
            self._stat_vector = start_stat_vector
        return

    def _iteration(self):
        self._old_stat_vector = self._stat_vector[:]
        pages_number = len(self._matrix)
        for page_num in range(pages_number):
            sum_weight = 0
            for linking_page in range(pages_number):
                if abs(self._matrix._matrix[linking_page][page_num] - 1.) < 0.0001:
                    sum_weight += self._old_stat_vector[linking_page] / \
                                  self._matrix._links_numbers[linking_page]

            self._stat_vector[page_num] = (1 - self._d) + self._d * (sum_weight)
        return

    def iterating_run(self, iterations):
        self._timer.start()
        for i in range(iterations):
            self._iteration()
        self._srun_iteraions = iterations
        self._iterating_run_time = self._timer.finish()
        return

    def stopping_run(self, precision=0.01):
        self._timer.start()
        self._srun_iteraions = 0
        while True:
            self._iteration()
            self._srun_iteraions += 1
            if _calculateComponentsDistance(self._stat_vector, self._old_stat_vector) < precision:
                break
        self._stopping_run_time = self._timer.finish()
        return


def _compute_pi_vector(vectors_stack):
    pik2 = vectors_stack.pop()
    pik1 = vectors_stack.pop()
    pik0 = vectors_stack.pop()
    length = len(pik0)
    pi_vector = []
    vectors_stack = []

    for i in range(length):
        try:
            top = (pik1[i] - pik0[i]) ** 2
            bot = pik2[i] - 2 * pik1[i] - pik0[i]
            pi_vector.append(pik0[i] - top / bot)
        except ZeroDivisionError:
            pi_vector = pik2
            break

    return pi_vector


class AdaptivePowerMethod:
    _timer = Timer()
    _iterating_run_time = None
    _stopping_run_time = None
    _stat_vector = None
    _stat_vectors_stack = []

    def __init__(self, tmatrix, start_stat_vector=None, d=0.85):
        pages_number = len(tmatrix)
        self._need_to_recount_pages = [True for i in range(pages_number)]
        self._matrix = tmatrix
        self._need_to_recount_pages_number = len(self._matrix)
        self._d = d
        if start_stat_vector is None:
            self._stat_vector = [1 for i in range(pages_number)]
        else:
            self._stat_vector = start_stat_vector
        return

    def _iteration(self, with_extrapolation=False):
        pages_number = len(self._matrix)
        self._old_stat_vector = self._stat_vector[:]

        for page_num in range(pages_number):
            if not self._need_to_recount_pages[page_num]:
                continue

            sum_weight = 0
            for linking_page in range(pages_number):
                if abs(self._matrix._matrix[linking_page][page_num] - 1.) < 0.0001:
                    sum_weight += self._old_stat_vector[linking_page] / \
                                  self._matrix._links_numbers[linking_page]

            self._stat_vector[page_num] = (1 - self._d) + self._d * (sum_weight)

        self._stat_vectors_stack.append(self._old_stat_vector)
        if with_extrapolation:
            new_stat_vector = _compute_pi_vector(self._stat_vectors_stack)
        return

    def iterating_run(self, iterations, extrapolation_period=None):
        self._timer.start()

        need_extrapolation = False
        if extrapolation_period is not None:
            need_extrapolation = True
            if extrapolation_period < 3:
                raise Exception("extrapolation_period cant be less then 3")

        for i in range(iterations):
            if need_extrapolation and i % extrapolation_period == 0:
                self._iteration(with_extrapolation=True)
                continue
            self._iteration()

        self._srun_iteraions = iterations
        self._iterating_run_time = self._timer.finish()
        return

    def stopping_run(self, precision=0.01, extrapolation_period=None):
        self._timer.start()

        need_extrapolation = False
        if extrapolation_period is not None:
            need_extrapolation = True
            if extrapolation_period < 3:
                raise Exception("extrapolation_period cant be less then 3")

        self._srun_iteraions = 0
        while True:
            if need_extrapolation and (self._srun_iteraions + 1) % extrapolation_period == 0:
                self._iteration(with_extrapolation=True)
            else:
                self._iteration()

            self._srun_iteraions += 1

            for page_num in range(len(self._matrix)):
                if abs(self._stat_vector[page_num] - self._old_stat_vector[page_num]) < precision and \
                        self._need_to_recount_pages[page_num]:
                    self._need_to_recount_pages[page_num] = False
                    self._need_to_recount_pages_number -= 1

            if self._need_to_recount_pages_number == 0:
                break

        self._stopping_run_time = self._timer.finish()

        self._need_to_recount_pages_number = len(self._matrix)
        self._need_to_recount_pages = [True for i in range(len(self._matrix))]
        return


class ExtrapolatingAdaptivePowerMethod:
    _iterating_run_time = None
    _stopping_run_time = None
    _stat_vector = None

    def __init__(self, tmatrix, start_stat_vector=None, d=0.85):
        self._APmethod = AdaptivePowerMethod(tmatrix, start_stat_vector, d)
        return

    def _iteration(self, with_extrapolation=False):
        raise Exception("Cant be used for that: ExtrapolatingAdaptivePowerMethod")
        return

    def iterating_run(self, iterations, extrapolation_period=10):
        self._APmethod.iterating_run(iterations, extrapolation_period)
        self._iterating_run_time = self._APmethod._iterating_run_time
        self._stat_vector = self._APmethod._stat_vector
        return

    def stopping_run(self, precision=0.01, extrapolation_period=10):
        self._APmethod.stopping_run(precision, extrapolation_period)
        self._stopping_run_time = self._APmethod._stopping_run_time
        self._stat_vector = self._APmethod._stat_vector
        return


# Monte Carlo methods


def _simulate_run(tlist, start_page, d, precision=100):
    lst = tlist._tlist
    current_page = start_page

    while True:
        if random.randint(0, precision) / precision > d:
            # terminating run
            return current_page
        else:
            current_page = lst[current_page][random.randint(0, len(lst[current_page]) - 1)]

    return


class EndpointRandomStartMonteCarloMethod:
    _timer = Timer()
    _iterating_run_time = None
    _stopping_run_time = None
    _stat_vector = None

    def __init__(self, tlist, d=0.85):
        self._d = d
        pages_number = len(tlist)
        self._matrix = tlist
        self._stat_vector = [0 for i in range(pages_number)]
        return

    def _iteration(self):
        pages_number = len(self._matrix)
        for i in range(self._N):
            start_page = random.randint(0, pages_number - 1)
            self._stat_vector[_simulate_run(self._matrix, start_page, self._d)] += 1
        return

    def iterating_run(self, iterations, order="linear"):
        pages_number = len(self._matrix)
        if order == "linear":
            self._N = pages_number
        elif order == "square":
            self._N = pages_number ** 2
        else:
            raise ValueError("Wrong order parameter")

        self._timer.start()
        for i in range(iterations):
            self._iteration()
        self._srun_iteraions = iterations
        self._iterating_run_time = self._timer.finish()
        return

    def stopping_run(self, precision=0.01, order="linear"):
        raise Exception("No available implementation")
        return


class EndpointCyclicStartMonteCarloMethod:
    _timer = Timer()
    _iterating_run_time = None
    _stopping_run_time = None
    _stat_vector = None

    def __init__(self, tlist, d=0.85):
        self._d = d
        pages_number = len(tlist)
        self._matrix = tlist
        self._stat_vector = [0 for i in range(pages_number)]
        return

    def _iteration(self):
        pages_number = len(self._matrix)
        for page_number in range(pages_number):
            for iter in range(self._m):
                self._stat_vector[_simulate_run(self._matrix, page_number, self._d)] += 1
        return

    def iterating_run(self, iterations, m=3):
        self._m = m
        self._timer.start()
        for i in range(iterations):
            self._iteration()
        self._srun_iteraions = iterations
        self._iterating_run_time = self._timer.finish()
        return

    def stopping_run(self, precision=0.01, m=3):
        raise Exception("No available implementation")
        return


def _simulate_complete_run(tlist, stat_vector, start_page, d, precision=100):
    lst = tlist._tlist
    current_page = start_page

    while True:
        stat_vector[current_page] += 1
        if random.randint(0, precision) / precision > d:
            # terminating run
            return
        else:
            current_page = lst[current_page][random.randint(0, len(lst[current_page]) - 1)]

    return


class CompletePathMonteCarloMethod:
    _timer = Timer()
    _iterating_run_time = None
    _stopping_run_time = None
    _stat_vector = None

    def __init__(self, tlist, d=0.85):
        self._d = d
        pages_number = len(tlist)
        self._matrix = tlist
        self._stat_vector = [0 for i in range(pages_number)]
        return

    def _iteration(self):
        pages_number = len(self._matrix)
        for page_number in range(pages_number):
            for iter in range(self._m):
                _simulate_complete_run(self._matrix, self._stat_vector, page_number, self._d)
        return

    def iterating_run(self, iterations, m=3):
        self._m = m
        self._timer.start()
        for i in range(iterations):
            self._iteration()
        self._srun_iteraions = iterations
        self._iterating_run_time = self._timer.finish()
        return

    def stopping_run(self, precision=0.01, m=3):
        raise Exception("No available implementation")
        return


def _stopping_simulate_complete_run(tlist, stat_vector, start_page, d, precision=100):
    lst = tlist._tlist
    current_page = start_page
    pages_number = tlist._pages_number

    while True:
        stat_vector[current_page] += 1
        if random.randint(0, precision) / precision > d or len(lst[current_page]) == pages_number - 1:
            # terminating run
            return
        else:
            current_page = lst[current_page][random.randint(0, len(lst[current_page]) - 1)]

    return


class StoppingCompletePathMonteCarloMethod:
    _timer = Timer()
    _iterating_run_time = None
    _stopping_run_time = None
    _stat_vector = None

    def __init__(self, tlist, d=0.85):
        self._d = d
        pages_number = len(tlist)
        self._matrix = tlist
        self._stat_vector = [0 for i in range(pages_number)]
        return

    def _iteration(self):
        pages_number = len(self._matrix)
        for page_number in range(pages_number):
            for iter in range(self._m):
                _stopping_simulate_complete_run(self._matrix, self._stat_vector, page_number, self._d)
        return

    def iterating_run(self, iterations, m=3):
        self._m = m
        self._timer.start()
        for i in range(iterations):
            self._iteration()
        self._srun_iteraions = iterations
        self._iterating_run_time = self._timer.finish()
        return

    def stopping_run(self, precision=0.01, m=3):
        raise Exception("No available implementation")
        return


class RandomStartStoppingCompletePathMonteCarloMethod:
    _timer = Timer()
    _iterating_run_time = None
    _stopping_run_time = None
    _stat_vector = None

    def __init__(self, tlist, d=0.85):
        self._d = d
        pages_number = len(tlist)
        self._matrix = tlist
        self._stat_vector = [0 for i in range(pages_number)]
        return

    def _iteration(self):
        pages_number = len(self._matrix)
        for i in range(self._N):
            start_page = random.randint(0, pages_number - 1)
            _stopping_simulate_complete_run(self._matrix, self._stat_vector, start_page, self._d)
        return

    def iterating_run(self, iterations, order="linear"):
        pages_number = len(self._matrix)
        if order == "linear":
            self._N = pages_number
        elif order == "square":
            self._N = pages_number ** 2
        else:
            raise ValueError("Wrong order parameter")

        self._timer.start()
        for i in range(iterations):
            self._iteration()
        self._srun_iteraions = iterations
        self._iterating_run_time = self._timer.finish()
        return

    def stopping_run(self, precision=0.01, order="linear"):
        raise Exception("No available implementation")
        return
