import os
import requests
import json
import time
import pickle
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def save_to_login_details(session_data, filename="login_details.json"):
    """
    Save session data to login_details.json file
    This will either create the file or update existing login details
    """
    try:
        # Load existing login details if file exists
        login_details = {}
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    login_details = json.load(f)
                print(f"📂 Loaded existing login details from: {filename}")
            except json.JSONDecodeError:
                print(f"⚠️  Invalid JSON in {filename}, creating new file")
                login_details = {}
        
        # Add session information to login details
        login_details.update({
            'session_info': {
                'last_login': datetime.now().isoformat(),
                'sessionid': session_data.get('sessionid'),
                'user_id': session_data.get('user_id'),
                'csrf_token': session_data.get('csrf_token'),
                'login_successful': session_data.get('success', False),
                'cookies': session_data.get('cookies', {})
            }
        })
        
        # Save updated login details
        with open(filename, 'w') as f:
            json.dump(login_details, f, indent=2)
        
        print(f"💾 Session data saved to: {filename}")
        print(f"📅 Last login timestamp: {login_details['session_info']['last_login']}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to save to login details: {e}")
        return False

def load_from_login_details(filename="login_details.json"):
    """
    Load session data from login_details.json
    """
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                login_details = json.load(f)
            
            session_info = login_details.get('session_info')
            if session_info:
                print(f"📂 Loaded session data from: {filename}")
                print(f"📅 Last login: {session_info.get('last_login')}")
                return session_info
            else:
                print(f"📂 No session info found in: {filename}")
                return None
        else:
            print(f"📂 No login details file found at: {filename}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to load from login details: {e}")
        return None

def create_session_from_saved_data(session_data):
    """
    Recreate a requests session from saved session data
    """
    try:
        session = requests.Session()
        
        # Restore cookies
        cookies = session_data.get('cookies', {})
        for name, value in cookies.items():
            session.cookies.set(name, value, domain='.instagram.com')
        
        # Set common headers
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "X-CSRFToken": session_data.get('csrf_token'),
            "X-IG-App-ID": "936619743392459",
        })
        
        print("🔄 Session recreated from saved data")
        return session
        
    except Exception as e:
        print(f"❌ Failed to recreate session: {e}")
        return None

def display_session_summary(session_data):
    """
    Display a nice summary of the session information
    """
    print("\n" + "=" * 60)
    print("📊 SESSION SUMMARY")
    print("=" * 60)
    print(f"🔑 Session ID: {session_data.get('sessionid', 'N/A')}")
    print(f"👤 User ID: {session_data.get('user_id', 'N/A')}")
    print(f"🛡️  CSRF Token: {session_data.get('csrf_token', 'N/A')}")
    print(f"📅 Login Time: {session_data.get('last_login', 'N/A')}")
    print(f"✅ Status: {'Active' if session_data.get('login_successful') else 'Inactive'}")
    
    # Show available cookies
    cookies = session_data.get('cookies', {})
    if cookies:
        print(f"\n🍪 Available Cookies ({len(cookies)}):")
        for cookie_name in cookies.keys():
            print(f"   • {cookie_name}")
    
    print("=" * 60)

