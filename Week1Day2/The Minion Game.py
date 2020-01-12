main_string = input("Enter a string: ")
vowels = 'AEIOU'
kevin_score = 0
stuart_score = 0
for i in range(0, len(main_string)):
    if main_string[i] in vowels:
        kevin_score += len(main_string)-i
    else:
        stuart_score += len(main_string) - i
print("Kevin's Score: " + str(kevin_score))
print("Stuart's Score: " + str(stuart_score))
if kevin_score > stuart_score:
    print("Kevin Wins!")
elif kevin_score == stuart_score:
    print("Draw!")
else:
    print("Stuart Wins!")