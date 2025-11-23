# Kanbird Login with XPath
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Initialize driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 15)

try:
    print("🌐 Opening Kanbird login page...")
    driver.get("https://app.kanbird.com/login")
    driver.maximize_window()
    time.sleep(3)

    # METHOD 1: Direct email/password login (if available)
    print("🔍 Trying direct email/password login...")

    # Email field XPaths
    email_xpaths = [
        "//input[@id='email']",
        "//input[@type='email']",
        "//input[@name='email']",
        "//input[contains(@placeholder, 'email')]",
        "//input[contains(@placeholder, 'Email')]",
        "//input[@id='username']",
        "//input[@name='username']"
    ]

    # Password field XPaths
    password_xpaths = [
        "//input[@type='password']",
        "//input[@name='password']",
        "//input[@id='password']",
        "//input[contains(@placeholder, 'password')]",
        "//input[contains(@placeholder, 'Password')]"
    ]

    # Login button XPaths
    login_button_xpaths = [
        "//button[@type='submit']",
        "//button[contains(text(), 'Login')]",
        "//button[contains(text(), 'Sign In')]",
        "//button[contains(text(), 'Log In')]",
        "//input[@type='submit']",
        "//button[@class='btn']",
        "//button[contains(@class, 'btn-primary')]",
        "//button[contains(@class, 'login')]"
    ]

    # Try email/password login
    email_field = None
    for xpath in email_xpaths:
        try:
            email_field = driver.find_element(By.XPATH, xpath)
            print(f"✅ Found email field: {xpath}")
            email_field.clear()
            email_field.send_keys("intern@gmail.com")
            break
        except:
            continue

    password_field = None
    if email_field:
        for xpath in password_xpaths:
            try:
                password_field = driver.find_element(By.XPATH, xpath)
                print(f"✅ Found password field: {xpath}")
                password_field.clear()
                password_field.send_keys("12345678")
                break
            except:
                continue

    if email_field and password_field:
        for xpath in login_button_xpaths:
            try:
                login_btn = driver.find_element(By.XPATH, xpath)
                print(f"✅ Found login button: {xpath}")
                login_btn.click()
                print("✅ Login button clicked")
                break
            except:
                continue
    else:
        print("❌ Email/password fields not found")

        # METHOD 2: Google OAuth login
        print("\n🔍 Trying Google OAuth login...")

        google_button_xpaths = [
            "//button[contains(., 'Google')]",
            "//div[contains(., 'Google')]",
            "//span[contains(., 'Google')]",
            "//*[contains(text(), 'Google')]",
            "//*[contains(text(), 'Sign in with Google')]",
            "//*[contains(text(), 'Continue with Google')]",
            "//button[contains(@class, 'google')]",
            "//div[contains(@class, 'google')]",
            "//*[@aria-label='Sign in with Google']"
        ]

        for xpath in google_button_xpaths:
            try:
                google_btn = driver.find_element(By.XPATH, xpath)
                print(f"✅ Found Google button: {xpath}")
                google_btn.click()
                print("✅ Google button clicked")

                # Wait for Google OAuth page
                time.sleep(5)

                # Handle Google OAuth
                if "accounts.google.com" in driver.current_url:
                    print("🔍 On Google OAuth page...")

                    # Google email
                    google_email_xpaths = [
                        "//input[@id='identifierId']",
                        "//input[@type='email']",
                        "//input[@name='identifier']"
                    ]

                    for email_xpath in google_email_xpaths:
                        try:
                            gmail_field = wait.until(EC.presence_of_element_located((By.XPATH, email_xpath)))
                            gmail_field.send_keys("intern@gmail.com")
                            print(f"✅ Google email entered: {email_xpath}")
                            break
                        except:
                            continue

                    # Google Next button
                    google_next_xpaths = [
                        "//span[contains(., 'Next')]",
                        "//button[contains(., 'Next')]",
                        "//div[contains(., 'Next')]"
                    ]

                    for next_xpath in google_next_xpaths:
                        try:
                            next_btn = driver.find_element(By.XPATH, next_xpath)
                            next_btn.click()
                            print("✅ Google Next button clicked")
                            break
                        except:
                            continue

                    # Wait for password page
                    time.sleep(5)

                    # Google password
                    google_password_xpaths = [
                        "//input[@name='Passwd']",
                        "//input[@type='password']",
                        "//input[@name='password']"
                    ]

                    for pwd_xpath in google_password_xpaths:
                        try:
                            pwd_field = wait.until(EC.presence_of_element_located((By.XPATH, pwd_xpath)))
                            pwd_field.send_keys("12345678")
                            print(f"✅ Google password entered: {pwd_xpath}")
                            break
                        except:
                            continue

                    # Final sign in
                    for next_xpath in google_next_xpaths:
                        try:
                            signin_btn = driver.find_element(By.XPATH, next_xpath)
                            signin_btn.click()
                            print("✅ Google Sign In clicked")
                            break
                        except:
                            continue

                break
            except:
                continue

    # Wait for login result
    print("\n⏳ Waiting for login result...")
    time.sleep(10)

    # Check if login successful
    current_url = driver.current_url
    print(f"🔗 Current URL: {current_url}")

    if "login" not in current_url and current_url != "https://app.kanbird.com/login":
        print("🎉 Login successful!")
    else:
        print("❌ Login may have failed")

        # METHOD 3: Try any clickable element that might be login
        print("\n🔍 Trying alternative login methods...")

        alternative_xpaths = [
            "//*[contains(text(), 'Continue')]",
            "//*[contains(text(), 'Get Started')]",
            "//*[contains(text(), 'Start')]",
            "//*[contains(@class, 'login-btn')]",
            "//*[contains(@class, 'signin-btn')]",
            "//a[contains(text(), 'Login')]",
            "//a[contains(text(), 'Sign In')]"
        ]

        for xpath in alternative_xpaths:
            try:
                alt_btn = driver.find_element(By.XPATH, xpath)
                print(f"✅ Found alternative button: {xpath}")
                alt_btn.click()
                print("✅ Alternative button clicked")
                break
            except:
                continue

    # Final check
    time.sleep(5)
    print(f"🎯 Final URL: {driver.current_url}")
    print(f"🎯 Final Title: '{driver.title}'")

    # Keep browser open
    input("\nPress Enter to close browser...")

except Exception as e:
    print(f"❌ Error: {str(e)}")

finally:
    driver.quit()