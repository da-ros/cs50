from cs50 import get_string

def count_letters(text):
    number_letters = 0
    for i in text:
        if (i.isalpha()):
            number_letters += 1
    return number_letters

def count_words(text):
    blanks = 0
    for i in range(len(text)):
        if (text[i]==" " and text[i+1]==" "):
            continue
        elif (text[i]==" "):
            blanks += 1
    return blanks+1

def count_sentences(text):
    number_sentences = 0
    for i in text:
        if (i=="!" or i=="?" or i=="."):
            number_sentences += 1
    return number_sentences


text = get_string("Text: ")

number_letters = count_letters(text)
number_words = count_words(text)
number_sentences = count_sentences(text)

L = (100*number_letters)/number_words
S = (100*number_sentences)/number_words
index = 0.0588 * L - 0.296 * S - 15.8

if (index >= 16):
    print("Grade 16+")
elif (index < 1):
    print("Before Grade 1")
else:
    print("Grade {}".format(round(index)))

