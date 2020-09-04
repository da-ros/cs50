from cs50 import get_int

numberC, newN, i, suma = 0, 0, 0, 0

numberC = get_int("Input credit card number: ")
newN = numberC  #number to loop trough to avoid mutate the original

while newN > 0:
    num = newN % 10
    if (i%2 == 0):
        suma += num
    else:
        actual = num*2
        if(actual>9):
            newAc = actual
            while newAc > 0:
                digit = newAc%10
                suma += digit
                newAc //= 10
        else:
            suma += actual
    i += 1
    newN //= 10

if (i>=13 and i<=16):
    lastDigit, penDigit = 0, 0
    checkN = numberC # Number to loop through to avoid mutate original
    while checkN > 0:
        lastDigit = checkN%10
        if (checkN>=10 and checkN<=99):
            penDigit = checkN%10
        checkN //= 10
    if (lastDigit==4 and (suma%10==0)):
        print("VISA")
    elif (lastDigit==3 and i==15 and (suma%10==0) and (penDigit==4 or penDigit==7)):
        print("AMEX")
    elif (lastDigit==5 and i==16 and (suma%10==0) and (penDigit in [1,2,3,4,5])):
        print("MASTERCARD")
    else:
        print("INVALID")
else:
    print("INVALID")