from heapq import heappop, heappush, heapify
queries = int(input("Number of queries: "))
heap = []
for i in range(queries):
    com = [int(x) for x in input().split()]
    if com[0]==1:
        heappush(heap, com[1])
    elif com[0]==2:
        index = heap.index(com[1])
        heap[index]= float("-inf")
        ind_par = int((index+1)/2)
        while index > 0 and heap[index] > heap[ind_par]:
            heap[index], heap[ind_par] = heap[ind_par], heap[index]
            index = heap.index(com[1])
            ind_par = int((index+1) / 2)
        heappop(heap)
    else:
        print(heap[0])