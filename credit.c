#include <stdio.h>
#include <cs50.h>

int main(void){
    long numberC, newN;
    int sum=0, i;
    
    numberC = get_long("Input credit card number: ");
    
    for (i=0, newN=numberC; newN>0; i++, newN/=10){
        int num = newN % 10;
        if (i%2 == 0)
            sum += num;
        else{
            int actual = num*2;
            if (actual>9){
                for(int newAc=actual; newAc>0; newAc/=10){
                    int digit = newAc%10;
                    sum += digit;
                }
            }
            else{
                sum += actual;
            }
        }
    }
    
    if (i>=13 && i<=16){
        int lastDigit;
        for(long checkN=numberC; checkN>0; checkN/=10){
            lastDigit = checkN%10;
        }
        if (lastDigit == 4 && (sum%10==0)){
            printf("VISA\n");
            return 0;
        }
        else if (lastDigit==3 && i==15 && (sum%10==0)){
            int penDigit;
            for(long checkN=numberC; checkN>=10; checkN/=10){
                penDigit = checkN%10;
            }
            if(penDigit==4 || penDigit==7){
                printf("AMEX\n");
                return 0;
            }
        }
        else if (lastDigit==5 && i==16 && (sum%10==0)){
            int penDigit;
            for(long checkN=numberC; checkN>=10; checkN/=10){
                penDigit = checkN%10;
            }
            if(penDigit==1 || penDigit==2 || penDigit==3 || penDigit==4 || penDigit==5){
                printf("MASTERCARD\n");
                return 0;
            }
        }
        else{
            printf("INVALID\n");
            return 0;
        }
    }
    else{
            printf("INVALID\n");
            return 0;
        }
}