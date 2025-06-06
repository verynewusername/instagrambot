'''
This script retrieves a specific digit of pi from a file named 'pi.txt'.

EX USAGE:
3.14159
0 > 3
1 > 1
2 > 4
3 > 1
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
    """
    try:
        with open('pi.txt', 'r') as f:
            pi_digits = f.read().replace('.', '')  # Remove decimal point
            if position < len(pi_digits):
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