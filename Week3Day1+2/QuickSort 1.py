#!/bin/python

import math
import os
import random
import re
import sys

# Complete the quickSort function below.
def quickSort(arr):
    pivot = arr[0]
    left = []
    right = []
    for i in range(1, len(arr)):
        if arr[i] < pivot:
            left.append(arr[i])
        elif arr[i] > pivot:
            right.append(arr[i])
    for i in range(len(left)):
        print(left[i], end=' ')
    print(pivot, end=' ')
    for i in range(len(right)):
        print(right[i], end=' ')

if __name__ == '__main__':
    n = int(input())

    arr = [int(x) for x in input().split()]

    quickSort(arr)
