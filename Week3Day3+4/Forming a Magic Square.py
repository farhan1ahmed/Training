#!/bin/python3

import math
import os
import random
import re
import sys
OUTPUT_PATH = r'C:\Users\hp\PycharmProjects\Training\Week3Day3+4\Output.txt'
# Complete the formingMagicSquare function below.
def formingMagicSquare(s):
    valid_solutions =[[[2,9,4], [7,5,3], [6,1,8]],[[4,9,2],[3,5,7 ],[8,1,6]], [[8,1,6], [3,5,7],[4,9,2]], [[6,1,8],[7,5,3],[2,9,4]],\
                      [[8,3,4], [1,5,9], [6,7,2]],[[4,3,8],[9,5,1 ],[2,7,6]], [[6,7,2], [1,5,9],[8,3,4]], [[2,7,6],[9,5,1],[4,3,8]]]
    all_costs = []
    for sol in valid_solutions:
        cost = 0
        for c in range(3):
            for i in range(3):
                if s[c][i] != sol[c][i]:
                    cost += abs(s[c][i]-sol[c][i])
        all_costs.append(cost)
    print(min(all_costs))
    return min(all_costs)

if __name__ == '__main__':
    fptr = open(OUTPUT_PATH, 'w')

    s = []

    for _ in range(3):
        s.append(list(map(int, input().rstrip().split())))

    result = formingMagicSquare(s)

    fptr.write(str(result) + '\n')

    fptr.close()
