#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int valid_key(string key);

int main (int argc, string argv[]){
    
    if (argc != 2){
        printf("Please provide just one command-line key\n");
        return 1;
    }
    else if(valid_key(argv[1])==-1){
        printf("Key must contain 26 characters\n");
        return 1;
    }
    else if(valid_key(argv[1])==-2){
        printf("Key must only contain alphabetic characters\n");
        return 1;
    }
    else if(valid_key(argv[1])==-3){
        printf("Key must not contain repeated characters\n");
        return 1;
    }
    
    string plain_text = get_string("plaintext: ");
    string key = argv[1];
    int n_key[26];
    // Make mapping to key in ascii numbers
    for (int i=0; i<26; i++){
        if (key[i]>=65 && key[i]<=90){
            n_key[i] = key[i] - (65+i);
        }
        else if(key[i]>=97 && key[i]<=122){
            n_key[i] = key[i] - (97+i);
        }
    }
    
    string cipher = plain_text;
    int n_cipher = strlen(cipher);
    // Cipher according to index in n_key
    for (int i=0; i<n_cipher; i++){
        if(cipher[i]>=65 && cipher[i]<=90){
            cipher[i] += n_key[cipher[i]-65];
        }
        else if(cipher[i]>=97 && cipher[i]<=122){
            cipher[i] += n_key[cipher[i]-97];
        }
    }
    printf("ciphertext: %s\n", cipher);
    return 0;
}

int valid_key(string key){
    
    int n_char = strlen(key);
    if(n_char!=26) return -1;
    
    for (int i=0; i<n_char; i++){
        if ((key[i]>=65 && key[i]<=90) || (key[i]>=97 && key[i]<=122))
            continue;
        else
            return -2;
    }
    
    string alphabet="abcdefghijklmnopqrstuvwxyz";
    int n_alphabet = strlen(alphabet);
    for (int i=0; i<n_char; i++){
        key[i] = tolower(key[i]);
    }
    
    int count=0;
    
    for (int i=0; i<n_alphabet; i++){
        for (int j=0; j<n_char; j++){
            if (alphabet[i]==key[j])
                count++;
        }
        if(count>1) return -3;
        count = 0;
    }
    return 1;
}