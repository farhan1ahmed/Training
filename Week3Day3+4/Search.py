#!/bin/python3

import math
import os
import random
import re
import sys
OUTPUT_PATH = r'C:\Users\hp\PycharmProjects\Training\Week3Day3+4\Output.txt'
# Complete the gridSearch function below.
def gridSearch(G, P):
    G_col = len(G[0])
    G_rows = len(G)
    P_col = len(P[0])
    P_rows = len(P)
    prow = 0
    for row in range(G_rows - P_rows+1):
        for i in range(G_col-P_col+1):
            j = 0
            while j < P_col:

                if G[row][i+j] != P[prow][j]:
                    break
                j += 1
            if j == P_col:
                for nextrow in range(P_rows-1):
                    if G[row+nextrow+1][i:i+P_col] != P[prow+nextrow+1]:
                        return "NO"
    return "YES"

if __name__ == '__main__':
    fptr = open(OUTPUT_PATH, 'w')

    t = int(input())

    for t_itr in range(t):
        RC = input().split()

        R = int(RC[0])

        C = int(RC[1])

        G = []

        for _ in range(R):
            G_item = input()
            G.append(G_item)

        rc = input().split()

        r = int(rc[0])

        c = int(rc[1])

        P = []

        for _ in range(r):
            P_item = input()
            P.append(P_item)

        result = gridSearch(G, P)

        fptr.write(result + '\n')

    fptr.close()
