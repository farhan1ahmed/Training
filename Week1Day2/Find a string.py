main_string = (input("Enter the main string: "))
sub_string = (input("Enter the sub-string: "))
c = 0
for i in range(0, len(main_string)-len(sub_string)+1):
    if main_string[i:i+len(sub_string)] == sub_string:
        c+=1
print(c)