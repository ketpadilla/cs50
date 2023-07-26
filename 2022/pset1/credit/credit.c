#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Input
    long num;
    do
    {
        num = get_long("Number: ");
    }
    while (num < 0);

    // Determine length
    int len = 0;
    long card = num; //Variable "card" used to retain inputted number
    for (len = 0; num != 0; num /= 10, len++);
    if (len < 13 || len == 14 || len > 16)
    {
        // Is not the lenght of a valid credit card number
        printf("EOF\n");
    }

    // Sum of digits multiplied by 2
    long k = 10;
    long sum1 = 0;
    long calc1; //for first half of computation of sum1
    for (long n = 100; n <= 10000000000000000; n = n * 100)
    {
        calc1 = ((card % n) / k) * 2;
        sum1 = sum1 + (calc1 / 10) + (calc1 % 10);
        k = k * 100;
    }

    // Sum of digits not multiplied by 2
    long m = 10;
    long l = 1;
    long sum2 = 0;
    do
    {
        sum2 = sum2 + ((card % m) / l);
        m = m * 100;
        l = l * 100;
    }
    while (m <= 1000000000000000);

    // Sum of the two sums
    long sum = sum1 + sum2;

    // Validation
    while (card >= 100)
    {
        card /= 10;
    }
    if ((card > 55 || card < 34) || (sum % 10 != 0))
    {
        //Inputted number do not have the starting number of any credit card company
        printf("INVALID\n");
    }
    else
    {
        if ((len == 15) && (card == 34  || card == 37))
        {
            // Number is from AMEX
            printf("AMEX\n");
        }
        else if (len == 13 || len == 16)
        {
            if (card >= 40 && card <= 49)
            {
                // Number is from VISA
                printf("VISA\n");
            }
            else if (card >= 51 && card <= 55)
            {
                // Number is from MASTERCARD
                printf("MASTERCARD\n");
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
}
