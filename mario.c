#include <stdio.h>
#include <cs50.h>

void printLine(int row, int lenght){
    for (int i=0; i<lenght-row; i++){
        printf(" ");
    }
    
    for (int i=0; i<row; i++){
        printf("#");
    }
    
    printf("  ");
    
    for (int i=0; i<row; i++){
        printf("#");
    }
    printf("\n");
}

int main(void){
    int n;
    
    do{
        n = get_int("Height: ");
    } while (n<1 || n>8);
    
    for(int i=1; i<= n; i++)
        printLine(i, n);
    
}