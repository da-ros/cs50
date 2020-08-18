#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");
    
    int number_letters = count_letters(text);
    int number_words = count_words(text);
    int number_sentences = count_sentences(text);
    
    float L = (100*number_letters)/(float) number_words;
    float S = (100*number_sentences)/(float) number_words;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    
    if (index>=16) {
        printf("Grade 16+\n");
        return 0;
    }
    else if (index<1){
        printf("Before Grade 1\n");
        return 0;
    }
    else{
        printf("Grade %.0f\n", round(index));
        return 0;
    }
}

int count_letters(string text){
    
    int number_letters=0;
    
    for (int i=0, n=strlen(text); i<n; i++){
        if((text[i]>=65 && text[i]<=90) || (text[i]>=97 && text[i]<=122))
            number_letters++;
    }
    return number_letters;
}

int count_words(string text){
    
    int blanks=0;
    
    for (int i=0, n=strlen(text); i<n; i++){
        if(text[i]==32 && text[i+1]==32)
            continue;
        else if(text[i]==32)
            blanks++;
    }
    
    return blanks+1;
}

int count_sentences(string text){
    
    int number_sentences=0;
    
    for (int i=0, n=strlen(text); i<n; i++){
        if(text[i]==33 || text[i]==63 || text[i]==46)
            number_sentences++;
    }
    return number_sentences;
}