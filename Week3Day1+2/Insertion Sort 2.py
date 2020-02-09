#!/bin/python

import math
import os
import random
import re
import sys

# Complete the insertionSort2 function below.
def insertionSort2(n, arr):
    for i in range(1, n):
        for j in range(i):
            if arr[i] < arr[j]:
                shift = arr[i]
                arr[j+1:i+1] = arr[j:i]
                arr[j] = shift
        arrprint(arr)

def arrprint(array):
    for i in range(len(array)):
        print(array[i], end=' ')
    print('')
if __name__ == '__main__':
    n = int(input())

    arr = [int(x) for x in input().split()]

    insertionSort2(n, arr)