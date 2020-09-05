from sys import argv, exit
import csv

if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

# Open CSV DNA database
fileDB = open(argv[1], "r")
input_DB = csv.DictReader(fileDB)
# Load CSV into a list of dictionaries
DB_list = []
for row in input_DB:
    DB_list.append(row)
#print(DB_list[0]['TATC'])

# Open each DNA sequence txt and save into string
fileSEQ = open(argv[2], "r")
input_SEQ = fileSEQ.read()

# Save list of STR types from DB_list
types_str=[]
for key in DB_list[0].keys():
    types_str.append(key)
types_str = types_str[1:] # Erase 'name' field from list of STR types

# For each STR type compute the longest run of consecutive repeats and save in dictionary 'count_str'
count_str={}
for str_t in types_str:
    longest=0
    for i in range(len(input_SEQ)):
        current=0
        for j in range(i, len(input_SEQ), len(str_t)):
            nucleotids = input_SEQ[j:j+len(str_t)]
            if nucleotids == str_t:
                current += 1
                if current>longest:
                    longest=current
            else:
                break
    count_str[str_t] = longest

# For each dict in the list of dictionaries DB_list, compare against count_str dictionary
number_str_t = len(types_str)
for dictPerson in DB_list:
    str_t_matches=0
    for str_t in count_str.keys():
        if (int(dictPerson[str_t]) == count_str[str_t]):
            str_t_matches += 1
    if (str_t_matches == number_str_t):
        print(dictPerson['name'])
        exit(0)
print("No Match")


#print(DB_list)
#print(input_SEQ)
#print(types_str)
#print(count_str)

