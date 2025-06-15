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

def get_pi_digit(position):
    """
    Get the digit of pi at the specified position (0-indexed) using mmap.
    Returns -1 if the character at the position is a decimal point.
    """
    try:
        # Adjust position to account for the "3." at the beginning
        file_position = position + 1
        
        with open('pi.txt', 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                if file_position < len(mm):
                    char = chr(mm[file_position])
                    if char == '.':
                        return -1
                    else:
                        return char
                else:
                    return None
                    
    except FileNotFoundError:
        print("File 'pi.txt' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
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