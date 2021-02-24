from PageRank import TransitionMatrix, Generators, ComputingMethods, _create_html_table
import time

__LEVEL_TEST_FILE = "PageRank/_tests/level_test.txt"

__methods_data = {
    "MarkovChain": "tpm",
    "PowerMethod": "tm",
    "AdaptivePowerMethod": "tm",
    "ExtrapolatingAdaptivePowerMethod": "tm",
    "EndpointRandomStartMonteCarloMethod": "tl",
    "EndpointCyclicStartMonteCarloMethod": "tl",
    "CompletePathMonteCarloMethod": "tl",
    "StoppingCompletePathMonteCarloMethod": "tl",
    "RandomStartStoppingCompletePathMonteCarloMethod": "tl"
}
__methods = [
    ComputingMethods.MarkovChain,
    ComputingMethods.PowerMethod,
    ComputingMethods.AdaptivePowerMethod,
    ComputingMethods.ExtrapolatingAdaptivePowerMethod,
    ComputingMethods.EndpointRandomStartMonteCarloMethod,
    ComputingMethods.EndpointCyclicStartMonteCarloMethod,
    ComputingMethods.CompletePathMonteCarloMethod,
    ComputingMethods.StoppingCompletePathMonteCarloMethod,
    ComputingMethods.RandomStartStoppingCompletePathMonteCarloMethod,
]
__true_tests = ["test1.txt", "test2.txt", "test3.txt"]


def __get_worked_method_object(file, method, method_opts={}):
    tm = TransitionMatrix.TransitionMatrix()
    tm.read_from_txt(file)
    method_type = __methods_data[method.__name__]

    if method_type == "tm":
        data = tm
    elif method_type == "tl":
        data = TransitionMatrix.TransitionList(tm)
    elif method_type == "tpm":
        data = TransitionMatrix.TransitionProbabilityMatrix(tm)
    else:
        raise Exception("Unknown method")
    method_object = method(data)
    try:
        method_object.stopping_run(precision=0.01)
    except Exception:
        method_object.iterating_run(iterations=1)
    return method_object


def __get_sort_pages(result):
    return list(
        map(
            lambda x: x[1],
            sorted(
                sorted(
                    [
                        (result[i], i) for i in range(len(result))
                    ],
                    key=lambda x: x[1]
                ),
                key=lambda x: x[0],
                reverse=True
            )
        )
    )


def positionTest(result, true_result):
    result_pages = __get_sort_pages(result)

    true_pages = __get_sort_pages(true_result)

    ################
    # for i in range(len(true_pages)):
    # print(true_pages[i], "<->", result_pages[i])

    pages_number = len(result)
    errors = 0
    for i in range(pages_number):
        if true_pages[i] != result_pages[i]:
            errors += 1
    if pages_number == 0:
        return 1
    return (pages_number - errors) / pages_number


def sequenceTest(result, true_result):
    result_pages = __get_sort_pages(result)
    true_pages = __get_sort_pages(true_result)

    i = 0
    pages_number = len(result)
    while i < len(true_pages):
        while true_pages[i] != result_pages[i]:
            value = result_pages[i]
            true_pages.remove(value)
            result_pages.remove(value)
            if i == len(true_pages):
                break
        i += 1
    if pages_number == 0:
        return 1
    return len(true_pages) / pages_number


def __normalize(vector):
    sum = 0
    for item in vector:
        sum += item
    normalized_vector = []
    for item in vector:
        normalized_vector.append(item / sum)
    return normalized_vector


def __calculate_l1_norm(lst1, lst2):
    l1_sum = 0
    for i in range(len(lst1)):
        l1_sum += abs(lst1[i] - lst2[i])
    return l1_sum


def vectorTest(result, true_result):
    result = __normalize(result)
    true_result = __normalize(true_result)
    return __calculate_l1_norm(true_result, result)


def levelTest(method, method_opts={}, levels=5, file=__LEVEL_TEST_FILE):
    Generators.BinaryTreeGenerator(output=file, levels=levels)

    method_object = __get_worked_method_object(file, method, method_opts)
    result = method_object._stat_vector

    pages_levels = Generators.generators_information['BinaryTreeGenerator']['levels']

    rating = sorted(
        sorted([tuple((result[i], pages_levels[i])) for i in range(len(result))], key=lambda x: x[1]),
        key=lambda x: x[0], reverse=True
    )

    mistakes = 0
    current_level = 0
    for item in rating:
        if item[1] == current_level:
            continue
        elif item[1] > current_level:
            current_level += 1
        else:
            mistakes += 1

    return (len(rating) - mistakes) / len(rating)


def distanceTest(result, true_result):
    result_pages = __get_sort_pages(result)
    true_pages = __get_sort_pages(true_result)

    sum_distance = 0
    for i in range(len(true_pages)):
        item = true_pages[i]
        j = 0
        while (item != result_pages[j]):
            j += 1

        sum_distance += abs(i - j)
    return sum_distance / len(true_pages)


def __get_matches_percentage(set1, set2):
    l_base = len(set1)
    l_new = len(set1.union(set2))
    return 2. - l_new / l_base


def topTest(result, true_result, top=None):
    if len(result) == 0:
        return

    if top is None:
        top = len(result)

    result_pages = __get_sort_pages(result)
    true_pages = __get_sort_pages(true_result)

    result_set = set()
    true_set = set()

    test = []

    for i in range(top):
        result_set.add(result_pages[i])
        true_set.add(true_pages[i])
        test.append(__get_matches_percentage(result_set, true_set))

    return test


