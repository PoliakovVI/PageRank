import time
import random

methods_run_information = {
    "iterations": {},
    "spent time": {}
}

numbers_after_point = 30


class Timer:
    _run_info_dict = None
    _start_time = None
    _name = None

    def __init__(self, run_info_dict):
        self._run_info_dict = run_info_dict
        return

    def start(self, name):
        self._name = name
        self._start_time = time.time()
        return

    def end(self):
        end_time = time.time()
        self._run_info_dict[self._name] = end_time - self._start_time
        return


__Timer = Timer(methods_run_information["spent time"])


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


def MarkovChain(tpmatrix, precision=0.001, probability_start_stat_vector=None):
    __Timer.start("MarkovChain")
    pages_number = tpmatrix._pages_number
    if probability_start_stat_vector is None:
        previous_stat_vector = [1 / pages_number for i in range(pages_number)]
    else:
        if abs(sum(probability_start_stat_vector) - 1) > 0.0001:
            raise Exception("Wrong parameter 'probability_start_stat_vector': sum does not equal ot 1")

        previous_stat_vector = probability_start_stat_vector

    iteration = 0
    while True:
        iteration += 1
        new_stat_vector = _vectorSquareMatrixMultiplication(previous_stat_vector,
                                                            tpmatrix._matrix)
        if _calculateComponentsDistance(previous_stat_vector, new_stat_vector) < precision:
            break

        previous_stat_vector = new_stat_vector

    __Timer.end()

    methods_run_information['iterations']['MarkovChain'] = iteration
    return new_stat_vector


def PowerMethod(tmatrix, precision=0.001, d=0.85, start_weight_vector=None):
    __Timer.start("PowerMethod")

    pages_number = tmatrix._pages_number
    if start_weight_vector is None:
        previous_stat_vector = [1 for i in range(pages_number)]
    else:
        previous_stat_vector = start_weight_vector

    new_stat_vector = previous_stat_vector[:]

    iteration = 0
    while True:
        iteration += 1
        for page_num in range(pages_number):
            sum_weight = 0
            for linking_page in range(pages_number):
                if abs(tmatrix._matrix[linking_page][page_num] - 1.) < 0.0001:
                    sum_weight += previous_stat_vector[linking_page] / tmatrix._links_numbers[linking_page]

            new_stat_vector[page_num] = (1 - d) + d * (sum_weight)
        dist = _calculateComponentsDistance(previous_stat_vector, new_stat_vector)
        if dist < precision:
            break

        previous_stat_vector = new_stat_vector[:]

    __Timer.end()

    methods_run_information['iterations']['PowerMethod'] = iteration
    return new_stat_vector


def _compute_pi_vector(vectors_stack):
    pik2 = vectors_stack.pop()
    pik1 = vectors_stack.pop()
    pik0 = vectors_stack.pop()
    length = len(pik0)
    pi_vector = []
    vectors_stack = []

    for i in range(length):
        top = (pik1[i] - pik0[i]) ** 2
        bot = pik2[i] - 2 * pik1[i] - pik0[i]
        pi_vector.append(pik2[i] - top / bot)

    return pi_vector


