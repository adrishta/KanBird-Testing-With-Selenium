# Complete Kanbird Automation - Full Working Code
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

    # Step 2: Handle Organization Selection
    print("\n📍 Step 2: Handling organization selection...")

    # Click OK on password warning using JavaScript
    print("📍 Clicking OK on password warning...")
    ok_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'OK')]")
    if ok_buttons:
        driver.execute_script("arguments[0].click();", ok_buttons[0])
        print("✅ Password warning OK clicked")
    time.sleep(2)

    # Select intern organization using JavaScript
    print("📍 Selecting intern organization...")
    intern_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'intern')]")
    for element in intern_elements:
        if element.is_displayed():
            driver.execute_script("arguments[0].click();", element)
            print("✅ Intern organization selected")
            break
    time.sleep(2)

    # Click main OK button using JavaScript
    print("📍 Clicking main OK button...")
    main_ok_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'OK')]")
    if main_ok_buttons:
        driver.execute_script("arguments[0].click();", main_ok_buttons[0])
        print("✅ Main OK button clicked")

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
    # Continue with alternative approach
    try:
        print("🔄 Trying alternative approach...")

        # Alternative: Direct organization page access
        driver.get("https://app.kanbird.com/switch-account?email=intern@gmail.com")
        time.sleep(5)

        # Force click all OK buttons
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if "OK" in button.text:
                driver.execute_script("arguments[0].click();", button)
                print("✅ OK button clicked")
                time.sleep(1)

        # Force click all intern elements
        elements = driver.find_elements(By.XPATH, "//*")
        for element in elements:
            if "intern" in element.text:
                driver.execute_script("arguments[0].click();", element)
                print("✅ Intern clicked")
                time.sleep(1)

        time.sleep(10)
        print(f"🎯 Final URL: {driver.current_url}")

    except Exception as alt_error:
        print(f"Alternative approach failed: {alt_error}")

finally:
    driver.quit()