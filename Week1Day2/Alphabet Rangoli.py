import string
alphabets = string.ascii_lowercase
dash = "-"
size = int(input("Enter size: "))
thickness = 2*(2*size-1)-1
for i in range(1, 2*size+1, 2):
    s = "-".join(alphabets)
    print((s[i-1:0:-1]+s[0:i:1]).center(thickness, "-"))
for i in range(2*size-2, 0, -2):
    s = "-".join(alphabets)
    print((s[i-1:0:-1]+s[0:i:1]).center(thickness, "-"))