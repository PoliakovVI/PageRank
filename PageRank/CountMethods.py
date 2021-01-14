numbers_after_point = 30


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


def MarkovChain(tpmatrix, precision=0.001):
    pages_number = tpmatrix._number_of_pages
    previous_stat_vector= [1 / pages_number for i in range(pages_number)]

    while True:
        new_stat_vector = _vectorSquareMatrixMultiplication(previous_stat_vector,
                                                            tpmatrix._matrix)
        if _calculateComponentsDistance(previous_stat_vector, new_stat_vector) < precision:
            break

        previous_stat_vector = new_stat_vector

    return new_stat_vector


def PowerMethod(tmatrix, precision=0.001, d=0.85):
    pages_number = tmatrix._number_of_pages
    previous_stat_vector = [1 for i in range(pages_number)]
    new_stat_vector = previous_stat_vector[:]

    iter = 0
    while True:
        iter += 1
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
    print("iterations:", iter)
    return new_stat_vector
