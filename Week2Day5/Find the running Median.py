from heapq import heappop, heappush, heapify
queries = int(input("Number of queries: "))
minheap = []
maxheap = []
median = int(0)
for i in range(queries):
    element = int(input())
    if len(maxheap) == int(0) and len(minheap) == int(0):
        heappush(maxheap, -element)
    elif element <= median:
        heappush(maxheap, -element)
    else:
        heappush(minheap, element)
    if abs(len(maxheap)-len(minheap)) > 1:
        if len(maxheap) > len(minheap):
            transfer = -heappop(maxheap)
            heappush(minheap, transfer)
        else:
            transfer = heappop(minheap)
            heappush(maxheap, -transfer)
    if len(maxheap) > len(minheap):
        median = -maxheap[0]
    elif len(maxheap) < len(minheap):
        median = minheap[0]
    else:
        median = float((-maxheap[0]+minheap[0])/2)
    print("Median: {}".format(median))