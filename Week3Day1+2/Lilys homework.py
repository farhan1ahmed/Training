#!/bin/python

import math
import os
import random
import re
import sys

# Complete the countingSort function below.
def lilysHomework(arr):
    swaps = 0
    for i in range(len(arr)-1):
        small = min(arr[i:])
        index = arr.index(small)
        if index != i:
            arr[i], arr[index] = arr[index], arr[i]
            swaps += 1
    return swaps


if __name__ == '__main__':
    n = int(input())

    arr = [int(x) for x in input().split()]

    print(lilysHomework(arr))

