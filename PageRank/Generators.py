import random


generators_information = {}

class _page:
    number = None
    outgoing_links = []
    rang = None
    _in_sum = 0
    in_links_num = 0

    def __init__(self, number, pages=[], d=0.85):
        self.number = number
        self.d = d
        self.outgoing_links = pages[:]
        self._in_sum = 0
        self.rang = 0
        self._recompute_rang()

    def _recompute_rang(self):
        self._old_rang = self.rang
        self.rang = 1 - self.d + self.d * self._in_sum
        links_number = len(self.outgoing_links)

        for page in self.outgoing_links:
            page.recompute_sum(self._old_rang / links_number, self.rang / links_number)

    def recompute_sum(self, prev_value, new_value):
        if prev_value == 0:
            self.in_links_num += 1
        self._in_sum = self._in_sum - prev_value + new_value
        self._recompute_rang()

    def get_rang(self):
        return self.rang

    def get_number(self):
        return self.number

    def get_in_links_num(self):
        return self.in_links_num

    def get_as_matrix_string(self, length):
        out_str = ""
        numbers = set()
        for page in self.outgoing_links:
            numbers.add(page.get_number())

        numbers = sorted(list(numbers))
        for i in range(len(numbers)):
            for j in range(i+1, len(numbers)):
                numbers[j] -= (numbers[i] + 1)

        #
        #print()
        #print("num:", self.number)
        #
        #
        #print("list:", numbers)
        #
        for next_num in numbers:
            #
            #print("len:", length)
            #
            out_str += "0;" * next_num + "1;"
            #
            #print("out:", out_str)
            #
            length -= next_num + 1
        out_str += "0;" * length
        return out_str[0:-1]

    def __str__(self):
        links = ""
        for page in self.outgoing_links:
            links += str(page.get_number()) + " "
        return str(self.number) + ": " + str(self.rang) + " ( " + links + ") in: " + str(self.in_links_num)


def LCDmodel(vertices_number, file_out, filepath=""):
    N = vertices_number * 2
    points = [None for i in range(N)]

    # creating curves
    for i in range(vertices_number):
        first = random.randint(0, N-1)
        while points[first] != None:
            first = (first + 1) % N

        second = random.randint(0, N-1)
        while first == second or points[second] != None:
            second = (second + 1) % N

        if first < second:
            points[first] = second
            points[second] = -first
        else:
            points[first] = -second
            points[second] = first

    # making pages
    total_index = 0
    current_vertex = 0
    pages = list()
    for i in range(vertices_number):
        linked_pages = []
        while points[total_index] > 0:
            points[total_index] = current_vertex
            total_index += 1

        page_index = points[abs(points[total_index])]
        if page_index != current_vertex:
            linked_pages = [ pages[page_index] ]


        points[total_index] = current_vertex
        pages.append(_page(current_vertex, pages=linked_pages))

        total_index += 1
        current_vertex += 1

    with open(filepath+file_out, "w") as file:
        for page in pages:
            file.write(page.get_as_matrix_string(len(pages)) + "\n")

    with open(filepath+"true_"+file_out, "w") as file:
        out_str = ""
        for page in pages:
            out_str += str(page.get_rang()) + " "
        file.write(out_str)



def BAmodel(vertices_number, file_out, filepath=""):
    page0 = _page(0)
    page1 = _page(1, pages=[page0, ])
    page2 = _page(2, pages=[page0, page1])
    pages = [page0, page1, page2]

    out_links_number = 6  # with self-reference

    for i in range(vertices_number - 3):

        # getting different links
        current_page_links_number = random.randint(1, 3)
        current_page_links = set()

        for j in range(current_page_links_number):
            linked_page = random.randint(0, out_links_number - 1) # [a, b]

            # page number defenition
            id = 0
            while True:
                current_in_links_num = pages[id].get_in_links_num()
                if current_in_links_num >= linked_page:
                    break
                else:
                    linked_page -= (current_in_links_num + 1)  # with self-reference
                    id += 1

            while id in current_page_links:
                id = (id + 1) % len(pages)

            current_page_links.add(id)

        out_links_number += 1 + current_page_links_number

        # forming _page input
        linked_pages = []
        for number in current_page_links:
            linked_pages.append(pages[number])

        # adding new page
        pages.append(_page(i+3, pages=linked_pages))

    with open(filepath+file_out, "w") as file:
        for page in pages:
            file.write(page.get_as_matrix_string(len(pages)) + "\n")

    with open(filepath+"true_"+file_out, "w") as file:
        out_str = ""
        for page in pages:
            out_str += str(page.get_rang()) + " "
        file.write(out_str)


