#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Prompting user for their name
    string name = get_string("What is your name? ");

    // Greeting user "hello"
    printf("hello, %s\n", name);
}