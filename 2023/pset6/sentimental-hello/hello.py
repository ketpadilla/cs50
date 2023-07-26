from cs50 import get_string


def main():
    # Ask for name
    name = get_string("What is your name? ")

    # Greet person
    print(f"hello, {name}")


main()