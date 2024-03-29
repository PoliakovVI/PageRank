import copy


class TransitionMatrix:
    _precision = None
    _matrix = []
    _links_numbers = []
    _pages_number = None

    def __init__(self, precision=0.001):
        self._precision = precision

    def check_for_transition(self):
        height = len(self._matrix)

        for row in self._matrix:
            if len(self._matrix) != height:
                raise Exception("Length does not match")

        self._links_numbers = []
        page_number = 0
        for row in self._matrix:
            links_num = 0
            for item in row:
                links_num += item
            self._links_numbers.append(links_num)

            if links_num == 0:
                for j in range(0, page_number):
                    self._matrix[page_number][j] = 1.
                for j in range(page_number+1, height):
                    self._matrix[page_number][j] = 1.
                self._links_numbers[page_number] = height - 1


            page_number += 1

        self._pages_number = height
        return


    def read_from_txt(self, filename, sep=';'):
        self._matrix = []

        with open(filename, "r") as file:
            for line in file:
                self._matrix.append(list(map(float, line.split(sep=sep))))

        self.check_for_transition()
        return

    def __str__(self):
        total_string = ""

        for row in self._matrix:
            total_string += "[ "
            for item in row:
                total_string += str(item) + " "
            total_string += "]\n"

        return total_string

    def __len__(self):
        return len(self._matrix)


class TransitionProbabilityMatrix:
    _matrix = None
    _pages_number = None
    _d = None

    def __init__(self, tmatrix, d=0.85):
        self._d = d
        self._matrix = copy.deepcopy(tmatrix._matrix)
        self._pages_number = tmatrix._pages_number

        for i in range(self._pages_number):
            self._matrix[i][i] = d
            link_number = 0
            for j in range(0, i):
                link_number += self._matrix[i][j]
            for j in range(i+1, self._pages_number):
                link_number += self._matrix[i][j]

            if link_number == 0:
                number = (1 - d) / (self._pages_number - 1)
                for j in range(0, i):
                    self._matrix[i][j] = number
                for j in range(i+1, self._pages_number):
                    self._matrix[i][j] = number
            else:
                number = (1 - d) / link_number
                for j in range(0, i):
                    if self._matrix[i][j] == 1:
                        self._matrix[i][j] = number
                for j in range(i+1, self._pages_number):
                    if self._matrix[i][j] == 1:
                        self._matrix[i][j] = number

        return

    def __len__(self):
        return len(self._matrix)

    def __str__(self):
        total_string = ""

        for row in self._matrix:
            total_string += "[ "
            for item in row:
                total_string += str(item) + " "
            total_string += "]\n"

        return total_string


class TransitionList:
    _tlist = []
    _pages_number = None

    def __init__(self, tmatrix):
        matrix = tmatrix._matrix
        self._pages_number = tmatrix._pages_number
        self._tlist = [[] for i in range(self._pages_number)]

        for i in range(self._pages_number):
            for j in range(self._pages_number):
                if abs(matrix[i][j] - 1.) < 0.001:
                    self._tlist[i].append(j)
        return

    def __str__(self):
        return self._tlist.__str__()

    def __len__(self):
        return len(self._tlist)
