from sys import argv, exit
import csv
from cs50 import SQL

# Check for correct command-line input
if len(argv) != 2:
    print("Usage: python import.py characters.csv")
    exit(1)

# Reference empty database named students.db, Just comment: "create tables with columns we need", because it is already created
db = SQL("sqlite:///students.db")
#db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

# Open CSV expected
file = open(argv[1], "r")
input_csv = csv.DictReader(file)

# For each row, parse name to insert into database
for row in input_csv:
    if len(row["name"].split()) == 3:
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?,?,?,?,?)", row["name"].split()[0], row["name"].split()[1], row["name"].split()[2], row["house"], int(row["birth"]))
    else:
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?,?,?,?,?)", row["name"].split()[0], None, row["name"].split()[1], row["house"], int(row["birth"]))


