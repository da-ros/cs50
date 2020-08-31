// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 50000;



// Number of words loades into hash table
int n_words = 0;
// Flag dictionary loaded
bool dict_loaded = false;



// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // First convert to lowercase all word in order to obtain the same hashcode as the equivalent word in dictionary did
    char low_word[LENGTH+1];
    strcpy(low_word, word);
    //printf("\n\n\n%s\n%s\n\n", word, low_word); // For testing
    for(int i=0; i<strlen(low_word); i++){
        low_word[i] = tolower(low_word[i]);
    }
    //printf("%s\n%s", word, low_word); // For testing

    unsigned int index_hash = hash(low_word);

    node *cursor = table[index_hash];

    while(cursor != NULL){
        if(strcasecmp(cursor->word, word) == 0){
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{

     /*unsigned long H = 0; // The same as below hash function
     int i;

     for (i = 0; i < strlen(word); ++i) {
          H = (H * 33) + word[i];
     }
     return (H % N);*/


    // djb2 by Dan Bernstein
    unsigned long hash = 5381; //big prime number
    int c;

    while ((c = *word++))
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    char string[LENGTH+1];

    if (file == NULL){
        return false;
    }

    while(fscanf(file, "%s", string) != EOF){ //fscanf puts a null '\0' character at the end of every string copied

        node *n = malloc(sizeof(node));
        if(n == NULL){
            return false;
        }
        strcpy(n->word, string);
        n->next = NULL;

        unsigned int n_hash = hash(string);

        if(table[n_hash] == NULL){
            table[n_hash] = n;
            n_words++;
        }
        else{
            n->next = table[n_hash];
            table[n_hash] = n;
            n_words++;
        }
    }

    if(ferror(file)){
        fclose(file);
        return false;
    }
    else{
        fclose(file);
        dict_loaded = true;
        return true;
    }
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (dict_loaded){
        return n_words;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    int i;

    for(i=0; i<N; i++){
        node *cursor = table[i];

        while(cursor != NULL){
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }

    if(i == N)
        return true;

    return false;
}
