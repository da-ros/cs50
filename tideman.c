#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int find_index(int ranks[], int element);//implemented by me
bool is_cycle_with(int winner, int loser);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO
    for (int i=0; i<candidate_count; i++){
        if (strcmp(candidates[i], name)==0){
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    for (int k=0; k<candidate_count; k++){ // iterate over ranks array
        for (int i=0; i<candidate_count; i++){ //iterate over onw row of preferences 2D array
            if (find_index(ranks, i)>k) //check in index greater than
                preferences[ranks[k]][i]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    for (int i=0; i<candidate_count; i++){ //iterate over preferences 2D array
        for (int j=i; j<candidate_count; j++){
            if (j==i) continue;
            if(preferences[i][j]>preferences[j][i]){ //compare opposites indices
                pairs[pair_count].winner=i;
                pairs[pair_count].loser=j;
                pair_count++;
            }
            else if(preferences[i][j]<preferences[j][i]){
                pairs[pair_count].winner=j;
                pairs[pair_count].loser=i;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO
    int strength[pair_count];
    
    for(int i=0; i<pair_count; i++){
        strength[i] = preferences[pairs[i].winner][pairs[i].loser] - preferences[pairs[i].loser][pairs[i].winner];
    }
    
    for (int i=0; i<pair_count; i++){
        int max_ind = i;
        for (int j=i; j<pair_count; j++){
            if(strength[j]>strength[max_ind])
                max_ind=j;
        }
        int temp=strength[i];
        pair temp_pair=pairs[i];
        
        strength[i]=strength[max_ind];
        pairs[i]=pairs[max_ind];
        
        strength[max_ind]=temp;
        pairs[max_ind]=temp_pair;
    }
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    for (int i=0; i<pair_count; i++){ //traverse the pairs array
        if (!is_cycle_with(pairs[i].winner, pairs[i].loser))
            locked[pairs[i].winner][pairs[i].loser] = true;
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    bool free_columns[candidate_count];  //to keep track of free columns, at first suppose all are free
    for (int i=0; i<candidate_count; i++){
        free_columns[i]=true;
    }
    
    for(int j=0; j<candidate_count; j++){  //check which columns are free
        for(int i=0; i<candidate_count; i++){
            if (locked[i][j]==true)
                free_columns[j]=false;
        }
    }
    
    for(int i=0; i<candidate_count; i++){
        if(free_columns[i]==true){
            printf("%s\n", candidates[i]);
            return;
        }
    }
    return;
}
// my functions implementations
int find_index(int *ranks, int element)
{
    for (int i=0; i<candidate_count; i++){
        if(ranks[i]==element)
            return i;
    }
    return -1;
}
bool is_cycle_with(int winner, int loser) //if at least one column is still completely free after putting this parameter bool: there is not cycle
{
    bool locked_clone[candidate_count][candidate_count]; //clone the array to avoid mutate the original while testing
    for(int i=0; i<candidate_count; i++){
        for(int j=0; j<candidate_count; j++){
            locked_clone[i][j] = locked[i][j];
        }
    }
    locked_clone[winner][loser] = true; //simulate setting the intended bool var
    
    
    bool free_columns[candidate_count];  //to keep track of free columns, at first suppose all are free
    for (int i=0; i<candidate_count; i++){
        free_columns[i]=true;
    }
    
    for(int j=0; j<candidate_count; j++){  //check which columns are still free
        for(int i=0; i<candidate_count; i++){
            if (locked_clone[i][j]==true)
                free_columns[j]=false;
        }
    }
    
    int count_free_columns = 0;
    for (int i=0; i<candidate_count; i++){ //traverse free_columns bool array to check how many columns are still free
        if (free_columns[i]==true)
            count_free_columns++;
    }
    
    if (count_free_columns>0) return false;  //if at least one column is still free, there is no cycle
    else return true;
}
