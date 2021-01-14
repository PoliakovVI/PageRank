import PageRank.TransitionMatrix as tx
import PageRank.CountMethods as md


def print_range(arr, names):
    new_one = []
    for i in range(len(arr)):
        new_one.append((arr[i], names[i]))
    result = sorted(new_one, reverse=True)
    for item in result:
        print(item[1], "  ", item[0])


tm = tx.TransitionMatrix()
tm.read_from_txt("matrix.txt")
tpm = tx.TransitionProbabilityMatrix(tm)

print(tm)
print(tm._links_numbers)
print()
print(tpm)

mc_result = md.MarkovChain(tpm)
print(mc_result)
pm_result = md.PowerMethod(tm)
print(pm_result)

names=['A', 'B', 'C', 'D', 'E', 'F', 'P1', 'P2', 'P3', 'P4', 'P5']
print("markov")
print_range(mc_result, names)
print("power")
print_range(pm_result, names)
print("power persentage")
print_range(
    list(map(lambda x: x / sum(pm_result), pm_result)),
    names)

