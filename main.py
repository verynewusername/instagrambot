'''
main.py for running the Instagram pi posting tool.

Author: Efe Sirin
Date: 2025-06-06

if 0 posts -> put index -1
if 1 post -> put index 0
....

=> number of posts - 1 = index of pi digit to post
'''
from get_credentials import get_login_session
from get_pi_digit import get_pi_digit
from get_post_count import get_media_count_of_user
from instagram_poster import post_pi_number
from dotenv import load_dotenv
import os

# load override for testing purposes
load_dotenv('.env.override', override=True)

IDX = -1
TARGET = 229

def get_caption_for_index(index, number):
    """
    Get the caption for the given index.
    """
    if index == -1:
        return "Hello World!"
    elif index == 0:
        return "The only dot in this number."
    else:
        return f"The digit at index {index} is {number}."

def main():

    # Get global variables IDX
    global IDX
    global TARGET

    username = os.getenv("INSTAGRAM_USERNAME")
    encrypted_password = os.getenv("INSTAGRAM_ENCRYPTED_PASSWORD")

    # Get login session
    try:
        while IDX < TARGET:
            assert username, "INSTAGRAM_USERNAME is not set in .env file"
            assert encrypted_password, "INSTAGRAM_ENCRYPTED_PASSWORD is not set in .env file"

            if os.path.exists('login_details.json'):
                print("login_details.json already exists. Skipping login.")
            else:
                # Get the login session
                get_login_session()
                
            # Assert that there is "login_details.json" file manually
            assert os.path.exists('login_details.json'), "login_details.json not found in current directory"

            # Get the number of posts
            post_count = get_media_count_of_user(username)
            print(f"User @{username} has {post_count} posts.")

            pi_index = post_count - 1  # Convert to 0-indexed

            # Get the digit of pi at the post count index
            pi_digit = get_pi_digit(pi_index)  # Convert to 0-indexed
            print(f"The digit of pi at index {post_count} is: {pi_digit}")

            # Get the caption for the index
            caption = get_caption_for_index(pi_index, pi_digit)
            print(f"Caption for index {pi_index}: {caption}")

            # # Post to Instagram
            status = post_pi_number(int(pi_digit), caption)

            assert status == "OK", "Failed to post to Instagram"
            IDX = pi_index
    except Exception as e:
        # print(f"An error occurred: {e}")
        # return
        # Stack trace for debugging
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

# ENDOF FILE main.py