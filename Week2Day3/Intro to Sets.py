number = input("Number of plants: ")
distinct_heights = [int(x) for x in set(input("Number of plants: ").split())]
print("Average: " + str(sum(distinct_heights)/(len(distinct_heights))))