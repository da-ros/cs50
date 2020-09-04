from cs50 import get_int

def printline(row, size):
    for i in range(size - row):
        print(" ", end="")
    for i in range(row):
        print("#", end="")
    print("  ", end="")
    for i in range(row):
        print("#", end="")
    print()

while True:
    size = get_int("Enter pyramid size: ")
    if size>0 and size<9:
        break
for row in range(1, size+1):
    printline(row, size)
        
