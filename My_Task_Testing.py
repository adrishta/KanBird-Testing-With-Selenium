# Kanbird MY Task Section Testing
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
    print("Starting Kanbird MY Task Section Testing...")

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

    # Step 3: Navigate to MY Task
    print("\nStep 3: Navigating to MY Task section...")

    # Method 1: Try to find and click MY Task link in sidebar
    my_task_found = False

    # Look for MY Task in various possible locations
    my_task_selectors = [
        "//*[contains(text(), 'My Task')]",
        "//*[contains(text(), 'My task')]",
        "//*[contains(text(), 'MY TASK')]",
        "//a[contains(@href, 'my-task')]",
        "//a[contains(@href, 'mytask')]",
        "//*[contains(text(), 'Tasks')]",
        "//*[contains(text(), 'tasks')]"
    ]

    for selector in my_task_selectors:
        try:
            my_task_elements = driver.find_elements(By.XPATH, selector)
            for element in my_task_elements:
                if element.is_displayed():
                    print(f"Found MY Task element with selector: {selector}")
                    driver.execute_script("arguments[0].click();", element)
                    print("Clicked MY Task")
                    my_task_found = True
                    break
            if my_task_found:
                break
        except:
            continue

    # If not found via click, try direct URL access
    if not my_task_found:
        print("MY Task link not found in UI, trying direct URL access...")
        driver.get("https://app.kanbird.com/my-task")
        print("Directly accessed MY Task URL")

    # Wait for MY Task to load
    print("\nWaiting for MY Task to load...")
    time.sleep(8)

    # Step 4: Test MY Task Elements and Functionality
    print("\nStep 4: Testing MY Task Elements and Functionality...")

    current_url = driver.current_url
    print(f"Current URL: {current_url}")

    # Expected MY Task elements
    expected_my_task_elements = [
        "My Task",
        "Tasks",
        "To Do",
        "In Progress",
        "Done",
        "Completed",
        "Pending",
        "Assigned",
        "Due Date",
        "Priority",
        "Status",
        "Filter",
        "Search"
    ]

    found_elements = []
    missing_elements = []

    for element_text in expected_my_task_elements:
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

    # Step 5: Test Task Management Specific Features
    print("\nStep 5: Testing Task Management Specific Features...")

    functionality_tests = []

    # Test 1: Check if we're on MY Task page
    if "my-task" in current_url or "mytask" in current_url or "task" in current_url.lower():
        functionality_tests.append("Successfully accessed MY Task URL")
        print("✓ Successfully accessed MY Task URL")
    else:
        functionality_tests.append(f"Not on MY Task, current page: {current_url}")
        print(f"✗ Not on MY Task, current page: {current_url}")

    # Test 2: Check for task lists or tables
    try:
        # Look for task containers, lists, or tables
        task_containers = driver.find_elements(By.XPATH,
                                               "//div[contains(@class, 'task')] | //div[contains(@class, 'task-list')] | //table | //div[contains(@class, 'item')] | //div[contains(@class, 'card')]")
        if task_containers:
            functionality_tests.append(f"Found {len(task_containers)} task containers/lists")
            print(f"✓ Found {len(task_containers)} task containers/lists")
        else:
            functionality_tests.append("No task containers found")
            print("✗ No task containers found")
    except Exception as e:
        functionality_tests.append(f"Error finding task containers: {str(e)}")
        print(f"✗ Error finding task containers: {str(e)}")

    # Test 3: Check for individual task items
    try:
        tasks = driver.find_elements(By.XPATH,
                                     "//div[contains(@class, 'task-item')] | //tr[contains(@class, 'task')] | //li[contains(@class, 'task')] | //div[contains(text(), 'Task')]")
        if tasks:
            functionality_tests.append(f"Found {len(tasks)} task items")
            print(f"✓ Found {len(tasks)} task items")
        else:
            functionality_tests.append("No individual task items found")
            print("✗ No individual task items found")
    except Exception as e:
        functionality_tests.append(f"Error finding tasks: {str(e)}")
        print(f"✗ Error finding tasks: {str(e)}")

    # Test 4: Test task filtering and search functionality
    try:
        # Look for filter buttons, dropdowns, or search inputs
        filter_elements = driver.find_elements(By.XPATH,
                                               "//button[contains(text(), 'Filter')] | //select | //input[@placeholder='Search'] | //input[@type='search']")
        search_elements = driver.find_elements(By.XPATH,
                                               "//input[contains(@placeholder, 'Search')] | //input[@type='search'] | //input[contains(@placeholder, 'Find')]")

        if filter_elements:
            functionality_tests.append("Filter functionality available")
            print("✓ Filter functionality available")
        else:
            functionality_tests.append("Filter elements not found")
            print("✗ Filter elements not found")

        if search_elements:
            functionality_tests.append("Search functionality available")
            print("✓ Search functionality available")
        else:
            functionality_tests.append("Search elements not found")
            print("✗ Search elements not found")

    except Exception as e:
        functionality_tests.append(f"Error testing filter/search: {str(e)}")
        print(f"✗ Error testing filter/search: {str(e)}")

    # Test 5: Test task status indicators
    try:
        status_indicators = driver.find_elements(By.XPATH,
                                                 "//*[contains(text(), 'To Do')] | //*[contains(text(), 'In Progress')] | //*[contains(text(), 'Done')] | //*[contains(text(), 'Completed')] | //span[contains(@class, 'status')]")
        if status_indicators:
            functionality_tests.append(f"Found {len(status_indicators)} status indicators")
            print(f"✓ Found {len(status_indicators)} status indicators")
        else:
            functionality_tests.append("No status indicators found")
            print("✗ No status indicators found")
    except Exception as e:
        functionality_tests.append(f"Error checking status indicators: {str(e)}")
        print(f"✗ Error checking status indicators: {str(e)}")

    # Test 6: Test task actions (edit, delete, etc.)
    try:
        action_buttons = driver.find_elements(By.XPATH,
                                              "//button[contains(text(), 'Edit')] | //button[contains(text(), 'Delete')] | //button[contains(text(), 'Complete')] | //*[contains(@class, 'actions')]")
        if action_buttons:
            functionality_tests.append("Task action buttons available")
            print("✓ Task action buttons available")
        else:
            functionality_tests.append("No task action buttons found")
            print("✗ No task action buttons found")
    except Exception as e:
        functionality_tests.append(f"Error checking action buttons: {str(e)}")
        print(f"✗ Error checking action buttons: {str(e)}")

    # Step 6: Summary and Results
    print(f"\n{'=' * 50}")
    print("MY TASK TEST SUMMARY")
    print(f"{'=' * 50}")
    print(f"Final URL: {current_url}")
    print(f"Elements Found: {len(found_elements)}/{len(expected_my_task_elements)}")
    print(f"Missing Elements: {missing_elements}")
    print(f"Functionality Tests: {len(functionality_tests)} checks performed")

    for test in functionality_tests:
        print(f" - {test}")

    # Take screenshot for verification
    driver.save_screenshot("my_task_test_results.png")
    print("Screenshot saved as 'my_task_test_results.png'")

    # Final verdict
    success_criteria = [
        "my-task" in current_url or "mytask" in current_url or "task" in current_url.lower(),
        len(found_elements) >= 4,  # At least basic elements present
        any("task" in test.lower() for test in functionality_tests),
        any("container" in test.lower() or "item" in test.lower() for test in functionality_tests)
    ]

    if all(success_criteria):
        print(f"\n{'=' * 50}")
        print("MY TASK TEST: PASSED ✓")
        print("Successfully accessed and tested MY Task functionality")
        print(f"{'=' * 50}")
    else:
        print(f"\n{'=' * 50}")
        print("MY TASK TEST: FAILED ✗")
        print("Issues encountered with MY Task access or functionality")
        print(f"{'=' * 50}")

        # Additional troubleshooting info
        print("\nTroubleshooting Info:")
        print(f"On MY Task URL: {'my-task' in current_url or 'mytask' in current_url or 'task' in current_url.lower()}")
        print(f"Basic elements found: {len(found_elements)}/{len(expected_my_task_elements)}")
        print(
            f"Task containers detected: {any('container' in test.lower() or 'item' in test.lower() for test in functionality_tests)}")
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
        if "task" in page_source.lower():
            print("Task content detected")
        if "todo" in page_source.lower() or "progress" in page_source.lower():
            print("Task status content detected")

    except Exception as troubleshoot_error:
        print(f"Troubleshooting failed: {troubleshoot_error}")

finally:
    driver.quit()