#!/bin/python

import math
import os
import random
import re
import sys

# Complete the insertionSort1 function below
def insertionSort1(n, arr):
    last = arr[n-1]
    for i in range(n-2, -1, -1):
        if arr[i] > last:
            arr[i+1] = arr[i]
            arrprint(arr)
        else:
            arr[i+1] = last
            arrprint(arr)


def arrprint(array):
    for i in range(len(array)):
        print(array[i], end=' ')
    print('')

if __name__ == '__main__':
    n = int(input())

    arr = [int(x) for x in input().split()]

    insertionSort1(n, arr)
