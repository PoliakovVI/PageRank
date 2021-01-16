import PageRank.TransitionMatrix as tx
import PageRank.CountMethods as md
import time


def print_range(arr, names):
    new_one = []
    for i in range(len(arr)):
        new_one.append((arr[i], names[i]))
    result = sorted(new_one, reverse=True)
    for item in result:
        print(item[1], "  ", item[0])

def run_and_print(method, names, matrix, precision):
    result = method(matrix, precision=precision)
    print_range(result, names)
    return


tm = tx.TransitionMatrix()
tm.read_from_txt("matrix.txt")

tpm = tx.TransitionProbabilityMatrix(tm)

tl = tx.TransitionList(tm)

print(tm)
print(tm._links_numbers)
print()
print(tpm)
print()
print(tl)

names=['A', 'B', 'C', 'D', 'E', 'F', 'P1', 'P2', 'P3', 'P4', 'P5']
precision = 0.0001

print("MarkovChain")
run_and_print(md.MarkovChain, names, tpm, precision)

print("PowerMethod")
run_and_print(md.PowerMethod, names, tm, precision)

print("AdaptivePowerMethod")
run_and_print(md.AdaptivePowerMethod, names, tm, precision)

print("ExtrapolatingAdaptivePowerMethod")
print_range(md.AdaptivePowerMethod(tm, precision, extrapolation=True), names)

print("EndpointRandomStartMonteCarloMethod, linear")
print_range(md.EndpointRandomStartMonteCarloMethod(tl, order="linear", iterations=1), names)

print("EndpointRandomStartMonteCarloMethod, square")
print_range(md.EndpointRandomStartMonteCarloMethod(tl, order="square", iterations=1), names)

print("EndpointCyclicStartMonteCarloMethod")
print_range(md.EndpointCyclicStartMonteCarloMethod(tl), names)

print("CompletePathMonteCarloMethod")
print_range(md.CompletePathMonteCarloMethod(tl, iterations=3), names)

print("StoppingCompletePathMonteCarloMethod")
print_range(md.StoppingCompletePathMonteCarloMethod(tl, iterations=3), names)

print("RandomStartStoppingCompletePathMonteCarloMethod")
print_range(md.RandomStartStoppingCompletePathMonteCarloMethod(tl, order="linear", iterations=3), names)

print(md.methods_run_information)
