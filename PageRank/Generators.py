import random


generators_information = {}


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
