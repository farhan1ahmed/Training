#!/bin/python3

import os
import sys
module_path = os.path.dirname(os.path.realpath(__file__))
OUTPUT_PATH = r'C:\Users\hp\PycharmProjects\Training\Week3Day3+4\Output.txt'
#
# Complete the simpleArraySum function below.
#
def simpleArraySum(ar):
    sum = 0
    for i in ar:
        sum += i
    return sum


if __name__ == '__main__':
    fptr = open(OUTPUT_PATH, 'w')

    ar_count = int(input())

    ar = list(map(int, input().rstrip().split()))

    result = simpleArraySum(ar)

    fptr.write(str(result) + '\n')

    fptr.close()
