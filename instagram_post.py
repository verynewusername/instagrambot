import os
import requests
import json
import time
import base64
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def upload_image_to_instagram(session, image_path, upload_id):
    """
    Upload image file to Instagram's servers
    """
    print(f"📤 Uploading image: {image_path}")
    
    # Read and encode image
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Get image dimensions (you might want to add proper image dimension detection)
    # For now, using 512x512 as in your example
    width, height = 512, 512
    
    # Prepare upload headers
    upload_headers = {
        'Host': 'i.instagram.com',
        'Connection': 'keep-alive',
        'X-Instagram-Rupload-Params': json.dumps({
            "media_type": 1,
            "upload_id": upload_id,
            "upload_media_height": height,
            "upload_media_width": width
        }),
        'X-Instagram-AJAX': '1023572446',
        'sec-ch-ua-platform': '"macOS"',
        'X-Web-Session-ID': '9m0l9s:d48dze:k8lyo0',
        'Offset': '0',
        'sec-ch-ua': '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'X-Entity-Length': str(len(image_data)),
        'X-IG-App-ID': '936619743392459',
        'X-ASBD-ID': '359341',
        'X-Entity-Type': 'image/jpeg',
        'X-Entity-Name': f'fb_uploader_{upload_id}',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Sec-GPC': '1',
        'Accept-Language': 'en-US,en;q=0.6',
        'Origin': 'https://www.instagram.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.instagram.com/',
        'Content-Type': 'image/jpeg'
    }
    
    # Upload image
    upload_url = f'https://i.instagram.com/rupload_igphoto/fb_uploader_{upload_id}'
    
    try:
        response = session.post(
            upload_url,
            headers=upload_headers,
            data=image_data,
            timeout=30
        )
        
        print(f"📤 Upload Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Image uploaded successfully!")
            return True
        else:
            print(f"❌ Upload failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def configure_instagram_post(session, upload_id, caption="", csrf_token=None):
    """
    Configure and publish the Instagram post
    """
    print(f"📝 Configuring post with caption: '{caption}'")
    
    # Get CSRF token from session if not provided
    if not csrf_token:
        csrf_token = session.cookies.get('csrftoken')
    
    # Prepare post data (from your curl command)
    post_data = {
        'archive_only': 'false',
        'caption': caption,
        'clips_share_preview_to_feed': '1',
        'disable_comments': '0',
        'disable_oa_reuse': 'false',
        'igtv_share_preview_to_feed': '1',
        'is_meta_only_post': '0',
        'is_unified_video': '1',
        'like_and_view_counts_disabled': '0',
        'media_share_flow': 'creation_flow',
        'share_to_facebook': '',
        'share_to_fb_destination_type': 'USER',
        'source_type': 'library',
        'upload_id': upload_id,
        'video_subtitles_enabled': '0',
        'jazoest': '22916'
    }
    
    # Prepare headers (from your curl command)
    configure_headers = {
        'Host': 'www.instagram.com',
        'Connection': 'keep-alive',
        'sec-ch-ua-full-version-list': '"Chromium";v="136.0.0.0", "Brave";v="136.0.0.0", "Not.A/Brand";v="99.0.0.0"',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua': '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-mobile': '?0',
        'X-IG-App-ID': '936619743392459',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': '*/*',
        'X-Instagram-AJAX': '1023572446',
        'X-CSRFToken': csrf_token,
        'X-Web-Session-ID': '9m0l9s:d48dze:k8lyo0',
        'X-ASBD-ID': '359341',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'X-IG-WWW-Claim': 'hmac.AR1NQWcvrEmK3axZth3zzILQerkEFzY7y9fS5kgMjy7Nle_s',
        'sec-ch-ua-platform-version': '"15.5.0"',
        'Sec-GPC': '1',
        'Accept-Language': 'en-US,en;q=0.6',
        'Origin': 'https://www.instagram.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.instagram.com/',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Configure post
    configure_url = 'https://www.instagram.com/api/v1/media/configure/'
    
    try:
        response = session.post(
            configure_url,
            headers=configure_headers,
            data=post_data,
            timeout=30
        )
        
        print(f"📝 Configure Status: {response.status_code}")
        
        try:
            response_json = response.json()
            
            if response_json.get('status') == 'ok':
                print("🎉 POST PUBLISHED SUCCESSFULLY!")
                media_info = response_json.get('media', {})
                print(f"📱 Media ID: {media_info.get('id')}")
                print(f"🔗 Media Code: {media_info.get('code')}")
                
                return {
                    'success': True,
                    'media_id': media_info.get('id'),
                    'media_code': media_info.get('code'),
                    'response': response_json
                }
            else:
                print(f"❌ Post configuration failed: {response_json}")
                return {
                    'success': False,
                    'response': response_json
                }
                
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response: {response.text}")
            return {'success': False, 'error': 'Invalid JSON response'}
            
    except Exception as e:
        print(f"❌ Configure error: {e}")
        return {'success': False, 'error': str(e)}

def post_to_instagram(session, image_path, caption="", csrf_token=None):
    """
    Complete Instagram posting function
    """
    print("📸 Starting Instagram Post Process")
    print("=" * 50)
    
    # Generate upload ID (timestamp-based like Instagram)
    upload_id = str(int(time.time() * 1000))
    print(f"🆔 Upload ID: {upload_id}")
    
    # Step 1: Upload image
    upload_success = upload_image_to_instagram(session, image_path, upload_id)
    if not upload_success:
        return {'success': False, 'error': 'Image upload failed'}
    
    # Small delay between upload and configure
    time.sleep(2)
    
    # Step 2: Configure post
    result = configure_instagram_post(session, upload_id, caption, csrf_token)
    
    return result

def load_session_from_login_details(filename="login_details.json"):
    """
    Load session data and recreate session object
    """
    try:
        with open(filename, 'r') as f:
            login_details = json.load(f)
        
        session_info = login_details.get('session_info')
        if not session_info or not session_info.get('login_successful'):
            print("❌ No valid session found in login details")
            return None, None
        
        # Recreate session
        session = requests.Session()
        
        # Restore cookies
        cookies = session_info.get('cookies', {})
        for name, value in cookies.items():
            session.cookies.set(name, value, domain='.instagram.com')
        
        # Set headers
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "X-IG-App-ID": "936619743392459",
        })
        
        csrf_token = session_info.get('csrf_token')
        
        print("✅ Session loaded from login_details.json")
        return session, csrf_token
        
    except Exception as e:
        print(f"❌ Failed to load session: {e}")
        return None, None

def main():
    """
    Main posting function
    """
    print("Instagram Posting Tool")
    print("=" * 50)
    
    # Load session from saved login details
    session, csrf_token = load_session_from_login_details()
    if not session:
        print("❌ Please run the login script first to save session details")
        return
    
    # Get image path and caption
    image_path = input("📁 Enter image path: ").strip()
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    caption = input("📝 Enter caption (optional): ").strip()
    
    # Post to Instagram
    result = post_to_instagram(session, image_path, caption, csrf_token)
    
    if result.get('success'):
        print("\n🎉 SUCCESS!")
        print("=" * 50)
        print(f"Media ID: {result.get('media_id')}")
        print(f"Media Code: {result.get('media_code')}")
        print("Your post is now live on Instagram! 📱")
    else:
        print(f"\n❌ Posting failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
