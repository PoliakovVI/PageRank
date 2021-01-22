import PageRank.TransitionMatrix as tx
import PageRank.ComputingMethods as md
import PageRank.Generators as gen
import PageRank.Test as t
import time
import random


#t.CompleteTest()
#exit(0)

#gen.TreeGenerator(output="file.txt", levels=12)
#exit(0)
tm = tx.TransitionMatrix()
tm.read_from_txt("file.txt")
tpm = tx.TransitionProbabilityMatrix(tm)
tl = tx.TransitionList(tm)

# print("Methods time {}:".format(tm._pages_number))
# for method in t.__methods:
#     method_type = t.__methods_data[method.__name__]
#
#     if method_type == "tm":
#         data = tm
#     elif method_type == "tl":
#         data = tx.TransitionList(tm)
#     elif method_type =="tpm":
#         data = tx.TransitionProbabilityMatrix(tm)
#
#     method(data)
#     print(method.__name__, " has finished!")
# print(md.methods_run_information["spent time"])

# {'MarkovChain': 1.015460729598999,
#  'PowerMethod': 47.517489433288574,
#  'AdaptivePowerMethod': 11.127044916152954,
#  'ExtrapolatingAdaptivePowerMethod': 10.561493396759033,
#  'EndpointRandomStartMonteCarloMethod:linear': 0.060633182525634766,
#  'EndpointCyclicStartMonteCarloMethod': 0.18993282318115234,
#  'CompletePathMonteCarloMethod': 0.1920452117919922,
#  'StoppingCompletePathMonteCarloMethod': 0.20283770561218262,
#  'RandomStartStoppingCompletePathMonteCarloMethod': 0.049947261810302734}
