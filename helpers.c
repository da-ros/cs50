#include "helpers.h"
#include <math.h>

int is_location_valid(int i, int j, int height, int width);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i=0; i<height; i++){
        for (int j=0; j<width; j++){
            int av_pix = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed)/(float)(3));
            image[i][j].rgbtBlue = av_pix;
            image[i][j].rgbtGreen = av_pix;
            image[i][j].rgbtRed = av_pix;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i=0; i<height; i++){
        for (int j=0, k=width-1; j<width/2; j++, k--){
            RGBTRIPLE temp;
            temp = image[i][j];
            image[i][j] = image[i][k];
            image[i][k] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE original_im[height][width];
    for (int i=0; i<height; i++){
        for (int j=0; j<width; j++){
            original_im[i][j] = image[i][j];
        }
    }

    for (int i=0; i<height; i++){
        for (int j=0; j<width; j++){

            int sum_red = 0, sum_green = 0, sum_blue=0;
            int n_px = 0;
            int start_x = j-1;
            int start_y = i-1;
            int end_x = j+1;
            int end_y = i+1;

            for (int k=start_y; k<=end_y; k++){
                for (int l=start_x; l<=end_x; l++){
                    if (is_location_valid(k, l, height, width)){
                        sum_red += original_im[k][l].rgbtRed;
                        sum_green += original_im[k][l].rgbtGreen;
                        sum_blue += original_im[k][l].rgbtBlue;
                        n_px++;
                    }
                }
            }
            image[i][j].rgbtRed = round(sum_red / (float)(n_px));
            image[i][j].rgbtGreen = round(sum_green / (float)(n_px));
            image[i][j].rgbtBlue = round(sum_blue / (float)(n_px));
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE original_im[height][width];
    for (int i=0; i<height; i++){
        for (int j=0; j<width; j++){
            original_im[i][j] = image[i][j];
        }
    }
    
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    
    for (int i=0; i<height; i++){
        for (int j=0; j<width; j++){
            int gx_red = 0, gx_green = 0, gx_blue = 0;
            int gy_red = 0, gy_green = 0, gy_blue = 0;
            int start_x = j-1;
            int start_y = i-1;
            int end_x = j+1;
            int end_y = i+1;
            
            for (int k=start_y, m=0; k<=end_y; k++, m++){
                for (int l=start_x, n=0; l<=end_x; l++, n++){
                    if(is_location_valid(k, l, height, width)){
                        gx_red += gx[m][n] * original_im[k][l].rgbtRed;
                        gx_green += gx[m][n] * original_im[k][l].rgbtGreen;
                        gx_blue += gx[m][n] * original_im[k][l].rgbtBlue;
                        
                        gy_red += gy[m][n] * original_im[k][l].rgbtRed;
                        gy_green += gy[m][n] * original_im[k][l].rgbtGreen;
                        gy_blue += gy[m][n] * original_im[k][l].rgbtBlue;
                    }
                }
            }
            image[i][j].rgbtRed = (sqrt(pow(gx_red,2)+pow(gy_red,2)) > 255) ? 255 : round(sqrt(pow(gx_red,2)+pow(gy_red,2)));
            image[i][j].rgbtGreen = (sqrt(pow(gx_green,2)+pow(gy_green,2)) > 255) ? 255 : round(sqrt(pow(gx_green,2)+pow(gy_green,2)));
            image[i][j].rgbtBlue = (sqrt(pow(gx_blue,2)+pow(gy_blue,2)) > 255) ? 255 : round(sqrt(pow(gx_blue,2)+pow(gy_blue,2)));
        }
    }
    return;
}

int is_location_valid(int i, int j, int height, int width){
    if ((i>=0 && i<height) && (j>=0 && j<width))
        return 1;
    else
        return 0;
}