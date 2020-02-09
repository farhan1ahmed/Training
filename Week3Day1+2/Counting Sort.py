#!/bin/python

import math
import os
import random
import re
import sys

# Complete the countingSort function below.
def countingSort(arr):
    largest = max(arr)
    countarr = [0] * (largest + 1)
    for i in range(len(arr)):
        countarr[arr[i]] += 1
    print(countarr)

if __name__ == '__main__':
    n = int(input())

    arr = [int(x) for x in input().split()]

    countingSort(arr)