def TreeGenerator(output="return", levels=3, print_res=False, sep=';'):
    prev_pages_number = 2

    tlist = []
    pages_number = 0

    for level in range(levels):
        new_pages_number = random.randint(prev_pages_number, 2 ** level + 2)

        for i in range(new_pages_number):
            links = []

            links_number = random.randint(1, level * 2 + 1)
            for link_number in range(links_number):
                link = random.randint(0, pages_number + new_pages_number - 1)
                while link == pages_number + i:
                    link = random.randint(0, pages_number + new_pages_number - 1)

                links.append(link)

            tlist.append(sorted(list(set(links))))
            if print_res:
                print(pages_number + i, " (", level, "): ", tlist[pages_number + i], sep="")

        pages_number += new_pages_number
        prev_pages_number = new_pages_number
        #print(level, pages_number)

    generators_information["SeparatedLevelsTreeGenerator"] = {
        "pages number": len(tlist)
    }

    if output == "return":
        return tlist
    else:
        with open(output, "w") as file:
            number_of_links = 0
            id = 0
            for row in tlist:
                id += 1
                #if id % 1000 == 0:
                    #print(id)
                separator = ""
                line = ""
                current_position = 0
                for item in row:
                    number_of_links += 1
                    line += "0;" * (item - current_position) + "1;"
                    current_position = item + 1
                line += "0;" * (pages_number - current_position)

                file.write(line[0:-1] + "\n")

            generators_information["SeparatedLevelsTreeGenerator"]["links number"] = number_of_links


def generate_tg_files(startnum, endnum, outdir="PageRank/pregenerated_structs/"):
    outfile = outdir + "level{}.txt"
    pages_links_numbers = []
    for levels in range(startnum, endnum):
        TreeGenerator(levels=levels, output=outfile.format(levels))
        generated = generators_information["SeparatedLevelsTreeGenerator"]["pages number"]
        links_number = generators_information["SeparatedLevelsTreeGenerator"]["links number"]
        print("level: {} gen: {} links: {}".format(levels, generated, links_number))
        pages_links_numbers.append((generated, links_number))
    return pages_links_numbers


def get_connected_level(pages_number, min_number):
    pages_links = [[] for i in range(pages_number)]
    pages_1 = [min_number]
    pages_2 = [i for i in range(min_number + 1, min_number + pages_number)]
    additional_links_number = random.randint(0, pages_number * 2)

    a = min_number
    for i in range(pages_number - 1):
        # a -> b
        b_num = random.randint(0, len(pages_2) - 1)
        b = pages_2.pop(b_num)

        pages_links[a - min_number].append(b)
        pages_1.append(b)
        a = b

    pages_links[b - min_number].append(min_number)

    for i in range(additional_links_number):
        a = random.choice(pages_1)
        b = random.choice(pages_1)
        while a == b:
            b = random.choice(pages_1)
        pages_links[a - min_number].append(b)

    for i in range(len(pages_links)):
        pages_links[i] = list(set(pages_links[i]))

    return pages_links


def SeparatedLevelsTreeGenerator(output="return", levels=3, print_res=False, sep=';'):
    prev_pages_number = 2

    generators_information["SeparatedLevelsTreeGenerator"] = {
        "levels": []
    }
    tlist = []
    pages_number = 0

    for level in range(levels):
        new_pages_number = random.randint(prev_pages_number, 2 ** level + 2)

        links_list = get_connected_level(new_pages_number, pages_number)

        for i in range(new_pages_number):
            generators_information["SeparatedLevelsTreeGenerator"]["levels"].append(level)

            links = links_list[i]
            if level != 0:
                top_links_number = random.randint(1, 4)
                for j in range(top_links_number):
                    top_level_link_page = random.randint(pages_number - prev_pages_number, pages_number - 1)
                    links.append(top_level_link_page)

            tlist.append(sorted(list(set(links))))
            if print_res:
                print(pages_number + i, " (", level, "): ", tlist[pages_number + i], sep="")

        pages_number += new_pages_number
        prev_pages_number = new_pages_number
    generators_information["SeparatedLevelsTreeGenerator"]["number"] = pages_number
    if output == "return":
        return tlist
    else:
        with open(output, "w") as file:
            for row in tlist:
                separator = ""
                line = ""
                num_in_row = 0
                for i in range(pages_number):
                    if num_in_row >= len(row) or i != row[num_in_row]:
                        line += separator + "0"

                    else:
                        line += separator + "1"
                        num_in_row += 1

                    separator = sep

                file.write(line + "\n")


def BinaryTreeGenerator(output="return", levels=5, sep=';'):
    tlist = [[], ]
    node_levels = [0, ]
    current_level_nodes = [0]
    next_level_nodes = []
    next_node_number = 1

    for level in range(1, levels):
        for node in current_level_nodes:
            tlist.append([node])
            node_levels.append(level)
            next_level_nodes.append(next_node_number)
            next_node_number += 1

            tlist.append([node])
            node_levels.append(level)
            next_level_nodes.append(next_node_number)
            next_node_number += 1

        current_level_nodes = next_level_nodes
        next_level_nodes = []

    generators_information["BinaryTreeGenerator"] = {
        "levels": node_levels
    }

    pages_number = len(tlist)

    if output == "return":
        return tlist
    else:
        with open(output, "w") as file:
            id = 0
            for row in tlist:
                id += 1
                #if id % 1000 == 0:
                    #print(id)
                separator = ""
                line = ""
                current_position = 0
                for item in row:
                    line += "0;" * (item - current_position) + "1;"
                    current_position = item + 1
                line += "0;" * (pages_number - current_position)

                file.write(line[0:-1] + "\n")
