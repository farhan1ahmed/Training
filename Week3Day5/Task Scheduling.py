#!/bin/python3

import os
import sys
from operator import itemgetter
OUTPUT_PATH = r'C:\Users\hp\PycharmProjects\Training\Week3Day5\Output.txt'
#
# Complete the taskScheduling function below.
#

def taskScheduling(tasks):
    original = tuple(tasks)
    print("Hi")
    total_minutes = sum(x[1] for x in tasks)
    minutes = 0
    overshoot_time = []
    #print(priority_task)
    print("Original List: ", tasks)
    while minutes != total_minutes:
        margin = [x[0] - x[1] for x in tasks]
        print("Margin: ", margin)
        print("Original List: ", original)
        nexjob = margin.index(min(margin))
        print(nexjob)
        for y in tasks:
            y[0] = y[0]-1
        print("Original List: ", original)
        tasks[nexjob][1] = tasks[nexjob][1] - 1
        print("Original List: ", original)
        if tasks[nexjob][1] == 0:
            overshoot_time.append(tasks[nexjob][0]-minutes)
            tasks.pop(nexjob)
        print("Tasks:", tasks)
        print("Original List: ", original)
        print("OS_Time: ", overshoot_time)
        minutes += 1
    print(overshoot_time)
    return overshoot_time


if __name__ == '__main__':
    fptr = open(OUTPUT_PATH, 'w')

    t = int(input())
    tasks = []
    for t_itr in range(t):
        dm = input().split()

        d = int(dm[0])

        m = int(dm[1])
        tasks.append([d,m])

    result = taskScheduling(tasks)
    fptr.write(str(result) + '\n')

    fptr.close()
