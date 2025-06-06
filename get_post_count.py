''' 
This script retrieves the post count of a given Instagram user by their username.

Author: Efe Sirin
Date: 2025-06-06

'''

import requests
import json
import sys
import re

def load_login_details():
    """Load login details from login_details.json"""
    try:
        with open('login_details.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: login_details.json not found in current directory")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in login_details.json")
        sys.exit(1)

def get_user_id_from_username(username, login_data):
    """
    Get Instagram user ID from username by fetching the profile page
    """
    session_info = login_data['session_info']
    cookies = session_info['cookies']
    
    # Method 1: Try the profile page approach
    profile_url = f"https://www.instagram.com/{username}/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(profile_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        
        # Look for the user ID in the page content
        # Instagram embeds user data in JSON within script tags
        content = response.text
        
        # Pattern to find user ID in the page source
        patterns = [
            r'"profilePage_(\d+)"',
            r'"id":"(\d+)".*?"username":"' + re.escape(username) + '"',
            r'"owner":{"id":"(\d+)"',
            r'"user_id":"(\d+)"',
            r'"pk":(\d+).*?"username":"' + re.escape(username) + '"'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                user_id = match.group(1)
                # print(f"Found user ID for @{username}: {user_id}")
                return user_id
        
        # If regex fails, try to find it in the JSON data
        # Look for window._sharedData or similar
        json_match = re.search(r'window\._sharedData\s*=\s*({.*?});', content)
        if json_match:
            try:
                shared_data = json.loads(json_match.group(1))
                # Navigate through the JSON structure to find user ID
                entry_data = shared_data.get('entry_data', {})
                profile_page = entry_data.get('ProfilePage', [])
                if profile_page:
                    user_data = profile_page[0].get('graphql', {}).get('user', {})
                    user_id = user_data.get('id')
                    if user_id:
                        # print(f"Found user ID for @{username}: {user_id}")
                        return user_id
            except json.JSONDecodeError:
                pass
        
        # print(f"Could not find user ID for @{username} in profile page")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching profile page: {e}")
        return None

def get_user_id_via_search(username, login_data):
    """
    Alternative method: Use Instagram's search API
    """
    session_info = login_data['session_info']
    cookies = session_info['cookies']
    
    search_url = "https://www.instagram.com/web/search/topsearch/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'X-CSRFToken': session_info['csrf_token'],
        'X-IG-App-ID': '936619743392459',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/',
    }
    
    params = {
        'query': username,
        'context': 'blended'
    }
    
    try:
        response = requests.get(search_url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()
        
        data = response.json()
        users = data.get('users', [])
        
        for user in users:
            if user.get('user', {}).get('username') == username:
                user_id = user.get('user', {}).get('pk')
                if user_id:
                    # print(f"Found user ID via search for @{username}: {user_id}")
                    return str(user_id)
        
        # print(f"User @{username} not found in search results")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error with search API: {e}")
        return None

def make_instagram_request(username, target_user_id, login_data):
    """Make the Instagram GraphQL request"""
    
    session_info = login_data['session_info']
    cookies = session_info['cookies']
    
    url = "https://www.instagram.com/graphql/query"
    
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.instagram.com',
        'Referer': f'https://www.instagram.com/{username}/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'X-CSRFToken': session_info['csrf_token'],
        'X-FB-Friendly-Name': 'PolarisProfilePageContentQuery',
        'X-IG-App-ID': '936619743392459',
    }
    
    # Prepare the variables for the GraphQL query
    variables = {
        "id": target_user_id,
        "render_surface": "PROFILE"
    }
    
    data = {
        'variables': json.dumps(variables),
        'doc_id': '9916454141777118'
    }
    
    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"GraphQL request failed: {e}")
        return None

def get_media_count_of_user(username):
    """Get the media count of a user by username"""
    if username is None or username == "":
        print("Username cannot be empty")
        sys.exit(1)
    
    username = sys.argv[1].replace('@', '')  # Remove @ if present
    
    # Load login details
    login_data = load_login_details()
    
    # print(f"Loaded login details for user ID: {login_data['session_info']['user_id']}")
    # print(f"Resolving user ID for: @{username}")
    
    # Try to get user ID from username
    target_user_id = get_user_id_from_username(username, login_data)
    
    # If first method fails, try search API
    if not target_user_id:
        # print("Trying search API method...")
        target_user_id = get_user_id_via_search(username, login_data)
    
    if not target_user_id:
        print(f"Failed to resolve user ID for @{username}")
        sys.exit(1)
    
    # print(f"Making GraphQL request for user ID: {target_user_id}")
    
    # Make the request
    result = make_instagram_request(username, target_user_id, login_data)
    
    if result:
        # print("\n" + "="*50)
        # print("RESPONSE:")
        # print("="*50)
        # print(json.dumps(result, indent=2))
        
        # Save to file
        if False:
            output_filename = f"{username}_profile_data.json"
            with open(output_filename, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nData saved to: {output_filename}")

         # only get the media_count under data['data']['user']['media_count']
        media_count = result.get('data', {}).get('user', {}).get('media_count', 0)
        # print(f"User @{username} has {media_count} posts.")
        return media_count
    else:
        print("Failed to get profile data")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_post_count.py <username>")
        sys.exit(1)
    username = sys.argv[1]
    if username.startswith('@'):
        username = username[1:]
    post_count = get_media_count_of_user(username)
    if post_count is not None:
        print(f"User @{username} has {post_count} posts.")
    else:
        print(f"Could not retrieve post count for @{username}.")


# ENDOF FILE get_post_count.py