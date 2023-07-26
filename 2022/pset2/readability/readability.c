#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

float letter(string text, int h);
float sentence(string text, int h);
float word(string text, int h);

int main(void)
{
    string text = get_string("Text: ");

    //Calculate lenght of text
    int h = strlen(text);

    //Variables for calculating readability
    float lt = letter(text, h);
    float sen = sentence(text, h);
    float wd = word(text, h);

    //Calculating readability
    int index = round((0.0588 * lt / wd * 100) - (0.296 * sen / wd * 100) - 15.8);

    //Printing readability
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

float letter(string text, int h)
{
    float lt = 0;
    for (int g = 0; g < h; g++)
    {
        //Uppercase all letter to reduce range of values (ASCII)
        text[g] = toupper(text[g]);
        //Set range of value that variable "lt" counts
        if (text[g] >= 65 && text[g] <= 90)
        {
            lt += 1;
        }
    }
    return lt;
}

float sentence(string text, int h)
{
    float sen = 0;
    for (int i = 0; i < h; i++)
    {
        //Count the number of ending punctuations to count the number of sentences
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sen += 1;
        }
    }
    return sen;
}

float word(string text, int h)
{
    //Explicity count the last word of every sentence
    float wd = 1;
    for (int j = 0; j < h; j++)
    {
        //Count the number of spaces to count the number of words
        if (text[j] == ' ')
        {
            wd += 1;
        }
    }
    return wd;
}