def KendallCorrelationTest(result, true_result):
    # http://www.machinelearning.ru/wiki/index.php?title=%D0%9A%D0%BE%D1%8D%D1%84%D1%84%D0%B8%D1%86%D0%B8%D0%B5%D0%BD%D1%82_%D0%BA%D0%BE%D1%80%D1%80%D0%B5%D0%BB%D1%8F%D1%86%D0%B8%D0%B8_%D0%9A%D0%B5%D0%BD%D0%B4%D0%B5%D0%BB%D0%BB%D0%B0#:~:text=%D0%9A%D0%BE%D1%8D%D1%84%D1%84%D0%B8%D1%86%D0%B8%D0%B5%D0%BD%D1%82%20%D0%BA%D0%BE%D1%80%D1%80%D0%B5%D0%BB%D1%8F%D1%86%D0%B8%D0%B8%20%D0%9A%D0%B5%D0%BD%D0%B4%D0%B5%D0%BB%D0%BB%D0%B0%20(Kendall%20tau,%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D1%8F%2C%20%D0%B0%20%D1%81%D0%BE%D0%BE%D1%82%D0%B2%D0%B5%D1%82%D1%81%D1%82%D0%B2%D1%83%D1%8E%D1%89%D0%B8%D0%B5%20%D0%B8%D0%BC%20%D1%80%D0%B0%D0%BD%D0%B3%D0%B8.
    n = len(result)
    x = __normalize(result)
    y = __normalize(true_result)

    R = 0
    for i in range(1, n-1):
        for j in range(i+1, n):
            xi_less_xj = x[i] < x[j]
            yi_less_yj = y[i] < y[j]
            if xi_less_xj != yi_less_yj:
                R += 1

    return 1 - 4 * R / (n * (n - 1))



def ComparingTest(result, baseline_result):
    raise Exception("No available update")
    pt_res = positionTest(result, baseline_result)
    st_res = sequenceTest(result, baseline_result)
    vt_res = vectorTest(result, baseline_result)
    dt_res = distanceTest(result, baseline_result)

    print("Comparing test:")
    print("    Position test: {:.2f}%".format(pt_res * 100))
    print("    Sequence test: {:.2f}%".format(st_res * 100))
    print("    Vector test: {:.3f}".format(vt_res))
    print("    Distance test: {:.2f}".format(dt_res))
    print()


def print_percentage_bar(done, all, end="", lenght=20):
    percentage_symbols = done * lenght // all
    percentage_done = int(done / all * 100)
    out = "\r" + "|" + "#" * percentage_symbols + " " * (lenght - percentage_symbols) + \
          "| " + str(percentage_done) + "% done    "
    print(out, end=end)


def CompleteTest():
    test_matrix = []
    current_row = 0
    total_row_number = len(__methods) * (1 + len(__true_tests) * 6)
    print("Start complete test:")

    for method in __methods:

        test_number = 0
        lt_res = levelTest(method)

        test_matrix.append([method.__name__, "Level test", "#<", str(lt_res)])
        current_row += 1

        for file in __true_tests:
            # percentage drawing
            print_percentage_bar(current_row, total_row_number)

            test_number += 1

            true_file = "PageRank/_tests/true_" + file
            file = "PageRank/_tests/" + file
            method_object = __get_worked_method_object(file, method)
            with open(true_file, "r") as f:
                true_result = list(map(float, f.readline().split()))

            t_res = {}
            t_res["Position test"] = positionTest(method_object._stat_vector, true_result)
            t_res["Sequence test"] = sequenceTest(method_object._stat_vector, true_result)
            t_res["Vector test"] = vectorTest(method_object._stat_vector, true_result)
            t_res["Distance test"] = distanceTest(method_object._stat_vector, true_result)
            t_res["Kendall test"] = KendallCorrelationTest(method_object._stat_vector, true_result)

            tt_res = topTest(method_object._stat_vector, true_result, top=5)

            if method_object._stopping_run_time is not None:
                all_time = method_object._stopping_run_time
            else:
                all_time = method_object._iterating_run_time

            test_matrix.append(["#^", "Test " + str(test_number), "Top test", tt_res])
            current_row += 1

            for key in t_res:
                test_matrix.append(["#^", "#^", key, t_res[key]])
                current_row += 1

    html_report_file = "CompleteTestResults.html"
    table = _create_html_table.Table(test_matrix)
    table.writeHtml(html_report_file)

    print_percentage_bar(current_row, total_row_number, end="\n")
    print("Check out", html_report_file)


def CompleteTimeTest(file, prev_ctt_data=None):
    print("CompleteTimeTest:", file)

    if prev_ctt_data is None:
        data = {}
        for method in __methods:
            data[method.__name__] = []
    else:
        data = prev_ctt_data

    current_method_id = 0
    total_methods_number = len(__methods)
    for method in __methods:
        print_percentage_bar(current_method_id, total_methods_number)

        method_object = __get_worked_method_object(file, method)

        if method_object._stopping_run_time is not None:
            all_time = method_object._stopping_run_time
        else:
            all_time = method_object._iterating_run_time

        data[method.__name__].append(all_time)

        current_method_id += 1

    print_percentage_bar(current_method_id, total_methods_number, end="\n")
    return data