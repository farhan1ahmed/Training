size_group = input("Enter size of group: ")
room_list = [int(x) for x in input().split()]
for room in room_list:
    if room_list.count(room) == 1:
        print(room)