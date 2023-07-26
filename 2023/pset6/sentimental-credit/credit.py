from cs50 import get_int


def main():
    # Get credit card number and number length
    num, num_len = get_num()
    print(num)

    # Determine if card is valid and its first two digits
    is_valid, num_dig = luhn_alg(num)

    # Determine and print what type of card it is
    card = typ_card(num_len, num_dig, is_valid)
    print(card)


def not_valid():
    # Return message for invalid card
    return "INVALID"


def get_num():
    # Ask for credit card number
    num = get_int("Number: ")

    # Calculate length
    num_len = len(str(num))

    # Only accept numbers with a length of 13 to 16
    if num_len in range(13, 17):
        return num, num_len
    else:
        print(not_valid())
        raise SystemExit(1)


def luhn_alg(num):
    # Initialize variables
    dig = dig1 = dig2 = sum_evn = sum_2odd = 0

    # Loop through digits from right to left
    while num > 0:
        # Get the rightmost digit and update variables
        dig2 = dig1
        dig1 = num % 10

        # Double every other digit starting from the second to last
        if dig % 2 == 0:
            sum_evn += dig1
        else:
            # If the doubled digit is two digits, add the digits together
            sum_2odd += ((2 * dig1) // 10) + ((2 * dig1) % 10)

        # Move to the next digit
        num //= 10
        dig += 1

    # Combine the last two digits to get the first two digits of the card number
    num_dig = (dig1 * 10) + dig2

    # Check if the sum of the digits is divisible by 10
    is_valid = (sum_evn + sum_2odd) % 10 == 0

    # Return the validity and first two digits of the card number
    return is_valid, num_dig


def typ_card(num_len, num_dig, is_valid):
    # Determine type of card based on length, first two digits, and validity
    if not is_valid:
        return not_valid()

    if num_len == 15 and num_dig in [34, 37]:
        return "AMEX"

    if num_len in [13, 16]:
        if 40 <= num_dig <= 49:
            return "VISA"
        if 51 <= num_dig <= 55:
            return "MASTERCARD"

    # Invalid if unidentified
    return not_valid()


if __name__ == "__main__":
    main()