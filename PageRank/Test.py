from PageRank import TransitionMatrix, Generators, ComputingMethods
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
__true_tests = ["test1.txt"]


def __get_method_result(file, method, method_opts):
    tm = TransitionMatrix.TransitionMatrix()
    tm.read_from_txt(file)
    method_type = __methods_data[method.__name__]

    if method_type == "tm":
        data = tm
    elif method_type == "tl":
        data = TransitionMatrix.TransitionList(tm)
    elif method_type =="tpm":
        data = TransitionMatrix.TransitionProbabilityMatrix(tm)
    else:
        raise Exception("Unknown method")

    return method(data, **method_opts)


def positionTest(file, true_file, method, method_opts={}):
    result = __get_method_result(file, method, method_opts)
    with open(true_file, "r") as f:
        true_answer = list(map(float, f.readline().split()))
        result_pages = list(
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

        true_pages = list(
            map(
                lambda x: x[1],
                sorted(
                    sorted(
                        [
                            (true_answer[i], i) for i in range(len(true_answer))
                        ],
                        key=lambda x: x[1]
                    ),
                    key=lambda x: x[0],
                    reverse=True
                )
            )
        )
        pages_number = len(result)
        errors = 0
        for i in range(pages_number):
            if true_pages[i] != result_pages[i]:
                errors += 1
        return (pages_number - errors) / pages_number


def sequenceTest(file, true_file, method, method_opts={}):
    result = __get_method_result(file, method, method_opts)
    with open(true_file, "r") as f:
        true_answer = list(map(float, f.readline().split()))
        result_pages = list(
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
        true_pages = list(
            map(
                lambda x: x[1],
                sorted(
                    sorted(
                        [
                            (true_answer
                             [i], i) for i in range(len(true_answer))
                        ],
                        key=lambda x: x[1]
                    ),
                    key=lambda x: x[0],
                    reverse=True
                )
            )
        )
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
        return len(true_pages) / pages_number


def __normalize(vector):
    sum = 0
    for item in vector:
        sum += item
    normalized_vector = []
    for item in vector:
        normalized_vector.append(item / sum)
    return normalized_vector


def vectorTest(file, true_file, method, method_opts={}):
    result = __normalize(__get_method_result(file, method, method_opts))
    with open(true_file, "r") as f:
        true_answer = __normalize(list(map(float, f.readline().split())))
        return ComputingMethods._calculateComponentsDistance(true_answer, result) / len(result)


def levelTest(method, method_opts={}, file=__LEVEL_TEST_FILE):
    levels=2  # only this one available
    Generators.SeparatedLevelsTreeGenerator(output=file, levels=levels)

    result = __get_method_result(file, method, method_opts)

    pages_levels = Generators.generators_information['SeparatedLevelsTreeGenerator']['levels']

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


def CompleteTest():
    for method in __methods:
        print("========== {} testing ==========".format(method.__name__))

        test_number = 0
        for file in __true_tests:
            test_number += 1

            true_file = "PageRank/_tests/true_" + file
            file = "PageRank/_tests/" + file
            pt_res = positionTest(file, true_file, method)
            st_res = sequenceTest(file, true_file, method)
            vt_res = vectorTest(file, true_file, method)
            lt_res = levelTest(method)

            print("Test number {}:".format(test_number))
            print("    Position test: {:.2f}%".format(pt_res * 100))
            print("    Sequence test: {:.2f}%".format(st_res * 100))
            print("    Vector test: {:.3f}".format(vt_res))
            print("    Level test: {:.2f}%".format(lt_res * 100))
            print()
