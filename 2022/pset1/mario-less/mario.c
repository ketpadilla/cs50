#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompting user for desired height
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    //Printing staircase
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height - i - 1; j++)
        {
            //Adding spaces
            printf(" ");
        }
        for (int k = 0; k <= i; k++)
        {
            //Adding bricks
            printf("#");
        }
        printf("\n");
    }
}