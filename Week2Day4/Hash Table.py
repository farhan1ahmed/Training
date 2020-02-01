from collections import Counter


def checkMagazine(magazine, note):
    negative = 'YES'
    result = Counter(magazine)
    for value in Counter(note):
        for loop in range(Counter(note).get(value)):
            if value in result and result[value] > 0:
                result[value] -= 1
            else:
                negative = 'NO'
    return negative


if __name__ == '__main__':
    mn = input().split()

    m = int(mn[0])

    n = int(mn[1])

    magazine = input().rstrip().split()

    note = input().rstrip().split()

    print(checkMagazine(magazine, note))
