def compare_triplets():
    a_score = input('Enter Alice\'s score: ').split()
    b_score = input('Enter Bob\'s score: ').split()
    a = 0
    b = 0
    for n in range(len(a_score)):
        if a_score[n] > b_score[n]:
            a += 1
        if a_score[n] < b_score[n]:
            b += 1
    return [a, b]


print(compare_triplets())