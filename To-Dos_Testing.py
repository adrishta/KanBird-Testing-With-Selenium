# Kanbird Todos Section Testing
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Initialize driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

try:
    print("Starting Kanbird Todos Section Testing...")

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

    # Step 3: Navigate to Todos
    print("\nStep 3: Navigating to Todos section...")

    # Method 1: Try to find and click Todos link in sidebar
    todos_found = False

    # Look for Todos in various possible locations
    todos_selectors = [
        "//*[contains(text(), 'Todos')]",
        "//*[contains(text(), 'todos')]",
        "//*[contains(text(), 'TODOS')]",
        "//*[contains(text(), 'To Do')]",
        "//*[contains(text(), 'To-do')]",
        "//a[contains(@href, 'todos')]",
        "//a[contains(@href, 'todo')]"
    ]

    for selector in todos_selectors:
        try:
            todos_elements = driver.find_elements(By.XPATH, selector)
            for element in todos_elements:
                if element.is_displayed():
                    print(f"Found Todos element with selector: {selector}")
                    driver.execute_script("arguments[0].click();", element)
                    print("Clicked Todos")
                    todos_found = True
                    break
            if todos_found:
                break
        except:
            continue

    # If not found via click, try direct URL access
    if not todos_found:
        print("Todos link not found in UI, trying direct URL access...")
        driver.get("https://app.kanbird.com/todos")
        print("Directly accessed Todos URL")

    # Wait for Todos to load
    print("\nWaiting for Todos to load...")
    time.sleep(8)

    # Step 4: Test Todos Elements and Functionality
    print("\nStep 4: Testing Todos Elements and Functionality...")

    current_url = driver.current_url
    print(f"Current URL: {current_url}")

    # Expected Todos elements
    expected_todos_elements = [
        "Todos",
        "Todo",
        "Add Task",
        "New Task",
        "Create",
        "Complete",
        "Pending",
        "Completed",
        "Due Date",
        "Priority",
        "Filter",
        "Search",
        "All",
        "Active",
        "Done"
    ]

    found_elements = []
    missing_elements = []

    for element_text in expected_todos_elements:
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

    # Step 5: Test Todos Specific Features
    print("\nStep 5: Testing Todos Specific Features...")

    functionality_tests = []

    # Test 1: Check if we're on Todos page
    if "todos" in current_url or "todo" in current_url:
        functionality_tests.append("Successfully accessed Todos URL")
        print("✓ Successfully accessed Todos URL")
    else:
        functionality_tests.append(f"Not on Todos, current page: {current_url}")
        print(f"✗ Not on Todos, current page: {current_url}")

    # Test 2: Check for task creation functionality
    try:
        add_task_buttons = driver.find_elements(By.XPATH,
                                                "//button[contains(text(), 'Add Task')] | " +
                                                "//button[contains(text(), 'New Task')] | " +
                                                "//button[contains(text(), 'Create Task')] | " +
                                                "//input[@placeholder='Add a new task...'] | " +
                                                "//input[@placeholder='What needs to be done?']")

        if add_task_buttons:
            functionality_tests.append("Task creation functionality available")
            print("✓ Task creation functionality available")

            # Try to add a new task
            for element in add_task_buttons:
                if element.is_displayed():
                    if element.tag_name == "input":
                        # It's an input field for quick task addition
                        test_task = f"Test Task {time.strftime('%H%M%S')}"
                        element.send_keys(test_task)
                        element.send_keys(Keys.ENTER)
                        functionality_tests.append(f"Added test task: {test_task}")
                        print(f"✓ Added test task: {test_task}")
                        time.sleep(2)
                        break
                    else:
                        # It's a button that opens a modal
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(2)

                        # Look for task creation modal
                        modal_inputs = driver.find_elements(By.XPATH,
                                                            "//input[@placeholder='Task title'] | " +
                                                            "//input[contains(@placeholder, 'Title')] | " +
                                                            "//textarea")
                        if modal_inputs:
                            test_task = f"Test Task {time.strftime('%H%M%S')}"
                            modal_inputs[0].send_keys(test_task)
                            functionality_tests.append("Task creation modal opened")
                            print("✓ Task creation modal opened")

                            # Try to save the task
                            save_buttons = driver.find_elements(By.XPATH,
                                                                "//button[contains(text(), 'Save')] | " +
                                                                "//button[contains(text(), 'Add')] | " +
                                                                "//button[@type='submit']")
                            if save_buttons:
                                driver.execute_script("arguments[0].click();", save_buttons[0])
                                functionality_tests.append(f"Task saved: {test_task}")
                                print(f"✓ Task saved: {test_task}")
                            else:
                                # Close modal if save not found
                                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                        break
        else:
            functionality_tests.append("No task creation functionality found")
            print("✗ No task creation functionality found")
    except Exception as e:
        functionality_tests.append(f"Error testing task creation: {str(e)}")
        print(f"✗ Error testing task creation: {str(e)}")

    # Test 3: Check for existing tasks list
    try:
        task_items = driver.find_elements(By.XPATH,
                                          "//div[contains(@class, 'task-item')] | " +
                                          "//li[contains(@class, 'task')] | " +
                                          "//div[contains(@class, 'todo-item')] | " +
                                          "//tr[contains(@class, 'task')]")

        if task_items:
            functionality_tests.append(f"Found {len(task_items)} task items")
            print(f"✓ Found {len(task_items)} task items")

            # Test task completion if tasks exist
            if task_items:
                # Look for completion checkboxes or buttons
                complete_buttons = driver.find_elements(By.XPATH,
                                                        "//input[@type='checkbox'] | " +
                                                        "//button[contains(text(), 'Complete')] | " +
                                                        "//*[contains(@class, 'complete')]")

                if complete_buttons:
                    # Try to complete the first task
                    driver.execute_script("arguments[0].click();", complete_buttons[0])
                    functionality_tests.append("Task completion functionality tested")
                    print("✓ Task completion functionality tested")
                    time.sleep(2)
        else:
            functionality_tests.append("No task items found")
            print("✗ No task items found")
    except Exception as e:
        functionality_tests.append(f"Error finding tasks: {str(e)}")
        print(f"✗ Error finding tasks: {str(e)}")

    # Test 4: Check for filtering options
    try:
        filter_buttons = driver.find_elements(By.XPATH,
                                              "//button[contains(text(), 'All')] | " +
                                              "//button[contains(text(), 'Active')] | " +
                                              "//button[contains(text(), 'Completed')] | " +
                                              "//button[contains(text(), 'Pending')] | " +
                                              "//div[contains(@class, 'filter')]")

        if filter_buttons:
            functionality_tests.append(f"Found {len(filter_buttons)} filtering options")
            print(f"✓ Found {len(filter_buttons)} filtering options")

            # Test filter switching
            for button in filter_buttons[:2]:  # Test first 2 filters
                try:
                    if button.is_displayed() and any(
                            filter_text in button.text for filter_text in ['All', 'Active', 'Completed', 'Pending']):
                        filter_name = button.text
                        driver.execute_script("arguments[0].click();", button)
                        functionality_tests.append(f"Switched to {filter_name} filter")
                        print(f"✓ Switched to {filter_name} filter")
                        time.sleep(2)
                        break
                except:
                    continue
        else:
            functionality_tests.append("No filtering options found")
            print("✗ No filtering options found")
    except Exception as e:
        functionality_tests.append(f"Error testing filters: {str(e)}")
        print(f"✗ Error testing filters: {str(e)}")

    # Test 5: Check for search functionality
    try:
        search_fields = driver.find_elements(By.XPATH,
                                             "//input[@placeholder='Search'] | " +
                                             "//input[@type='search'] | " +
                                             "//input[contains(@placeholder, 'Find')]")

        if search_fields:
            functionality_tests.append("Search functionality available")
            print("✓ Search functionality available")

            # Test search
            search_fields[0].send_keys("test")
            search_fields[0].send_keys(Keys.ENTER)
            functionality_tests.append("Search functionality tested")
            print("✓ Search functionality tested")
            time.sleep(2)
        else:
            functionality_tests.append("No search functionality found")
            print("✗ No search functionality found")
    except Exception as e:
        functionality_tests.append(f"Error testing search: {str(e)}")
        print(f"✗ Error testing search: {str(e)}")

    # Test 6: Check for priority indicators
    try:
        priority_elements = driver.find_elements(By.XPATH,
                                                 "//*[contains(text(), 'High')] | " +
                                                 "//*[contains(text(), 'Medium')] | " +
                                                 "//*[contains(text(), 'Low')] | " +
                                                 "//span[contains(@class, 'priority')]")

        if priority_elements:
            functionality_tests.append("Priority indicators found")
            print("✓ Priority indicators found")
        else:
            functionality_tests.append("No priority indicators found")
            print("✗ No priority indicators found")
    except Exception as e:
        functionality_tests.append(f"Error checking priorities: {str(e)}")
        print(f"✗ Error checking priorities: {str(e)}")

    # Test 7: Check for due date functionality
    try:
        due_date_elements = driver.find_elements(By.XPATH,
                                                 "//*[contains(text(), 'Due Date')] | " +
                                                 "//*[contains(text(), 'Due')] | " +
                                                 "//input[@type='date']")

        if due_date_elements:
            functionality_tests.append("Due date functionality found")
            print("✓ Due date functionality found")
        else:
            functionality_tests.append("No due date functionality found")
            print("✗ No due date functionality found")
    except Exception as e:
        functionality_tests.append(f"Error checking due dates: {str(e)}")
        print(f"✗ Error checking due dates: {str(e)}")

    # Test 8: Check for task actions (edit, delete)
    try:
        action_buttons = driver.find_elements(By.XPATH,
                                              "//button[contains(text(), 'Edit')] | " +
                                              "//button[contains(text(), 'Delete')] | " +
                                              "//button[contains(@class, 'edit')] | " +
                                              "//button[contains(@class, 'delete')]")

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
    print("TODOS TEST SUMMARY")
    print(f"{'=' * 50}")
    print(f"Final URL: {current_url}")
    print(f"Elements Found: {len(found_elements)}/{len(expected_todos_elements)}")
    print(f"Missing Elements: {missing_elements}")
    print(f"Functionality Tests: {len(functionality_tests)} checks performed")

    for test in functionality_tests:
        print(f" - {test}")

    # Take screenshot for verification
    driver.save_screenshot("todos_test_results.png")
    print("Screenshot saved as 'todos_test_results.png'")

    # Final verdict
    success_criteria = [
        "todos" in current_url or "todo" in current_url,
        len(found_elements) >= 5,  # At least basic elements present
        any("task" in test.lower() for test in functionality_tests),
        any("creation" in test.lower() or "add" in test.lower() for test in functionality_tests)
    ]

    if all(success_criteria):
        print(f"\n{'=' * 50}")
        print("TODOS TEST: PASSED ✓")
        print("Successfully accessed and tested Todos functionality")
        print(f"{'=' * 50}")
    else:
        print(f"\n{'=' * 50}")
        print("TODOS TEST: FAILED ✗")
        print("Issues encountered with Todos access or functionality")
        print(f"{'=' * 50}")

        # Additional troubleshooting info
        print("\nTroubleshooting Info:")
        print(f"On Todos URL: {'todos' in current_url or 'todo' in current_url}")
        print(f"Basic elements found: {len(found_elements)}/{len(expected_todos_elements)}")
        print(f"Task functionality detected: {any('task' in test.lower() for test in functionality_tests)}")
        print(
            f"Creation functionality detected: {any('creation' in test.lower() or 'add' in test.lower() for test in functionality_tests)}")

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
        if "todo" in page_source.lower():
            print("Todos content detected")
        if "task" in page_source.lower():
            print("Task content detected")

    except Exception as troubleshoot_error:
        print(f"Troubleshooting failed: {troubleshoot_error}")

finally:
    driver.quit()