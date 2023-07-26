def main():
    height = get_int()
    for i in range(height):
        # Print left side
        print(" " * (height - i - 1), end="")
        print("#" * (height - (abs(i-height+1))), end="")
        # Print right side
        print("  ", end="")
        print("#" * (height - (abs(i-height+1))))


def get_int():
    while True:
        try:
            # Only accept positive integers 1 to 8
            n = int(input("Height: "))
            if n in range(1, 9):
                return n
        except ValueError:
            print("Not an integer ")


main()