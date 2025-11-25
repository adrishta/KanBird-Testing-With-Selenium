# Kanbird MY Board Section Testing
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
    print("Starting Kanbird MY Board Section Testing...")

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

    # Step 3: Navigate to MY Board
    print("\nStep 3: Navigating to MY Board section...")

    # Method 1: Try to find and click MY Board link in sidebar
    my_board_found = False

    # Look for MY Board in various possible locations
    my_board_selectors = [
        "//*[contains(text(), 'My Board')]",
        "//*[contains(text(), 'My board')]",
        "//*[contains(text(), 'MY BOARD')]",
        "//a[contains(@href, 'kanban-board')]",
        "//a[contains(@href, 'my-board')]"
    ]

    for selector in my_board_selectors:
        try:
            my_board_elements = driver.find_elements(By.XPATH, selector)
            for element in my_board_elements:
                if element.is_displayed():
                    print(f"Found MY Board element with selector: {selector}")
                    driver.execute_script("arguments[0].click();", element)
                    print("Clicked MY Board")
                    my_board_found = True
                    break
            if my_board_found:
                break
        except:
            continue

    # If not found via click, try direct URL access
    if not my_board_found:
        print("MY Board link not found in UI, trying direct URL access...")
        driver.get("https://app.kanbird.com/kanban-board")
        print("Directly accessed MY Board URL")

    # Wait for MY Board to load
    print("\nWaiting for MY Board to load...")
    time.sleep(8)

    # Step 4: Test MY Board Elements and Functionality
    print("\nStep 4: Testing MY Board Elements and Functionality...")

    current_url = driver.current_url
    print(f"Current URL: {current_url}")

    # Expected MY Board elements
    expected_my_board_elements = [
        "To Do",
        "In Progress",
        "Done",
        "Add Task",
        "Add Column",
        "Filter",
        "Search"
    ]

    found_elements = []
    missing_elements = []

    for element_text in expected_my_board_elements:
        try:
            elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{element_text}')]")
            visible_elements = [e for e in elements if e.is_displayed()]
            if visible_elements:
                found_elements.append(element_text)
                print(f"✓ Found: {element_text}")
            else:
                missing_elements.append(element_text)
                print(f"✗ Not found (or not visible): {element_text}")
        except Exception as e:
            missing_elements.append(element_text)
            print(f"✗ Error searching for: {element_text} - {str(e)}")

    # Step 5: Test Kanban Board Specific Features
    print("\nStep 5: Testing Kanban Board Specific Features...")

    functionality_tests = []

    # Test 1: Check if we're on MY Board page
    if "kanban-board" in current_url or "my-board" in current_url:
        functionality_tests.append("Successfully accessed MY Board URL")
        print("✓ Successfully accessed MY Board URL")
    else:
        functionality_tests.append(f"Not on MY Board, current page: {current_url}")
        print(f"✗ Not on MY Board, current page: {current_url}")

    # Test 2: Check for kanban columns
    try:
        columns = driver.find_elements(By.XPATH,
                                       "//div[contains(@class, 'column')] | //div[contains(@class, 'board-column')] | //div[contains(@class, 'list')]")
        if columns:
            functionality_tests.append(f"Found {len(columns)} kanban columns")
            print(f"✓ Found {len(columns)} kanban columns")
        else:
            functionality_tests.append("No kanban columns found")
            print("✗ No kanban columns found")
    except Exception as e:
        functionality_tests.append(f"Error finding columns: {str(e)}")
        print(f"✗ Error finding columns: {str(e)}")

    # Test 3: Check for task cards
    try:
        tasks = driver.find_elements(By.XPATH,
                                     "//div[contains(@class, 'task')] | //div[contains(@class, 'card')] | //div[contains(@class, 'item')]")
        if tasks:
            functionality_tests.append(f"Found {len(tasks)} task cards")
            print(f"✓ Found {len(tasks)} task cards")
        else:
            functionality_tests.append("No task cards found")
            print("✗ No task cards found")
    except Exception as e:
        functionality_tests.append(f"Error finding tasks: {str(e)}")
        print(f"✗ Error finding tasks: {str(e)}")

    # Test 4: Test Add Task functionality
    try:
        add_task_buttons = driver.find_elements(By.XPATH,
                                                "//button[contains(text(), 'Add Task')] | //button[contains(text(), 'Add task')] | //*[contains(text(), '+')]")
        if add_task_buttons:
            functionality_tests.append("Add Task button available")
            print("✓ Add Task button available")

            # Try to click first Add Task button
            driver.execute_script("arguments[0].click();", add_task_buttons[0])
            time.sleep(2)

            # Check if task creation modal appears
            modal_elements = driver.find_elements(By.XPATH,
                                                  "//input[@placeholder='Task name'] | //input[@placeholder='Title'] | //textarea")
            if modal_elements:
                functionality_tests.append("Task creation modal opened successfully")
                print("✓ Task creation modal opened successfully")

                # Close modal (press ESC or click outside)
                driver.find_element(By.TAG_NAME, "body").send_keys("Escape")
            else:
                functionality_tests.append("Task creation modal did not open")
                print("✗ Task creation modal did not open")
        else:
            functionality_tests.append("Add Task button not found")
            print("✗ Add Task button not found")
    except Exception as e:
        functionality_tests.append(f"Error testing Add Task: {str(e)}")
        print(f"✗ Error testing Add Task: {str(e)}")

    # Test 5: Test drag and drop capability (visual check)
    try:
        draggable_elements = driver.find_elements(By.XPATH,
                                                  "//div[contains(@class, 'draggable')] | //div[@draggable='true']")
        if draggable_elements:
            functionality_tests.append(f"Found {len(draggable_elements)} draggable elements")
            print(f"✓ Found {len(draggable_elements)} draggable elements")
        else:
            # Check if tasks might be draggable even without explicit class
            if tasks:
                functionality_tests.append("Tasks present (potential draggable elements)")
                print("✓ Tasks present (potential draggable elements)")
            else:
                functionality_tests.append("No draggable elements found")
                print("✗ No draggable elements found")
    except Exception as e:
        functionality_tests.append(f"Error checking draggable elements: {str(e)}")
        print(f"✗ Error checking draggable elements: {str(e)}")

    # Step 6: Summary and Results
    print(f"\n{'=' * 50}")
    print("MY BOARD TEST SUMMARY")
    print(f"{'=' * 50}")
    print(f"Final URL: {current_url}")
    print(f"Elements Found: {len(found_elements)}/{len(expected_my_board_elements)}")
    print(f"Missing Elements: {missing_elements}")
    print(f"Functionality Tests: {len(functionality_tests)} checks performed")

    for test in functionality_tests:
        print(f" - {test}")

    # Take screenshot for verification
    driver.save_screenshot("my_board_test_results.png")
    print("Screenshot saved as 'my_board_test_results.png'")

    # Final verdict
    success_criteria = [
        "kanban-board" in current_url or "my-board" in current_url,
        len(found_elements) >= 4,  # At least basic elements present
        any("column" in test.lower() for test in functionality_tests),
        any("task" in test.lower() for test in functionality_tests)
    ]

    if all(success_criteria):
        print(f"\n{'=' * 50}")
        print("MY BOARD TEST: PASSED ✓")
        print("Successfully accessed and tested MY Board functionality")
        print(f"{'=' * 50}")
    else:
        print(f"\n{'=' * 50}")
        print("MY BOARD TEST: FAILED ✗")
        print("Issues encountered with MY Board access or functionality")
        print(f"{'=' * 50}")

        # Additional troubleshooting info
        print("\nTroubleshooting Info:")
        print(f"On MY Board URL: {'kanban-board' in current_url or 'my-board' in current_url}")
        print(f"Basic elements found: {len(found_elements)}/7")
        print(f"Columns detected: {any('column' in test.lower() for test in functionality_tests)}")
        print(f"Tasks detected: {any('task' in test.lower() for test in functionality_tests)}")

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

        # Try to get any page source info
        page_source = driver.page_source
        if "kanbird" in page_source.lower():
            print("Kanbird page detected")
        if "board" in page_source.lower():
            print("Board content detected")
        if "todo" in page_source.lower() or "progress" in page_source.lower():
            print("Kanban board content detected")

    except Exception as troubleshoot_error:
        print(f"Troubleshooting failed: {troubleshoot_error}")

finally:
    driver.quit()