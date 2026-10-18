with open("test.txt", "r") as f:
    count = 0
    for line in f:
        count += 1

print("This is the number of lines in the text file:", count)

with open("test.txt", "r") as f:
    count= 0
    for line in f:
        if "sed" in line.lower():
            count += 1

print("This is the number of lines containing the word sed:", count)