def AdaptivePowerMethod(tmatrix, precision=0.001, d=0.85, start_weight_vector=None, extrapolation=False, period=10):
    addition_name = ""
    if extrapolation:
        addition_name = "Extrapolating"

    __Timer.start(addition_name + "AdaptivePowerMethod")

    pages_number = tmatrix._pages_number
    if start_weight_vector is None:
        previous_stat_vector = [1 for i in range(pages_number)]
    else:
        previous_stat_vector = start_weight_vector

    number_of_counted = pages_number
    need_to_recount_pages = [True for i in range(pages_number)]

    new_stat_vector = previous_stat_vector[:]

    if extrapolation:
        stat_vectors_stack = []
        stat_vectors_stack.append(previous_stat_vector)

    iteration = 0
    while True:
        iteration += 1
        for page_num in range(pages_number):
            if not need_to_recount_pages[page_num]:
                continue

            sum_weight = 0
            for linking_page in range(pages_number):
                if abs(tmatrix._matrix[linking_page][page_num] - 1.) < 0.0001:
                    sum_weight += previous_stat_vector[linking_page] / tmatrix._links_numbers[linking_page]

            new_stat_vector[page_num] = (1 - d) + d * (sum_weight)

        if extrapolation:
            stat_vectors_stack.append(previous_stat_vector)
            if iteration % period == 0:
                new_stat_vector = _compute_pi_vector(stat_vectors_stack)

        for page_num in range(pages_number):
            if abs(new_stat_vector[page_num] - previous_stat_vector[page_num]) < precision and \
                    need_to_recount_pages[page_num]:
                need_to_recount_pages[page_num] = False
                number_of_counted -= 1

        if number_of_counted == 0:
            break

        previous_stat_vector = new_stat_vector[:]

    __Timer.end()

    methods_run_information['iterations'][addition_name + 'AdaptivePowerMethod'] = iteration
    return new_stat_vector


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


def EndpointRandomStartMonteCarloMethod(tlist, d=0.85, order="square", iterations=1):
    pages_number = tlist._pages_number
    if order == "linear":
        N = pages_number
    elif order == "square":
        N = pages_number ** 2
    else:
        raise ValueError("Wrong order parameter")

    __Timer.start("EndpointRandomStartMonteCarloMethod:" + order)

    stat_vector = [0 for i in range(pages_number)]

    for i in range(N * iterations):
        start_page = random.randint(0, pages_number - 1)
        stat_vector[_simulate_run(tlist, start_page, d)] += 1

    __Timer.end()

    methods_run_information['iterations']['EndpointRandomStartMonteCarloMethod:' + order] = iterations
    return stat_vector


def EndpointCyclicStartMonteCarloMethod(tlist, d=0.85, iterations=5):
    pages_number = tlist._pages_number

    __Timer.start("EndpointCyclicStartMonteCarloMethod")

    stat_vector = [0 for i in range(pages_number)]

    for page_number in range(pages_number):
        for iter in range(iterations):
            stat_vector[_simulate_run(tlist, page_number, d)] += 1

    __Timer.end()
    methods_run_information['iterations']['EndpointCyclicStartMonteCarloMethod'] = iterations
    return stat_vector


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


def CompletePathMonteCarloMethod(tlist, d=0.85, iterations=5):
    pages_number = tlist._pages_number

    __Timer.start("CompletePathMonteCarloMethod")

    stat_vector = [0 for i in range(pages_number)]

    for page_number in range(pages_number):
        for iter in range(iterations):
            _simulate_complete_run(tlist, stat_vector, page_number, d)

    __Timer.end()
    methods_run_information['iterations']['CompletePathMonteCarloMethod'] = iterations
    return stat_vector


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


def StoppingCompletePathMonteCarloMethod(tlist, d=0.85, iterations=5):
    pages_number = tlist._pages_number

    __Timer.start("StoppingCompletePathMonteCarloMethod")

    stat_vector = [0 for i in range(pages_number)]

    for page_number in range(pages_number):
        for iter in range(iterations):
            _stopping_simulate_complete_run(tlist, stat_vector, page_number, d)

    __Timer.end()
    methods_run_information['iterations']['StoppingCompletePathMonteCarloMethod'] = iterations
    return stat_vector


def RandomStartStoppingCompletePathMonteCarloMethod(tlist, d=0.85, order="square", iterations=1):
    pages_number = tlist._pages_number
    if order == "linear":
        N = pages_number
    elif order == "square":
        N = pages_number ** 2
    else:
        raise ValueError("Wrong order parameter")

    __Timer.start("RandomStartStoppingCompletePathMonteCarloMethod")

    stat_vector = [0 for i in range(pages_number)]

    for i in range(N * iterations):
        start_page = random.randint(0, pages_number - 1)
        _stopping_simulate_complete_run(tlist, stat_vector, start_page, d)

    __Timer.end()
    methods_run_information['iterations']['RandomStartStoppingCompletePathMonteCarloMethod'] = iterations
    return stat_vector
