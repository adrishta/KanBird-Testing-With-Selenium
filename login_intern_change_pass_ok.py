# Complete Kanbird Automation - Fixed Warning Message
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Initialize driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

try:
    print("🚀 Starting Complete Kanbird Automation...")

    # Step 1: Login to Kanbird
    print("\n📍 Step 1: Logging in to Kanbird...")
    driver.get("https://app.kanbird.com/login")
    driver.maximize_window()
    time.sleep(5)

    # Enter email
    email_field = driver.find_element(By.XPATH, "//input[@type='email']")
    email_field.send_keys("intern@gmail.com")
    print("✅ Email entered")

    # Enter password
    password_field = driver.find_element(By.XPATH, "//input[@type='password']")
    password_field.send_keys("12345678")
    print("✅ Password entered")

    # Click login button
    login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_btn.click()
    print("✅ Login button clicked")

    # Wait for organization page
    print("\n⏳ Waiting for organization selection page...")
    time.sleep(10)

    # Step 2: Handle Warning Message First
    print("\n📍 Step 2: Handling warning message...")

    # Wait for warning message to appear
    time.sleep(3)

    # Try multiple methods to click OK on warning
    warning_handled = False

    # Method 1: Try normal click
    try:
        ok_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'OK')]")
        for btn in ok_buttons:
            if btn.is_displayed():
                btn.click()
                print("✅ Warning OK clicked (normal click)")
                warning_handled = True
                break
    except:
        pass

    # Method 2: Try JavaScript click
    if not warning_handled:
        try:
            ok_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'OK')]")
            for btn in ok_buttons:
                driver.execute_script("arguments[0].click();", btn)
                print("✅ Warning OK clicked (JavaScript)")
                warning_handled = True
                break
        except:
            pass

    # Method 3: Try Enter key
    if not warning_handled:
        try:
            from selenium.webdriver.common.keys import Keys

            driver.switch_to.active_element.send_keys(Keys.ENTER)
            print("✅ Warning handled (Enter key)")
            warning_handled = True
        except:
            pass

    if warning_handled:
        print("✅ Warning message handled successfully")
    else:
        print("⚠️ Could not handle warning message, continuing...")

    time.sleep(3)

    # Step 3: Select Organization
    print("\n📍 Step 3: Selecting organization...")

    # Select intern organization
    intern_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'intern')]")
    for element in intern_elements:
        if element.is_displayed():
            driver.execute_script("arguments[0].click();", element)
            print("✅ Intern organization selected")
            break
    time.sleep(2)

    # Step 4: Click Main OK Button
    print("📍 Clicking main OK button...")

    # Wait a bit before clicking main OK
    time.sleep(2)

    main_ok_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'OK')]")
    if main_ok_buttons:
        for btn in main_ok_buttons:
            if btn.is_displayed():
                driver.execute_script("arguments[0].click();", btn)
                print("✅ Main OK button clicked")
                break

    # Wait for navigation
    print("\n⏳ Waiting for navigation to next page...")
    time.sleep(10)

    # Final result
    final_url = driver.current_url
    print(f"🎯 Final URL: {driver.current_url}")

    if "dashboard" in final_url or "workspace" in final_url:
        print("🎉 SUCCESS! You are now on Kanbird dashboard!")
    else:
        print("✅ Process completed!")

    print("\n✅ Automation finished!")
    input("Press Enter to close browser...")

except Exception as e:
    print(f"❌ Error: {str(e)}")

finally:
    driver.quit()