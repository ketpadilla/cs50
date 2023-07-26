#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <wctype.h>
#include <stdlib.h>

bool only_digits(char argv[1]);
string rotate(string text, int key);

int main(int argc, string argv[])
{
    //Checking
    if (argc != 2 || only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    //Ciphering
    string text = get_string("plaintext: ");
    int key = atoi(argv[1]);
    string cipher = rotate(text, key);

    //Print ciphertext
    printf("ciphertext: %s\n", cipher);
}

bool only_digits(char argv[1])
{
    //Convert string to integer
    int n = (int)argv[1];
    //Only digits will be accepted
    if (n == 0 || (n >= 48 && n <= 57))
    {
        return 0;
    }
    else
    {
        return 1;
    }
}

string rotate(string text, int key)
{
    //Reduce value of key to less then or equal to 26
    while (key > 26)
    {
        key -= 26;
    }

    for (int i = 0; i < strlen(text); i++)
    {
        if (iswalpha(text[i]))
        {
            if (text[i] + key < 123)
            {
                text[i] = text[i] + key;
            }
            else
            {
                //Rotation of characters must only be between letters
                text[i] = text[i] + key - 26;
            }
        }
    }
    return text;
}