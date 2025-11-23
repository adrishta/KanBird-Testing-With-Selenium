import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

# Initialize driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 30)

try:
    print("KANBIRD LEAD CREATION - EXACT PLUS BUTTON")
    print("=" * 50)

    # Step 1: Login
    print("\n Step 1: Login")
    driver.get("https://app.kanbird.com/login")
    driver.maximize_window()
    time.sleep(3)

    email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
    email_field.send_keys("intern@gmail.com")

    password_field = driver.find_element(By.XPATH, "//input[@type='password']")
    password_field.send_keys("12345678")

    login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_btn.click()
    print(" Logged in")

    time.sleep(10)

    # Handle warnings
    try:
        ok_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]")
        ok_btn.click()
        print(" Warning handled")
        time.sleep(3)
    except:
        pass

    # Step 2: Go to Leads
    print("\n Step 2: Navigate to Leads")
    driver.get("https://app.kanbird.com/leads")
    time.sleep(10)

    print(f"📄 Current page: {driver.current_url}")

    # Step 3: Click the EXACT PLUS button in navigation bar
    print("\n Step 3: Click Navigation Bar PLUS Button")
    time.sleep(5)

    # EXACT SELECTORS for the PLUS button in navigation bar
    plus_clicked = False

    # Strategy 1: PLUS button in the breadcrumb/navigation area
    nav_plus_selectors = [
        # After "Home / Lead / Deal / Sprint /"
        "//nav//button[contains(., '+')]",
        "//div[contains(@class, 'breadcrumb')]//button[contains(., '+')]",
        "//div[contains(text(), 'Home')]//following::button[contains(., '+')]",
        "//*[contains(text(), 'Sprint')]//following::button[1]",

        # In the header section near navigation
        "//header//button[contains(., '+')]",
        "//div[contains(@class, 'header')]//button[contains(., '+')]",

        # Specific to your navigation structure
        "//button[contains(@class, 'btn') and contains(., '+')]",
        "//a[contains(@class, 'btn') and contains(., '+')]"
    ]

    for selector in nav_plus_selectors:
        try:
            elements = driver.find_elements(By.XPATH, selector)
            print(f"Trying: {selector} - Found: {len(elements)}")

            for element in elements:
                try:
                    if element.is_displayed() and element.is_enabled():
                        text = element.text.strip()
                        print(f" Found navigation PLUS: '{text}'")

                        driver.execute_script("arguments[0].scrollIntoView();", element)
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", element)
                        print(" Navigation PLUS button clicked!")
                        plus_clicked = True
                        time.sleep(8)
                        break
                except Exception as e:
                    continue
            if plus_clicked:
                break
        except:
            continue

    # Strategy 2: Look for ANY button in the navigation area
    if not plus_clicked:
        print(" Strategy 2: Any button in navigation area...")
        nav_buttons_selectors = [
            "//nav//button",
            "//div[contains(@class, 'breadcrumb')]//button",
            "//header//button",
            "//div[contains(@class, 'navigation')]//button"
        ]

        for selector in nav_buttons_selectors:
            try:
                buttons = driver.find_elements(By.XPATH, selector)
                print(f"Navigation buttons found: {len(buttons)}")

                for btn in buttons:
                    try:
                        if btn.is_displayed() and btn.is_enabled():
                            btn_text = btn.text.strip()
                            print(f" Navigation button: '{btn_text}'")

                            # If it's a plus or looks like an add button
                            if '+' in btn_text or 'Add' in btn_text or 'New' in btn_text:
                                driver.execute_script("arguments[0].click();", btn)
                                print(" Navigation button clicked!")
                                plus_clicked = True
                                time.sleep(8)
                                break
                    except:
                        continue
                if plus_clicked:
                    break
            except:
                continue

    # Strategy 3: Find by position (should be near the navigation text)
    if not plus_clicked:
        print(" Strategy 3: Finding by position near navigation...")
        try:
            # Find the navigation text first
            nav_elements = driver.find_elements(By.XPATH,
                                                "//*[contains(text(), 'Home') or contains(text(), 'Lead') or contains(text(), 'Deal') or contains(text(), 'Sprint')]")

            for nav_element in nav_elements:
                if nav_element.is_displayed():
                    print(f" Found navigation: {nav_element.text}")

                    # Find buttons near this navigation element
                    nearby_buttons = driver.find_elements(By.XPATH,
                                                          f"//button[preceding::*[contains(text(), '{nav_element.text}')]]")

                    for btn in nearby_buttons:
                        if btn.is_displayed():
                            print(f" Nearby button: '{btn.text}'")
                            driver.execute_script("arguments[0].click();", btn)
                            print(" Nearby button clicked!")
                            plus_clicked = True
                            time.sleep(8)
                            break

                    if plus_clicked:
                        break
        except:
            pass

    if plus_clicked:
        print(" PLUS BUTTON CLICKED SUCCESSFULLY!")
        time.sleep(8)

        # Step 4: Fill Lead Form
        print("\n Step 4: Fill Lead Form")
        time.sleep(5)

        # Test data
        timestamp = str(int(time.time()))
        test_data = {
            'title': f'Auto Lead {timestamp}',
            'start_date': (datetime.now() + timedelta(days=1)).strftime("%m/%d/%Y"),
            'due_date': (datetime.now() + timedelta(days=30)).strftime("%m/%d/%Y"),
            'revenue': '10000',
            'description': f'Automated test lead {timestamp}'
        }

        # Fill Title
        try:
            title_field = driver.find_element(By.XPATH, "//input[@placeholder='Enter title']")
            title_field.clear()
            title_field.send_keys(test_data['title'])
            print(f" Title: {test_data['title']}")
        except:
            print("❌ Title field not found")

        # Fill Start Date
        try:
            start_field = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Start Date')]")
            start_field.clear()
            start_field.send_keys(test_data['start_date'])
            print(f"✅ Start Date: {test_data['start_date']}")
        except:
            print("⚠️ Start Date not found")

        # Fill Due Date
        try:
            due_field = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Due Date')]")
            due_field.clear()
            due_field.send_keys(test_data['due_date'])
            print(f"✅ Due Date: {test_data['due_date']}")
        except:
            print("⚠️ Due Date not found")

        # Fill Revenue
        try:
            revenue_field = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Expected Revenue')]")
            revenue_field.clear()
            revenue_field.send_keys(test_data['revenue'])
            print(f" Revenue: {test_data['revenue']}")
        except:
            print(" Revenue not found")

        # Fill Description
        try:
            desc_field = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
            desc_field.click()
            desc_field.clear()
            desc_field.send_keys(test_data['description'])
            print(" Description filled")
        except:
            try:
                desc_field = driver.find_element(By.XPATH, "//textarea")
                desc_field.clear()
                desc_field.send_keys(test_data['description'])
                print(" Description filled (textarea)")
            except:
                print(" Description not found")

        # Step 5: Save Lead
        print("\n Step 5: Save Lead")
        time.sleep(3)

        save_found = False
        for save_text in ['Save', 'Create', 'Submit']:
            try:
                save_btn = driver.find_element(By.XPATH, f"//button[contains(text(), '{save_text}')]")
                if save_btn.is_enabled():
                    driver.execute_script("arguments[0].click();", save_btn)
                    print(f" {save_text} button clicked!")
                    save_found = True
                    time.sleep(10)
                    break
            except:
                continue

        if save_found:
            print("SUCCESS! Lead created successfully!")
        else:
            print("Could not save lead")

    else:
        print("FAILED: Could not find navigation PLUS button")
        print(" Debug info:")

        # Show navigation elements
        print("\n Navigation elements found:")
        nav_elements = driver.find_elements(By.XPATH,
                                            "//*[contains(text(), 'Home') or contains(text(), 'Lead') or contains(text(), 'Deal') or contains(text(), 'Sprint')]")
        for elem in nav_elements:
            if elem.is_displayed():
                print(f"  - '{elem.text}'")

        # Take screenshot
        driver.save_screenshot("navigation_debug.png")
        print(" Screenshot saved: navigation_debug.png")

except Exception as e:
    print(f" ERROR: {e}")
    import traceback

    print(f"Details: {traceback.format_exc()}")

finally:
    print("\n" + "=" * 50)
    print(" AUTOMATION COMPLETED")
    print("=" * 50)
    input("Press Enter to close browser...")
    driver.quit()