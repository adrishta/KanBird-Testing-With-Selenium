# Kanbird New Todo Creation Testing
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


def generate_todo_title():
    """Generate unique todo title with timestamp"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return f"Test Todo {timestamp}"


try:
    print("Starting Kanbird New Todo Creation Testing...")

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

    # Step 3: Navigate to Todos Page
    print("\nStep 3: Navigating to Todos section...")

    # Try direct URL access
    print("Accessing Todos directly...")
    driver.get("https://app.kanbird.com/todos")
    print("Directly accessed Todos URL")

    # Wait for Todos to load
    print("\nWaiting for Todos to load...")
    time.sleep(8)

    # Step 4: Create New Todo
    print("\nStep 4: Creating New Todo...")

    # Generate unique todo data
    todo_title = generate_todo_title()
    print(f"Todo Title: {todo_title}")

    # Look for todo creation elements
    creation_tests = []

    # Method 1: Look for "Add Task" button
    print("\nMethod 1: Looking for 'Add Task' button...")
    add_task_buttons = driver.find_elements(By.XPATH,
                                            "//button[contains(text(), 'Add Task')] | " +
                                            "//button[contains(text(), 'New Task')] | " +
                                            "//button[contains(text(), 'Create Task')] | " +
                                            "//button[contains(text(), 'Add Todo')]")

    if add_task_buttons:
        for button in add_task_buttons:
            if button.is_displayed():
                print("Found Add Task button, clicking...")
                driver.execute_script("arguments[0].click();", button)
                creation_tests.append("✓ Add Task button clicked")
                time.sleep(3)
                break

    # Method 2: Look for quick input field
    print("\nMethod 2: Looking for quick input field...")
    quick_inputs = driver.find_elements(By.XPATH,
                                        "//input[@placeholder='Add a new task...'] | " +
                                        "//input[@placeholder='What needs to be done?'] | " +
                                        "//input[@placeholder='Add new todo...'] | " +
                                        "//input[contains(@placeholder, 'Add')] | " +
                                        "//input[contains(@placeholder, 'new')]")

    if quick_inputs:
        for input_field in quick_inputs:
            if input_field.is_displayed():
                print("Found quick input field, adding todo...")
                input_field.send_keys(todo_title)
                input_field.send_keys(Keys.ENTER)
                creation_tests.append("✓ Todo added via quick input")
                time.sleep(3)
                break

    # Method 3: Look for textarea or larger input
    print("\nMethod 3: Looking for larger input fields...")
    text_areas = driver.find_elements(By.XPATH,
                                      "//textarea | " +
                                      "//input[@type='text'] | " +
                                      "//div[contenteditable='true']")

    if text_areas:
        for field in text_areas:
            if field.is_displayed() and field.is_enabled():
                print("Found text input field, adding todo...")
                field.send_keys(todo_title)
                creation_tests.append("✓ Todo title entered in text field")

                # Look for save/submit button
                save_buttons = driver.find_elements(By.XPATH,
                                                    "//button[contains(text(), 'Save')] | " +
                                                    "//button[contains(text(), 'Add')] | " +
                                                    "//button[contains(text(), 'Create')] | " +
                                                    "//button[@type='submit']")

                if save_buttons:
                    for save_btn in save_buttons:
                        if save_btn.is_displayed():
                            driver.execute_script("arguments[0].click();", save_btn)
                            creation_tests.append("✓ Todo saved with save button")
                            break
                else:
                    # Try pressing Enter
                    field.send_keys(Keys.ENTER)
                    creation_tests.append("✓ Todo saved with Enter key")
                time.sleep(3)
                break

    # Method 4: Look for plus icon or create button
    print("\nMethod 4: Looking for plus icons...")
    plus_buttons = driver.find_elements(By.XPATH,
                                        "//button[contains(@class, 'plus')] | " +
                                        "//*[contains(text(), '+')] | " +
                                        "//button[contains(@class, 'add')] | " +
                                        "//div[contains(@class, 'create')]")

    if plus_buttons:
        for button in plus_buttons:
            if button.is_displayed():
                print("Found create button, clicking...")
                driver.execute_script("arguments[0].click();", button)
                creation_tests.append("✓ Create button clicked")
                time.sleep(3)

                # Now look for input in modal
                modal_inputs = driver.find_elements(By.XPATH,
                                                    "//input | //textarea | //div[contenteditable='true']")

                if modal_inputs:
                    for input_field in modal_inputs:
                        if input_field.is_displayed() and input_field.is_enabled():
                            input_field.send_keys(todo_title)
                            creation_tests.append("✓ Todo title entered in modal")

                            # Save the todo
                            modal_save_buttons = driver.find_elements(By.XPATH,
                                                                      "//button[contains(text(), 'Save')] | " +
                                                                      "//button[contains(text(), 'Add')] | " +
                                                                      "//button[contains(text(), 'Create')]")

                            if modal_save_buttons:
                                for save_btn in modal_save_buttons:
                                    if save_btn.is_displayed():
                                        driver.execute_script("arguments[0].click();", save_btn)
                                        creation_tests.append("✓ Todo saved from modal")
                                        break
                            break
                break

    # Step 5: Verify Todo Creation
    print("\nStep 5: Verifying Todo Creation...")

    verification_tests = []

    # Check if todo appears in the list
    try:
        # Wait a moment for the todo to appear
        time.sleep(5)

        # Look for the newly created todo in various ways
        todo_selectors = [
            f"//*[contains(text(), '{todo_title}')]",
            "//div[contains(@class, 'task')]",
            "//div[contains(@class, 'todo')]",
            "//li[contains(@class, 'task')]",
            "//li[contains(@class, 'todo')]"
        ]

        todo_found = False
        for selector in todo_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and todo_title in element.text:
                        verification_tests.append(f"✓ New todo '{todo_title}' found in list")
                        print(f"✓ New todo '{todo_title}' found in list")
                        todo_found = True
                        break
                if todo_found:
                    break
            except:
                continue

        if not todo_found:
            verification_tests.append(f"✗ New todo '{todo_title}' not found in list")
            print(f"✗ New todo '{todo_title}' not found in list")

    except Exception as e:
        verification_tests.append(f"✗ Error verifying todo: {str(e)}")
        print(f"✗ Error verifying todo: {str(e)}")

    # Check for success message
    try:
        success_messages = driver.find_elements(By.XPATH,
                                                "//*[contains(text(), 'success')] | " +
                                                "//*[contains(text(), 'created')] | " +
                                                "//*[contains(text(), 'added')] | " +
                                                "//*[contains(@class, 'success')]")

        if success_messages:
            verification_tests.append("✓ Success message displayed")
            print("✓ Success message displayed")
        else:
            verification_tests.append("✗ No success message detected")
            print("✗ No success message detected")
    except Exception as e:
        verification_tests.append(f"✗ Error checking success message: {str(e)}")
        print(f"✗ Error checking success message: {str(e)}")

    # Check current URL and page state
    current_url = driver.current_url
    if "todos" in current_url or "todo" in current_url:
        verification_tests.append("✓ Still on Todos page after creation")
        print("✓ Still on Todos page after creation")
    else:
        verification_tests.append(f"✗ Unexpected page: {current_url}")
        print(f"✗ Unexpected page: {current_url}")

    # Take screenshot
    driver.save_screenshot("todo_creation_results.png")
    print("Screenshot saved as 'todo_creation_results.png'")

    # Step 6: Summary and Results
    print(f"\n{'=' * 50}")
    print("TODO CREATION TEST SUMMARY")
    print(f"{'=' * 50}")
    print(f"Todo Title: {todo_title}")
    print(f"Creation Methods Attempted: {len(creation_tests)}")
    print(f"Verification Tests: {len(verification_tests)}")

    print("\nCreation Methods:")
    for test in creation_tests:
        print(f" - {test}")

    print("\nVerification Results:")
    for test in verification_tests:
        print(f" - {test}")

    # Final verdict
    creation_success = any("✓" in test for test in creation_tests)
    verification_success = any("✓" in test and "found" in test.lower() for test in verification_tests)

    if creation_success and verification_success:
        print(f"\n{'=' * 50}")
        print("TODO CREATION TEST: PASSED ✓")
        print("Successfully created new todo")
        print(f"{'=' * 50}")
    else:
        print(f"\n{'=' * 50}")
        print("TODO CREATION TEST: FAILED ✗")
        print("Issues encountered during todo creation")
        print(f"{'=' * 50}")

        # Debug information
        print("\nDebug Information:")
        print(f"Page Title: {driver.title}")
        print(f"Current URL: {current_url}")

        # Check page content
        page_source = driver.page_source.lower()
        if "todo" in page_source:
            print("✓ 'todo' text found in page")
        if "task" in page_source:
            print("✓ 'task' text found in page")
        if "add" in page_source:
            print("✓ 'add' text found in page")

    print("\nAutomation finished!")
    input("Press Enter to close browser...")

except Exception as e:
    print(f"Error during automation: {str(e)}")
    import traceback

    traceback.print_exc()

    # Take error screenshot
    try:
        driver.save_screenshot("todo_creation_error.png")
        print("Error screenshot saved as 'todo_creation_error.png'")
    except:
        pass

finally:
    driver.quit()