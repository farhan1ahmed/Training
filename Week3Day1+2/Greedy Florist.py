#!/bin/python

import math
import os
import random
import re
import sys

# Complete the getMinimumCost function below.
def getMinimumCost(k, c):
    maxfor1person = len(c)//k + (len(c) - k*(len(c)//k))
    sortedprice = sorted(price)
    cost = 0
    for i in range(maxfor1person):
        cost += (i+1) * sortedprice[maxfor1person-(i+1)]
    j = i+1
    for friend in range(k-1):
        for i in range(len(c)//k):
            cost += (i+1) * sortedprice[j+(len(c)//k)-(i+1)]
        j += len(c)//k
    return cost

if __name__ == '__main__':
    fnf = [int(x) for x in input().split()]

    price = [int(x) for x in input().split()]

    print(getMinimumCost(fnf[1], price))
