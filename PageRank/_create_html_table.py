EXAMPLE = [
    ["stream", "perfomance", "#<", "Company"],
    ["#^"    , "#^"       , "#<" , "Huawei"],
    ["#^"    , "456"       , "8" , "Intel"],
    ["#^"    , "678"       , "1" , "Nitel"],
]


class Cell:
    _value = ""
    _rowspan = 1
    _colspan = 1

    _is_left_joined = False
    _is_top_joined = False

    def __str__(self):
        return "(" + str(self._rowspan) + ", " + str(self._colspan) + ", " + \
               str(self._is_left_joined) + ", " + str(self._is_top_joined) + ", " + ")"

    def setValue(self, value):
        self._value = value

    def makeLeftJoined(self):
        self._is_left_joined = True

    def makeTopJoined(self):
        self._is_top_joined = True

    def joinNextRow(self):
        self._rowspan += 1

    def joinNextColumn(self):
        self._colspan += 1

    def gethtml(self):
        if self._is_left_joined or self._is_top_joined:
            return None

        html = "        <td"
        if self._rowspan != 1:
            html += ' rowspan="{}"'.format(self._rowspan)

        if self._colspan != 1:
            html += ' colspan="{}"'.format(self._colspan)
        html += ">" + str(self._value) + "</td>"
        return html


class Table:
    _grid = []
    _height = None
    _width = 0

    def __init__(self, matrix):
        self._height = len(matrix)
        if self._height == 0:
            raise Exception("Error: matrix height cant be 0!")

        self._width = len(matrix[0])
        if self._width == 0:
            raise Exception("Error: matrix height cant be 0!")

        for i in range(self._height):
            self._grid.append([])
            for j in range(self._width):
                cell = Cell()
                self._grid[i].append(cell)

                matrix_cell = str(matrix[i][j]).split(sep="#")
                cell.setValue(matrix_cell[0])

                if len(matrix_cell) == 1:
                    continue

                if len(matrix_cell) > 2:
                    raise Exception('Error: too much "#" in cell')

                keys = matrix_cell[1]

                for key in keys:
                    if key == "^":
                        cell.makeTopJoined()
                        self._increase_rowspan(i, j)
                        break

                    if key == "<":
                        cell.makeLeftJoined()
                        self._increase_colspan(i, j)
                        break

    def _increase_rowspan(self, ii, j):
        i = ii
        while self._grid[i][j]._is_top_joined:
            i -= 1
            if i < 0:
                raise Exception('Error: "^" cant refer to nothing')
        self._grid[i][j].joinNextRow()
        return

    def _increase_colspan(self, i, jj):
        j = jj
        while self._grid[i][j]._is_left_joined:
            j -= 1
            if j < 0:
                raise Exception('Error: "<" cant refer to nothing')
        self._grid[i][j].joinNextColumn()
        return

    def writeHtml(self, filename):
        html_code = '<table border="2", cellpadding="10">\n'

        for row in self._grid:
            html_code += '    <tr>\n'
            for cell in row:
                if cell._is_top_joined or cell._is_left_joined:
                    continue

                html_code += cell.gethtml() + '\n'

            html_code += '    </tr>\n'
        html_code += '</table>\n'


        with open(filename, "w") as fout:
            fout.write(html_code)
