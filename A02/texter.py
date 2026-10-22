import sys

class Texter:
    def __init__(self, filename):
        self.filename = filename

    def count_lines(self):
        with open(self.filename, "r") as f:
            count = 0
            for line in f:
                count += 1
        return count

    def count_sed(self):   
        with open(self.filename, "r") as f:
            count = 0
            for line in f:
                if "sed" in line.lower():
                    count += 1
        return count

    def run(self):
        print("This is the number of lines in the text file:", self.count_lines())
        print("This is the number of lines containing sed:", self.count_sed())

if len(sys.argv) < 2:
    print("Usage: python3 texter.py <filename>")
else:
    texter = Texter(sys.argv[1])
    texter.run()