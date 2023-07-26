import csv
import sys


def main():

    # Ensure correct CL usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # Place specified files into variables
    CSV = sys.argv[1]
    TXT = sys.argv[2]

    # Initialize variable to store CSV data
    data = []
    # Read CSV data into variable
    with open(CSV, 'r') as f:
        reader = csv.DictReader(f)
        for r in reader:
            data.append(r)

    # Initialize variable to store CSV data
    seq = ()
    # Read TXT data into variable
    with open(TXT, 'r') as f:
        seq = f.read()

    # Find longest match of each STR in DNA sequence
    subsequences = list(data[0].keys())[1:]
    results = {subsequence: longest_match(seq, subsequence) for subsequence in subsequences}

    # Check database for matching profiles
    for person in data:
        match = sum(int(person[subsequence]) == results[subsequence] for subsequence in subsequences)

        # If all subsequences match
        if match == len(subsequences):
            print(person["name"])
            break
    else:
        print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
