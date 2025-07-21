import os
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

def extract_session_data_from_cookies(driver):
    cookies = driver.get_cookies()
    cookie_dict = {c['name']: c['value'] for c in cookies}
    return {
        'sessionid': cookie_dict.get('sessionid'),
        'user_id': cookie_dict.get('ds_user_id'),
        'csrf_token': cookie_dict.get('csrftoken'),
        'cookies': cookie_dict,
        'success': True
    }

def save_to_login_details(session_data, filename="login_details.json"):
    try:
        login_details = {}
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    login_details = json.load(f)
            except Exception:
                login_details = {}

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
        with open(filename, 'w') as f:
            json.dump(login_details, f, indent=2)
        print(f"💾 Session data saved to: {filename}")
        print(f"📅 Last login timestamp: {login_details['session_info']['last_login']}")
        return True
    except Exception as e:
        print(f"❌ Failed to save to login details: {e}")
        return False

def instagram_login_with_selenium():
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        print("❌ Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env")
        return

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.instagram.com/accounts/login/")

    time.sleep(3)

    try:
        accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Only allow essential cookies')]")
        accept_btn.click()
        time.sleep(1)
    except Exception:
        pass

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)

    try:
        not_now_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        not_now_btn.click()
        time.sleep(1)
    except Exception:
        pass

    try:
        not_now_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        not_now_btn.click()
        time.sleep(1)
    except Exception:
        pass

    # --- Save credentials in original format ---
    session_data = extract_session_data_from_cookies(driver)
    save_to_login_details(session_data)

    print("✅ Login completed. Credentials saved in original format.")
    # driver.quit()  # Uncomment to close browser

if __name__ == "__main__":
    instagram_login_with_selenium()
