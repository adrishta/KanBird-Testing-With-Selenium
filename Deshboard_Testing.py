# Kanbird CRM Dashboard Direct Access Testing
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
    print("Starting Kanbird CRM Dashboard Direct Access Testing...")

    # Step 1: Direct access to CRM Dashboard
    print("\nStep 1: Direct access to CRM Dashboard...")
    driver.get("https://app.kanbird.com/crm-dashboard")
    driver.maximize_window()
    time.sleep(5)

    # Check if we need to login (redirected to login page)
    current_url = driver.current_url
    print(f"Current URL: {current_url}")

    if "login" in current_url:
        print("Redirected to login page, performing login...")

        # Enter email
        email_field = driver.find_element(By.XPATH, "//input[@type='email']")
        email_field.send_keys("intern@gmail.com")
        print("Email entered")

        # Enter password
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.send_keys("12345678")
        print("Password entered")

        # Click login button
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_btn.click()
        print("Login button clicked")

        # Wait for organization page
        print("\nWaiting for organization selection page...")
        time.sleep(10)

        # Step 2: Handle Organization Selection
        print("\nStep 2: Handling organization selection...")

        # Click OK on password warning using JavaScript
        print("Clicking OK on password warning...")
        ok_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'OK')]")
        if ok_buttons:
            driver.execute_script("arguments[0].click();", ok_buttons[0])
            print("Password warning OK clicked")
        time.sleep(2)

        # Select intern organization using JavaScript
        print("Selecting intern organization...")
        intern_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'intern')]")
        for element in intern_elements:
            if element.is_displayed():
                driver.execute_script("arguments[0].click();", element)
                print("Intern organization selected")
                break
        time.sleep(2)

        # Click main OK button using JavaScript
        print("Clicking main OK button...")
        main_ok_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'OK')]")
        if main_ok_buttons:
            driver.execute_script("arguments[0].click();", main_ok_buttons[0])
            print("Main OK button clicked")

        # Wait for navigation
        print("\nWaiting for navigation after login...")
        time.sleep(10)

        # Step 3: Check if we landed on CRM Dashboard or Home
        current_url_after_login = driver.current_url
        print(f"URL after login: {current_url_after_login}")

        if "crm-dashboard" not in current_url_after_login:
            print("Not on CRM Dashboard after login, redirecting...")

            # Directly navigate to CRM Dashboard
            driver.get("https://app.kanbird.com/crm-dashboard")
            time.sleep(8)

            print(f"URL after direct CRM Dashboard access: {driver.current_url}")

    # Step 4: Test CRM Dashboard Elements
    print("\nStep 4: Testing CRM Dashboard Elements...")

    final_url = driver.current_url
    print(f"Final URL: {final_url}")

    # Verify CRM dashboard elements
    print("\nTesting CRM Dashboard elements...")

    expected_elements = [
        "Home",
        "Dashboard",
        "Leads",
        "Deals",
        "Tickets",
        "My Board",
        "My Task",
        "Sprint",
        "Calendar",
        "Todes",
        "Teams",
        "Notes",
        "People",
        "Filter",
        "Project"
    ]

    found_elements = []
    missing_elements = []

    for element_text in expected_elements:
        try:
            elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{element_text}')]")
            if elements:
                found_elements.append(element_text)
                print(f"Found: {element_text}")
            else:
                missing_elements.append(element_text)
                print(f"Not found: {element_text}")
        except:
            missing_elements.append(element_text)
            print(f"Error searching for: {element_text}")

    # Step 5: Test Dashboard Functionality
    print("\nStep 5: Testing Dashboard Functionality...")

    functionality_tests = []

    # Test 1: Check if we're actually on CRM Dashboard
    if "crm-dashboard" in final_url:
        functionality_tests.append("Successfully accessed CRM Dashboard URL")
        print("Successfully accessed CRM Dashboard URL")
    else:
        functionality_tests.append(f"Not on CRM Dashboard, current page: {final_url}")
        print(f"Not on CRM Dashboard, current page: {final_url}")

    # Test 2: Check for CRM specific elements
    crm_modules = ["Leads", "Deals", "Tickets"]
    crm_found = []

    for module in crm_modules:
        if module in found_elements:
            crm_found.append(module)

    if crm_found:
        functionality_tests.append(f"CRM modules found: {crm_found}")
        print(f"CRM modules found: {crm_found}")
    else:
        functionality_tests.append("No CRM modules found")
        print("No CRM modules found")

    # Test 3: Check if dashboard is interactive
    try:
        # Try to find clickable elements
        clickable_elements = driver.find_elements(By.XPATH, "//a | //button | //div[@onclick]")
        if len(clickable_elements) > 10:
            functionality_tests.append(f"Dashboard has {len(clickable_elements)} interactive elements")
            print(f"Dashboard has {len(clickable_elements)} interactive elements")
        else:
            functionality_tests.append("Limited interactive elements found")
            print("Limited interactive elements found")
    except:
        functionality_tests.append("Could not check interactivity")
        print("Could not check interactivity")

    # Summary
    print(f"\nCRM Dashboard Test Summary:")
    print(f"Final URL: {final_url}")
    print(f"Found {len(found_elements)} out of {len(expected_elements)} elements")
    print(f"Missing elements: {missing_elements}")
    print(f"Functionality tests: {len(functionality_tests)} checks performed")

    for test in functionality_tests:
        print(f" - {test}")

    # Take screenshot for verification
    driver.save_screenshot("crm_dashboard_direct_access.png")
    print("Screenshot saved as 'crm_dashboard_direct_access.png'")

    # Final status
    if ("crm-dashboard" in final_url and
            len(found_elements) >= 10 and
            "Leads" in found_elements and
            "Deals" in found_elements):
        print("\nCRM DASHBOARD DIRECT ACCESS TEST: PASSED")
        print("Successfully accessed CRM Dashboard directly")
    else:
        print("\nCRM DASHBOARD DIRECT ACCESS TEST: FAILED")
        print("Could not access CRM Dashboard directly")

        # Additional troubleshooting
        print("\nTroubleshooting Info:")
        print(f"Are we on CRM Dashboard URL: {'crm-dashboard' in final_url}")
        print(f"CRM modules found: {crm_found}")
        print(f"Total elements found: {len(found_elements)}")

    print("\nAutomation finished!")
    input("Press Enter to close browser...")

except Exception as e:
    print(f"Error during automation: {str(e)}")

    # Additional troubleshooting
    try:
        print("\nTroubleshooting current state:")
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")

        # Try to get any page source info
        page_source = driver.page_source
        if "kanbird" in page_source.lower():
            print("Kanbird page detected")
        if "login" in page_source.lower():
            print("Login page detected")
        if "dashboard" in page_source.lower():
            print("Dashboard content detected")

    except Exception as troubleshoot_error:
        print(f"Troubleshooting failed: {troubleshoot_error}")

finally:
    driver.quit()