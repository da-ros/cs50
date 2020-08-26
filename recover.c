#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if(argc != 2){
        printf("Usage: ./recover image\n");
        return 1;
    }
    // Open memory card
    FILE *file = fopen(argv[1], "r");

    if(!file){
        printf("File cannot be opened\n");
        return 1;
    }

    int n_photo = 0;
    FILE *img = NULL;
    BYTE *buffer = malloc(sizeof(BYTE) * 512);
    while(!feof(file)){ // Repeat until end of card

        fread(buffer, sizeof(BYTE), 512, file); // Read 512 bytes into a buffer

        if (buffer[0]==0xff && buffer[1]==0xd8 && buffer[2]==0xff && (buffer[3] & 0xf0)==0xe0){ // If start of a new JPEG, write first 512 B chunk
            if(n_photo==0){  // If first JPEG file

                char filename[10]; // Give name to JPEG file
                sprintf(filename, "%03i.jpg", n_photo);
                n_photo++;

                img = fopen(filename, "a"); // Create JPEG file

                fwrite(buffer, sizeof(BYTE), 512, img); // Write into JPEG file
            }
            else{ // If it is not the first JPEG file found
                fclose(img); // First close the previous file

                char filename[10]; // Give name to JPEG file
                sprintf(filename, "%03i.jpg", n_photo);
                n_photo++;

                img = fopen(filename, "a"); // Create JPEG file

                fwrite(buffer, sizeof(BYTE), 512, img); // Write into JPEG file
            }
        }
        else if (n_photo>0){ // Keep writing next 512 B chunk of the same img file
            fwrite(buffer, sizeof(BYTE), 512, img);
        }
    }
    fclose(img);// Close the last written file and free buffer
    fclose(file);
    free(buffer);
}
