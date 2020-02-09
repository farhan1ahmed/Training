#!/bin/python

import math
import os
import random
import re
import sys
from itertools import combinations
# Complete the maxMin function below.
def maxMin(k, arr):
    unfair = float('inf')
    allsubarr = combinations(arr, k)
    for subarr in allsubarr:
        intsubarr = [int(x) for x in subarr]
        unfairness= max(intsubarr)- min(intsubarr)
        if unfairness < unfair:
            unfair = unfairness
    return unfair

if __name__ == '__main__':
    num_ele = int(input())
    len_subarr = int(input())
    elements = []
    for i in range(num_ele):
        elements.append(input())

    print(maxMin(len_subarr, elements))
