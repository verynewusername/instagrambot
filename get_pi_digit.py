'''
This script retrieves a specific digit of pi from a file named 'pi.txt'.

Author: Efe Sirin
Date: 2025-06-06

EX USAGE:
3.14159
IDX > output
-1 > 3
0 > -1
1 > 1
2 > 4
3 > 1
4 > 5
5 > 9
... 

. is ignored

'''
import mmap

def read_digit_mmap(filename, position):
    with open(filename, 'rb') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            if position < len(mm):
                return chr(mm[position])
    return None


def get_pi_digit(position):
    """
    Get the digit of pi at the specified position (0-indexed).
    Returns -1 if the character at the position is a decimal point.
    """
    try:
        position = position + 1
        with open('pi.txt', 'r') as f:
            pi_digits = f.read()  # Don't remove decimal point
            if position < len(pi_digits):
                if pi_digits[position] == '.':
                    return -1
                else:
                    return pi_digits[position]
            else:
                return None
    except FileNotFoundError:
        print("File 'pi.txt' not found.")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python get_pi_digit.py <position>")
        sys.exit(1)
    
    try:
        position = int(sys.argv[1])
        digit = get_pi_digit(position)
        if digit is not None:
            print(f"The digit of pi at position {position} is: {digit}")
        else:
            print(f"No digit found at position {position}.")
    except ValueError:
        print("Please provide a valid integer position.")
        sys.exit(1)


# ENDOF FILE get_pi_digit.py 