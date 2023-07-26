from cs50 import get_string
import re


def main():
    # Ask for text
    txt = get_string("Text: ")

    # Count the number of letters in the text
    ltr = letter(txt)
    # Count the number of words in the text
    wd = word(txt)
    # Count the number of sentences in the text
    sen = sentence(txt)

    print(ltr)
    print(wd)
    print(sen)
    # Calculate and print readability
    index = round((0.0588 * (ltr / wd) * 100) - (0.296 * (sen / wd) * 100) - 15.8)
    print(index_out(index))


def letter(txt):
    ltr = 0
    # Only count the letters in text text
    for i in txt:
        # Determine if the character is a letter
        if i.isalpha():
            ltr += 1
    return ltr


def word(txt):
    # Split the text into individual words
    txt = txt.split()
    # Count the words and return the value
    return len(txt)


def sentence(txt):
    # Split the text into sentences
    txt = re.split(r'[.!?]+', txt)
    # Count the sentences and return the value
    return len(txt) - 1


def index_out(index):
    # Determine readability grade based on index
    if index < 1:
        return "Before Grade 1"
    if index >= 16:
        return "Grade 16+"
    return f"Grade {index}"


if __name__ == "__main__":
    main()