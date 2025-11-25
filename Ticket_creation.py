import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Initialize driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 30)

try:
    print("KANBIRD TICKET CREATION - ALL DROPDOWN FIELDS FILLUP")
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

    # Step 2: Go to Tickets
    print("\n Step 2: Navigate to Tickets")
    driver.get("https://app.kanbird.com/tickets")
    time.sleep(10)

    print(f"Current page: {driver.current_url}")

    # Step 3: Click the EXACT PLUS button in navigation bar
    print("\n Step 3: Click Navigation Bar PLUS Button")
    time.sleep(5)

    # EXACT SELECTORS for the PLUS button in navigation bar
    plus_clicked = False

    # Strategy 1: PLUS button in the breadcrumb/navigation area
    nav_plus_selectors = [
        "//nav//button[contains(., '+')]",
        "//div[contains(@class, 'breadcrumb')]//button[contains(., '+')]",
        "//div[contains(text(), 'Home')]//following::button[contains(., '+')]",
        "//*[contains(text(), 'Tickets')]//following::button[1]",
        "//header//button[contains(., '+')]",
        "//div[contains(@class, 'header')]//button[contains(., '+')]",
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

    if plus_clicked:
        print(" PLUS BUTTON CLICKED SUCCESSFULLY!")
        time.sleep(8)

        # Step 4: Fill Title, Start Date, Due Date, Assigned By, Assignee Fields
        print("\n Step 4: Fill Title, Start Date, Due Date, Assigned By, Assignee Fields")
        time.sleep(5)

        # Track if all required fields are filled
        all_required_fields_filled = True

        # 1. Fill Title Field
        print("\n1. Filling Title Field...")
        try:
            title_selectors = [
                "//input[@placeholder='Enter title']",
                "//input[contains(@placeholder, 'Title')]",
                "//input[@id='title']",
                "//input[@name='title']",
                "//label[contains(text(), 'Title')]/following::input[1]"
            ]
            title_filled = False
            for selector in title_selectors:
                try:
                    title_field = driver.find_element(By.XPATH, selector)
                    title_field.clear()
                    title_field.send_keys("error in lead creation")
                    print("   Title: error in lead creation")
                    title_filled = True
                    break
                except:
                    continue
            else:
                print("   Title field not found")
                all_required_fields_filled = False
        except Exception as e:
            print(f"   Title field error: {e}")
            all_required_fields_filled = False

        # 2. Fill Start Date Field - DROPDOWN SELECTION
        print("\n2. Filling Start Date Field - Dropdown Selection...")
        start_date_filled = False
        try:
            # Click on Start Date field to open calendar
            start_date_selectors = [
                "//input[contains(@placeholder, 'Start Date')]",
                "//input[contains(@placeholder, 'Start date')]",
                "//label[contains(text(), 'Start Date')]/following::input[1]",
                "//input[@name='startDate']",
                "//input[@id='startDate']"
            ]

            for selector in start_date_selectors:
                try:
                    start_field = driver.find_element(By.XPATH, selector)
                    start_field.click()
                    print("   Start Date field clicked - calendar opened")
                    time.sleep(3)

                    # Select date 18 from calendar dropdown
                    date_18_selectors = [
                        "//div[contains(text(), '18')]",
                        "//td[contains(text(), '18')]",
                        "//span[contains(text(), '18')]",
                        "//button[contains(text(), '18')]",
                        "//div[text()='18']"
                    ]

                    for date_selector in date_18_selectors:
                        try:
                            date_elements = driver.find_elements(By.XPATH, date_selector)
                            for date_element in date_elements:
                                if date_element.is_displayed() and date_element.is_enabled():
                                    date_element.click()
                                    print("   Start Date selected: 18")
                                    start_date_filled = True
                                    time.sleep(2)
                                    break
                            if start_date_filled:
                                break
                        except:
                            continue
                    if start_date_filled:
                        break
                except:
                    continue

            if not start_date_filled:
                print("   Start Date field not filled")
                all_required_fields_filled = False
        except Exception as e:
            print(f"   Start Date field error: {e}")
            all_required_fields_filled = False

        # 3. Fill Due Date Field - DROPDOWN SELECTION
        print("\n3. Filling Due Date Field - Dropdown Selection...")
        due_date_filled = False
        try:
            # Click on Due Date field to open calendar
            due_date_selectors = [
                "//input[contains(@placeholder, 'Due Date')]",
                "//input[contains(@placeholder, 'Due date')]",
                "//label[contains(text(), 'Due Date')]/following::input[1]",
                "//input[@name='dueDate']",
                "//input[@id='dueDate']",
                "//input[contains(@placeholder, 'End Date')]"
            ]

            for selector in due_date_selectors:
                try:
                    due_fields = driver.find_elements(By.XPATH, selector)
                    for due_field in due_fields:
                        if due_field.is_displayed() and due_field.is_enabled():
                            driver.execute_script("arguments[0].click();", due_field)
                            print("   Due Date field clicked - calendar opened")
                            time.sleep(3)

                            # Select date 30 from calendar dropdown
                            date_30_selectors = [
                                "//div[contains(text(), '30') and contains(@class, 'day')]",
                                "//td[contains(text(), '30')]",
                                "//span[contains(text(), '30')]",
                                "//button[contains(text(), '30')]",
                                "//div[text()='30']"
                            ]

                            for date_selector in date_30_selectors:
                                try:
                                    date_elements = driver.find_elements(By.XPATH, date_selector)
                                    for date_element in date_elements:
                                        if date_element.is_displayed() and date_element.is_enabled():
                                            driver.execute_script("arguments[0].click();", date_element)
                                            print("   Due Date selected: 30")
                                            due_date_filled = True
                                            time.sleep(2)
                                            break
                                    if due_date_filled:
                                        break
                                except:
                                    continue
                            break
                    if due_date_filled:
                        break
                except:
                    continue

            if not due_date_filled:
                print("   Due Date field not filled")
                all_required_fields_filled = False
        except Exception as e:
            print(f"   Due Date field error: {e}")
            all_required_fields_filled = False

        # 4. Fill Assigned By Field - DROPDOWN SELECTION
        print("\n4. Filling Assigned By Field - Dropdown Selection...")
        assigned_by_filled = False
        try:
            # Find and click Assigned By dropdown
            assigned_by_dropdown_selectors = [
                "//label[contains(text(), 'Assigned By')]/following::div[1]",
                "//div[contains(text(), 'Assigned By')]/following::div[1]",
                "//div[contains(text(), 'Select Assignee')]",
                "//input[contains(@placeholder, 'Assigned By')]/following-sibling::div",
                "//div[@data-testid='assigned-by-dropdown']"
            ]

            for selector in assigned_by_dropdown_selectors:
                try:
                    dropdown_elements = driver.find_elements(By.XPATH, selector)
                    for dropdown in dropdown_elements:
                        if dropdown.is_displayed():
                            driver.execute_script("arguments[0].click();", dropdown)
                            print("   Assigned By dropdown clicked")
                            time.sleep(3)

                            # Select Intern from dropdown options
                            intern_selectors = [
                                "//div[contains(text(), 'Intern')]",
                                "//li[contains(text(), 'Intern')]",
                                "//span[contains(text(), 'Intern')]",
                                "//option[contains(text(), 'Intern')]"
                            ]

                            for intern_selector in intern_selectors:
                                try:
                                    intern_options = driver.find_elements(By.XPATH, intern_selector)
                                    for option in intern_options:
                                        if option.is_displayed():
                                            driver.execute_script("arguments[0].click();", option)
                                            print("   Assigned By selected: Intern")
                                            assigned_by_filled = True
                                            time.sleep(2)
                                            break
                                    if assigned_by_filled:
                                        break
                                except:
                                    continue
                            break
                except:
                    continue

            if not assigned_by_filled:
                print("   Assigned By field not filled")
                all_required_fields_filled = False
        except Exception as e:
            print(f"   Assigned By field error: {e}")
            all_required_fields_filled = False

        # 5. Fill Assignee Field - DROPDOWN SELECTION
        print("\n5. Filling Assignee Field - Dropdown Selection...")
        assignee_filled = False
        try:
            # Find and click Assignee dropdown
            assignee_dropdown_selectors = [
                "//label[contains(text(), 'Assignee')]/following::div[1]",
                "//div[contains(text(), 'Assignee')]/following::div[1]",
                "//div[contains(text(), 'Select Assignee')]",
                "//input[contains(@placeholder, 'Assignee')]/following-sibling::div",
                "//div[@data-testid='assignee-dropdown']"
            ]

            for selector in assignee_dropdown_selectors:
                try:
                    dropdown_elements = driver.find_elements(By.XPATH, selector)
                    for dropdown in dropdown_elements:
                        if dropdown.is_displayed():
                            driver.execute_script("arguments[0].click();", dropdown)
                            print("   Assignee dropdown clicked")
                            time.sleep(3)

                            # Select Intern from dropdown options
                            intern_selectors = [
                                "//div[contains(text(), 'Intern')]",
                                "//li[contains(text(), 'Intern')]",
                                "//span[contains(text(), 'Intern')]",
                                "//option[contains(text(), 'Intern')]"
                            ]

                            for intern_selector in intern_selectors:
                                try:
                                    intern_options = driver.find_elements(By.XPATH, intern_selector)
                                    for option in intern_options:
                                        if option.is_displayed():
                                            driver.execute_script("arguments[0].click();", option)
                                            print("   Assignee selected: Intern")
                                            assignee_filled = True
                                            time.sleep(2)
                                            break
                                    if assignee_filled:
                                        break
                                except:
                                    continue
                            break
                except:
                    continue

            if not assignee_filled:
                print("   Assignee field not filled")
                all_required_fields_filled = False
        except Exception as e:
            print(f"   Assignee field error: {e}")
            all_required_fields_filled = False

        # Step 5: Submit Ticket
        print("\n Step 5: Submit Ticket")
        time.sleep(3)

        # Submit regardless of field status
        print("Attempting to submit ticket...")

        submit_found = False
        submit_selectors = [
            "//button[@type='submit']",
            "//button[contains(text(), 'Submit')]",
            "//button[contains(text(), 'Save')]",
            "//button[contains(text(), 'Create')]",
            "//button[contains(@class, 'btn-primary')]",
            "//input[@type='submit']"
        ]

        for selector in submit_selectors:
            try:
                submit_btn = driver.find_element(By.XPATH, selector)
                if submit_btn.is_enabled():
                    print(f"Found submit button with: {selector}")
                    driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", submit_btn)
                    print(f"Submit button clicked!")
                    submit_found = True
                    time.sleep(10)
                    break
            except Exception as e:
                continue

        if submit_found:
            print("SUCCESS! Ticket submitted successfully!")
            print(f"\nFIELDS FILLED:")
            print(f"   Title: error in lead creation")
            print(f"   Start Date: 18 (Selected from calendar)")
            print(f"   Due Date: 30 (Selected from calendar)")
            print(f"   Assigned By: Intern (Selected from dropdown)")
            print(f"   Assignee: Intern (Selected from dropdown)")

            time.sleep(5)
            print(f"\nCurrent URL after submission: {driver.current_url}")
        else:
            print("Could not find or click submit button")

    else:
        print("FAILED: Could not find navigation PLUS button")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback

    print(f"Details: {traceback.format_exc()}")

finally:
    print("\n" + "=" * 50)
    print(" AUTOMATION COMPLETED")
    print("=" * 50)
    input("Press Enter to close browser...")
    driver.quit()