def instagram_login_with_env_encryption():
    """
    Instagram login using encrypted password from environment variable
    """
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    encrypted_password = os.getenv("INSTAGRAM_ENCRYPTED_PASSWORD")
    
    # Debug: Print what we got from environment
    print(f"🔍 Debug - Username: {username}")
    print(f"🔍 Debug - Password: {'*' * len(password) if password else 'None'}")
    print(f"🔍 Debug - Encrypted Password: {encrypted_password[:50] + '...' if encrypted_password else 'None'}")
    
    if not username or not password:
        print("❌ Error: INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables must be set")
        return None
    
    if not encrypted_password:
        print("❌ Error: INSTAGRAM_ENCRYPTED_PASSWORD environment variable must be set")
        print("💡 Get this from your browser's network tab when logging in manually")
        print("📝 It should look like: #PWD_INSTAGRAM_BROWSER:10:1749219645:AelQAPeuyjDW1oslZedz2...")
        return None
    
    print(f"🔐 Logging into Instagram as: {username}")
    print(f"🔑 Using encrypted password from environment (length: {len(encrypted_password)} chars)")
    
    # ... rest of your login code stays the same ...
    session = requests.Session()
    
    # Step 1: Get login page with exact headers
    print("📄 Getting login page...")
    initial_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.6",
        "Accept-Encoding": "gzip, deflate, br",
        "sec-ch-ua": '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }
    
    session.headers.update(initial_headers)
    
    # Visit homepage first (like a real browser)
    home_response = session.get("https://www.instagram.com/")
    print(f"📄 Homepage status: {home_response.status_code}")
    
    # Small delay
    time.sleep(2)
    
    # Get login page
    login_page = session.get("https://www.instagram.com/?flo=true")
    print(f"📄 Login page status: {login_page.status_code}")
    
    if login_page.status_code != 200:
        print(f"❌ Failed to load login page: {login_page.status_code}")
        return None
    
    csrf_token = session.cookies.get('csrftoken')
    mid = session.cookies.get('mid')
    ig_did = session.cookies.get('ig_did')
    
    print(f"🔑 CSRF Token: {csrf_token}")
    print(f"🔑 MID: {mid}")
    print(f"🔑 IG_DID: {ig_did}")
    
    # Step 2: Prepare login data
    login_data = {
        'enc_password': encrypted_password,
        'caaF2DebugGroup': '0',
        'isPrivacyPortalReq': 'false',
        'loginAttemptSubmissionCount': '0',
        'optIntoOneTap': 'false',
        'queryParams': '{"flo":"true"}',
        'trustedDeviceRecords': '{}',
        'username': username,
        'jazoest': '22733'
    }
    
    # Step 3: Set exact headers from working request
    login_headers = {
        "Host": "www.instagram.com",
        "Connection": "keep-alive",
        "sec-ch-ua-full-version-list": '"Chromium";v="136.0.0.0", "Brave";v="136.0.0.0", "Not.A/Brand";v="99.0.0.0"',
        "sec-ch-ua-platform": '"macOS"',
        "sec-ch-ua": '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-model": '""',
        "sec-ch-ua-mobile": "?0",
        "X-IG-App-ID": "936619743392459",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "*/*",
        "X-Instagram-AJAX": "1023570583",
        "X-CSRFToken": csrf_token,
        "X-Web-Session-ID": "yt8jxi:yj4zmk:pzaeuk",
        "X-ASBD-ID": "359341",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "X-IG-WWW-Claim": "hmac.AR1NQWcvrEmK3axZth3zzILQerkEFzY7y9fS5kgMjy7Nle_s",
        "sec-ch-ua-platform-version": '"15.5.0"',
        "Sec-GPC": "1",
        "Accept-Language": "en-US,en;q=0.6",
        "Origin": "https://www.instagram.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.instagram.com/?flo=true",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    session.headers.clear()
    session.headers.update(login_headers)
    
    # Step 4: Make login request
    print("🚀 Making login request...")
    
    try:
        response = session.post(
            "https://www.instagram.com/api/v1/web/accounts/login/ajax/",
            data=login_data,
            timeout=30
        )
        
        print(f"📡 Response Status: {response.status_code}")
        
        try:
            response_json = response.json()
            
            # Handle different response types
            if response_json.get('authenticated'):
                print("🎉 LOGIN SUCCESSFUL!")
                print(f"👤 User ID: {response_json.get('userId')}")
                
                # Get session token
                sessionid = session.cookies.get('sessionid')
                if sessionid:
                    print(f"🔑 Session Token: {sessionid}")
                    
                    return {
                        'success': True,
                        'session': session,
                        'sessionid': sessionid,
                        'user_id': response_json.get('userId'),
                        'csrf_token': csrf_token,
                        'cookies': dict(session.cookies)
                    }
                else:
                    print("❌ No session token found in cookies")
                    
            elif response_json.get('message') == 'checkpoint_required':
                checkpoint_url = response_json.get('checkpoint_url')
                print("⚠️  CHECKPOINT REQUIRED")
                print(f"🔗 Checkpoint URL: {checkpoint_url}")
                
                return {
                    'success': False,
                    'checkpoint_required': True,
                    'checkpoint_url': checkpoint_url,
                    'session': session
                }
                
            else:
                print("❌ LOGIN FAILED")
                print(f"📄 Response: {json.dumps(response_json, indent=2)}")
                
                return {
                    'success': False,
                    'response': response_json
                }
                
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response: {response.text}")
            return {'success': False, 'error': 'Invalid JSON response'}
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return {'success': False, 'error': str(e)}

def main():
    """
    Main function with login_details.json persistence
    """
    print("Instagram Login - Environment Configuration")
    print("=" * 60)
    
    # Check if we have saved session data in login_details.json
    saved_session = load_from_login_details()
    if saved_session and saved_session.get('login_successful'):
        print("🔄 Found saved session data in login_details.json!")
        display_session_summary(saved_session)
        
        use_saved = input("\nUse saved session? (y/n): ").lower().strip()
        if use_saved == 'y':
            print("✅ Using saved session data")
            
            # Optionally recreate the session object
            recreate = input("Recreate session object for API calls? (y/n): ").lower().strip()
            if recreate == 'y':
                session = create_session_from_saved_data(saved_session)
                if session:
                    print("🔄 Session object ready for API calls")
            
            return
    
    # Perform fresh login
    result = instagram_login_with_env_encryption()
    
    if result and result.get('success'):
        print("\n🎉 LOGIN SUCCESS!")
        
        # Display session summary
        session_data_for_display = {
            'sessionid': result.get('sessionid'),
            'user_id': result.get('user_id'),
            'csrf_token': result.get('csrf_token'),
            'last_login': datetime.now().isoformat(),
            'login_successful': True,
            'cookies': result.get('cookies', {})
        }
        display_session_summary(session_data_for_display)
        
        # Save to login_details.json
        print("\n💾 Saving session data to login_details.json...")
        save_to_login_details(result)
        
        print("\n📝 Session data saved to login_details.json")
        print("💡 You can now use the saved session for future API calls!")
        
    elif result and result.get('checkpoint_required'):
        print("\n⚠️  CHECKPOINT REQUIRED")
        print("Complete the verification and run again")
        
    else:
        print("\n❌ Login failed")

if __name__ == "__main__":
    main()
