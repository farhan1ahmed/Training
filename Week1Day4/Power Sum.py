X = int(input("Enter integer to sum to: "))
N = int(input("Enter integer power to raise number to: "))
num_arr = []
for i in range(int(pow(X, 1/N))):
    num_arr.append(i+1)


def powersum(number, power, arr, index):
    if number == 0:
        return 1
    if index >= len(arr):
        return 0
    count = powersum(number, power, arr, index+1)+powersum(number - pow(arr[index], power), power, arr, index+1)
    return count


print(powersum(X, N, num_arr, 0))