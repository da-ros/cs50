from sys import argv, exit
import csv
from cs50 import SQL

# Check for correct command-line arguments
if len(argv) != 2:
    print("Usage: python roster.py Gryffindor")
    exit(1)

# Reference database
db = SQL("sqlite:///students.db")

# Query database, result will be a list of Python dicts, where each dict represents a row in the table
query = db.execute("SELECT * FROM students WHERE house = ? ORDER BY last, first", argv[1])

for row in query:
    if row["middle"] == None:
        print("{} {}, born {}".format(row["first"], row["last"], row["birth"]))
    else:
        print("{} {} {}, born {}".format(row["first"], row["middle"], row["last"], row["birth"]))