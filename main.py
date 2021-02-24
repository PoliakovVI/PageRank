import PageRank.TransitionMatrix as tx
import PageRank.ComputingMethods as md
import PageRank.Generators as gen
import PageRank.Test as t
import time
import random


t.CompleteTest()
exit(0)

start_level = 4
finish_level = 11

file_in_template = "PageRank/pregenerated_structs/level{}.txt"
time_data = None
for level in range(start_level, finish_level):
    file = file_in_template.format(level)
    time_data = t.CompleteTimeTest(file, time_data)

for i in range(len(time_data["AdaptivePowerMethod"])):
    print(time_data["AdaptivePowerMethod"][i], time_data["ExtrapolatingAdaptivePowerMethod"][i], time_data["PowerMethod"][i])
