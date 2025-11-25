# Kanbird New Sprint Creation Testing - Fixed Version
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

# Initialize driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)


def generate_sprint_title():
    """Generate unique sprint title with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"Test_Sprint_{timestamp}"


def get_future_dates():
    """Get start and end dates for the new sprint"""
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(days=14)  # 2-week sprint
    return start_date.strftime("%m/%d/%Y"), end_date.strftime("%m/%d/%Y")


def safe_clear_and_send_keys(element, text):
    """Safely clear and send keys to an element"""
    try:
        # Method 1: Try normal clear and send keys
        element.clear()
        element.send_keys(text)
        return True
    except:
        try:
            # Method 2: Use Ctrl+A to select all and then type
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(text)
            return True
        except:
            try:
                # Method 3: Click and use JavaScript to set value
                driver.execute_script("arguments[0].value = arguments[1];", element, text)
                return True
            except:
                return False


def handle_date_field(date_field, date_value):
    """Handle date field input with multiple strategies"""
    print(f"Attempting to set date: {date_value}")

    # Strategy 1: Try direct input
    try:
        if safe_clear_and_send_keys(date_field, date_value):
            print("Date set using direct input")
            return True
    except Exception as e:
        print(f"Direct input failed: {e}")

    # Strategy 2: Try JavaScript injection
    try:
        driver.execute_script("arguments[0].value = arguments[1];", date_field, date_value)
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", date_field)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", date_field)
        print("Date set using JavaScript")
        return True
    except Exception as e:
        print(f"JavaScript injection failed: {e}")

    # Strategy 3: Try clicking and using keyboard
    try:
        date_field.click()
        time.sleep(1)
        date_field.send_keys(Keys.CONTROL + "a")
        date_field.send_keys(date_value)
        date_field.send_keys(Keys.ENTER)
        print("Date set using click and keyboard")
        return True
    except Exception as e:
        print(f"Click and keyboard failed: {e}")

    return False


try:
    print("Starting Kanbird New Sprint Creation Testing...")

    # Step 1: Login to Kanbird
    print("\nStep 1: Logging into Kanbird...")
    driver.get("https://app.kanbird.com/login")
    driver.maximize_window()
    time.sleep(3)

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
    time.sleep(8)

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

    # Wait for navigation to home/dashboard
    print("\nWaiting for navigation after login...")
    time.sleep(10)

    # Step 3: Navigate to Sprint Backlog
    print("\nStep 3: Navigating to Sprint Backlog section...")

    # Try direct URL access first
    print("Accessing Sprint Backlog directly...")
    driver.get("https://app.kanbird.com/sprint/sprint-backlog")
    print("Directly accessed Sprint Backlog URL")

    # Wait for Sprint Backlog to load
    print("\nWaiting for Sprint Backlog to load...")
    time.sleep(8)

    # Step 4: Create New Sprint
    print("\nStep 4: Creating New Sprint...")

    # Look for "Create New Sprint" button
    create_sprint_buttons = driver.find_elements(By.XPATH,
                                                 "//button[contains(text(), 'Create New Sprint')] | " +
                                                 "//button[contains(text(), 'Create new sprint')] | " +
                                                 "//*[contains(text(), 'Create New Sprint')]")

    if create_sprint_buttons:
        print("Found Create New Sprint button")
        driver.execute_script("arguments[0].click();", create_sprint_buttons[0])
        print("Clicked Create New Sprint button")
    else:
        print("Create New Sprint button not found, trying alternative methods...")
        # Try other possible selectors
        alternative_selectors = [
            "//button[contains(@class, 'btn')]",
            "//button[contains(text(), 'Create')]",
            "//button[contains(text(), 'New')]",
            "//div[contains(text(), 'Create New Sprint')]"
        ]

        for selector in alternative_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and ("create" in element.text.lower() or "new" in element.text.lower()):
                        driver.execute_script("arguments[0].click();", element)
                        print(f"Clicked button with text: {element.text}")
                        break
            except:
                continue

    # Wait for create sprint modal to appear
    print("Waiting for create sprint modal...")
    time.sleep(5)

    # Step 5: Fill Sprint Creation Form
    print("\nStep 5: Filling Sprint Creation Form...")

    # Generate unique sprint data
    sprint_title = generate_sprint_title()
    start_date, end_date = get_future_dates()
    sprint_goal = "Automated test sprint created by selenium automation"

    print(f"Sprint Title: {sprint_title}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Sprint Goal: {sprint_goal}")

    # Fill Title field
    print("Filling title field...")
    title_fields = driver.find_elements(By.XPATH,
                                        "//input[@placeholder='Enter title'] | " +
                                        "//input[contains(@placeholder, 'title')] | " +
                                        "//input[@name='title'] | " +
                                        "//label[contains(text(), 'Title')]/following-sibling::input")

    if title_fields:
        title_field = title_fields[0]
        if safe_clear_and_send_keys(title_field, sprint_title):
            print("✓ Title field filled successfully")
        else:
            print("✗ Failed to fill title field")
    else:
        print("✗ Title field not found")

    # Fill Start Date field
    print("Filling start date field...")
    start_date_fields = driver.find_elements(By.XPATH,
                                             "//input[@placeholder='Select Start Date'] | " +
                                             "//input[contains(@placeholder, 'Start Date')] | " +
                                             "//input[@name='startDate'] | " +
                                             "//label[contains(text(), 'Start Date')]/following-sibling::input | " +
                                             "//input[@type='date'] | " +
                                             "//input[contains(@class, 'date')]")

    if start_date_fields:
        start_date_field = start_date_fields[0]
        if handle_date_field(start_date_field, start_date):
            print("✓ Start date field filled successfully")
        else:
            print("✗ Failed to fill start date field")
            # Try alternative date format (YYYY-MM-DD)
            alt_start_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            if handle_date_field(start_date_field, alt_start_date):
                print("✓ Start date field filled with alternative format")
    else:
        print("✗ Start date field not found")

    # Fill End Date field
    print("Filling end date field...")
    end_date_fields = driver.find_elements(By.XPATH,
                                           "//input[@placeholder='Select End Date'] | " +
                                           "//input[contains(@placeholder, 'End Date')] | " +
                                           "//input[@name='endDate'] | " +
                                           "//label[contains(text(), 'End Date')]/following-sibling::input | " +
                                           "//input[@type='date'] | " +
                                           "//input[contains(@class, 'date')]")

    if end_date_fields:
        end_date_field = end_date_fields[0]
        if handle_date_field(end_date_field, end_date):
            print("✓ End date field filled successfully")
        else:
            print("✗ Failed to fill end date field")
            # Try alternative date format (YYYY-MM-DD)
            alt_end_date = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
            if handle_date_field(end_date_field, alt_end_date):
                print("✓ End date field filled with alternative format")
    else:
        print("✗ End date field not found")

    # Fill Sprint Goal field
    print("Filling sprint goal field...")
    goal_fields = driver.find_elements(By.XPATH,
                                       "//textarea[@placeholder='Enter description'] | " +
                                       "//textarea[contains(@placeholder, 'description')] | " +
                                       "//textarea[@name='goal'] | " +
                                       "//textarea[contains(@placeholder, 'Sprint Goal')] | " +
                                       "//label[contains(text(), 'Sprint Goal')]/following-sibling::textarea")

    if goal_fields:
        goal_field = goal_fields[0]
        if safe_clear_and_send_keys(goal_field, sprint_goal):
            print("✓ Sprint goal field filled successfully")
        else:
            print("✗ Failed to fill sprint goal field")
    else:
        print("✗ Sprint goal field not found")

    # Take screenshot after filling form
    driver.save_screenshot("sprint_form_filled.png")
    print("Screenshot of filled form saved as 'sprint_form_filled.png'")

    # Step 6: Save the Sprint
    print("\nStep 6: Saving the Sprint...")

    # Look for Save button
    save_buttons = driver.find_elements(By.XPATH,
                                        "//button[contains(text(), 'Save')] | " +
                                        "//button[@type='submit'] | " +
                                        "//button[contains(@class, 'btn-primary')]")

    save_success = False
    if save_buttons:
        for button in save_buttons:
            if button.is_displayed() and ("save" in button.text.lower() or "submit" in button.text.lower()):
                print("Found save button, clicking...")
                driver.execute_script("arguments[0].click();", button)
                print("Save button clicked")
                save_success = True
                break
    else:
        print("Save button not found")

    # Wait for sprint creation to complete
    print("Waiting for sprint creation to complete...")
    time.sleep(8)

    # Step 7: Verify Sprint Creation
    print("\nStep 7: Verifying Sprint Creation...")

    verification_tests = []

    # Check if we're back on sprint backlog page
    current_url = driver.current_url
    if "sprint-backlog" in current_url or "sprint" in current_url:
        verification_tests.append("✓ Returned to sprint page after creation")
        print("✓ Returned to sprint page after creation")
    else:
        verification_tests.append(f"✗ Unexpected page after creation: {current_url}")
        print(f"✗ Unexpected page after creation: {current_url}")

    # Check if new sprint appears in the list
    try:
        # Look for the newly created sprint in the list
        new_sprint_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{sprint_title}')]")
        if new_sprint_elements:
            verification_tests.append(f"✓ New sprint '{sprint_title}' found in list")
            print(f"✓ New sprint '{sprint_title}' found in list")
        else:
            verification_tests.append(f"✗ New sprint '{sprint_title}' not found in list")
            print(f"✗ New sprint '{sprint_title}' not found in list")
    except Exception as e:
        verification_tests.append(f"✗ Error verifying sprint in list: {str(e)}")
        print(f"✗ Error verifying sprint in list: {str(e)}")

    # Check for success message or notification
    try:
        success_messages = driver.find_elements(By.XPATH,
                                                "//*[contains(text(), 'success')] | " +
                                                "//*[contains(text(), 'created')] | " +
                                                "//*[contains(@class, 'success')] | " +
                                                "//*[contains(@class, 'alert-success')] | " +
                                                "//*[contains(text(), 'Success')]")

        if success_messages:
            verification_tests.append("✓ Success message displayed")
            print("✓ Success message displayed")
        else:
            verification_tests.append("✗ No success message detected")
            print("✗ No success message detected")
    except Exception as e:
        verification_tests.append(f"✗ Error checking success message: {str(e)}")
        print(f"✗ Error checking success message: {str(e)}")

    # Take screenshot for verification
    driver.save_screenshot("new_sprint_creation_results.png")
    print("Screenshot saved as 'new_sprint_creation_results.png'")

    # Final Summary
    print(f"\n{'=' * 50}")
    print("NEW SPRINT CREATION TEST SUMMARY")
    print(f"{'=' * 50}")
    print(f"Sprint Title: {sprint_title}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Save Button Clicked: {save_success}")
    print(f"Verification Tests: {len(verification_tests)} checks performed")

    for test in verification_tests:
        print(f" - {test}")

    # Final verdict
    success_count = sum(1 for test in verification_tests if "✓" in test)

    if success_count >= 2 and save_success:
        print(f"\n{'=' * 50}")
        print("NEW SPRINT CREATION TEST: PASSED ✓")
        print("Successfully created new sprint")
        print(f"{'=' * 50}")
    else:
        print(f"\n{'=' * 50}")
        print("NEW SPRINT CREATION TEST: FAILED ✗")
        print("Issues encountered during sprint creation")
        print(f"{'=' * 50}")

    print("\nAutomation finished!")
    input("Press Enter to close browser...")

except Exception as e:
    print(f"Error during automation: {str(e)}")
    import traceback

    traceback.print_exc()

    # Additional troubleshooting
    try:
        print("\nTroubleshooting current state:")
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")

        # Take screenshot for debugging
        driver.save_screenshot("sprint_creation_error.png")
        print("Error screenshot saved as 'sprint_creation_error.png'")

    except Exception as troubleshoot_error:
        print(f"Troubleshooting failed: {troubleshoot_error}")

finally:
    driver.quit()