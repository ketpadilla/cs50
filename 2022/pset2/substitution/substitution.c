#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

string rotate(string text, string key, int a[26]);
bool only_letters(string key);

int main(int argc, string argv[])
{
    //Check if command line argument is present
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    //Calculate distance between alphabeth letter and inputted letters
    string key = (argv[1]);
    int a[26];
    for (int i = 0; i < 26; i++)
    {
        if (isupper(key[i]))
        {
            a[i] = - ((65 + i) - key[i]);
        }
        if (islower(key[i]))
        {
            a[i] = - ((65 + i) - (key[i] - 32));
        }
    }

    //Check there are only 26 unqiue letters
    if (only_letters(key) == 1 || strlen(argv[1]) != 26)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    //Input text to cipher
    string text = get_string("plaintext: ");
    string cipher = rotate(text, key, a);

    //Print ciphertext
    printf("ciphertext: %s\n", cipher);
}

bool only_letters(string key)
{
    int wd = 0;

    //Set original alphabeth order
    string beta = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

    //Determine if there are only letters in the key
    for (int z = 5; z < 26; z++)
    {
        if ((key[z] >= 65 && key[z] <= 90) || (key[z] >= 97 && key[z] <= 122))
        {
            wd += 0;
        }
        else
        {
            wd++;
        }
    }

    //Determine if there are duplicate letters
    int ct = 0;
    for (int i = 0, j = 1; i < 26; i++, j++)
    {
        if (key[i] == key[j] && key[i] != ' ')
        {
            ct++;
        }
    }
    if (ct > 0)
    {
        wd++;
    }

    //Determine if program can continue or not
    if (wd != 0)
    {
        //printf("ct: %i\n", ct);
        return 1;
    }
    else
    {
        //printf("ct: %i\n", ct);
        return 0;
    }
}

string rotate(string text, string key, int a[26])
{
    //Set original alphabeth order
    string alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

    //Change plaintext to ciphertext
    for (int j = 0, k = -1; j < (strlen(text)); j++)
    {
        //Only change letters
        if (isalpha(text[j]))
        {
            //Find the letter to change
            do
            {
                k++;
            }
            while (text[j] != alpha[k]);
            //If specific letter is found
            if (text[j] == alpha[k])
            {
                if (isupper(text[j]))
                {
                    //Use this formula to change uppercase letterw
                    text[j] = text[j] + a[k];
                }
                if (islower(text[j]))
                {
                    //Use this formula to change lowercase letterss
                    text[j] = text[j] + a[k - 26];
                }
                k = 0;
            }
        }
        else
        {
            text[j] = text[j];
        }
    }
    return text;
}