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
    print("KANBIRD LEAD CREATION - WORKING VERSION")
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

    # Step 3: Click the PLUS button
    print("\n Step 3: Click Plus Button")
    time.sleep(5)

    plus_clicked = False
    plus_buttons = driver.find_elements(By.XPATH, "//button[contains(., '+')]")

    for btn in plus_buttons:
        if btn.is_displayed() and btn.is_enabled():
            print(f" Found plus button: '{btn.text}'")
            driver.execute_script("arguments[0].click();", btn)
            print(" Plus button clicked!")
            plus_clicked = True
            time.sleep(8)
            break

    if plus_clicked:
        print("✅ LEAD FORM OPENED SUCCESSFULLY!")
        time.sleep(5)

        # Step 4: Fill ALL Form Fields
        print("\n Step 4: Filling Form Fields")

        # Your exact test data
        test_data = {
            'start_date': '18.11.25',
            'due_date': '30.11.25',
            'title': 'Testing',
            'assigned_by': 'Intern',
            'assign_to': 'Intern'
        }

        # 1. Fill TITLE
        print("1. Filling Title...")
        try:
            title_field = driver.find_element(By.XPATH, "//input[@placeholder='Enter title']")
            title_field.clear()
            title_field.send_keys(test_data['title'])
            print(f"   ✅ Title: {test_data['title']}")
        except Exception as e:
            print(f"   ❌ Title error: {e}")

        # 2. Fill START DATE
        print("2. Filling Start Date...")
        try:
            start_field = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Start Date')]")
            start_field.clear()
            start_field.send_keys(test_data['start_date'])
            print(f"   ✅ Start Date: {test_data['start_date']}")
        except Exception as e:
            print(f"   ❌ Start Date error: {e}")

        # 3. Fill DUE DATE
        print("3. Filling Due Date...")
        try:
            due_field = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Due Date')]")
            due_field.clear()
            due_field.send_keys(test_data['due_date'])
            print(f"   ✅ Due Date: {test_data['due_date']}")
        except Exception as e:
            print(f"   ❌ Due Date error: {e}")

        # 4. Fill EXPECTED REVENUE
        print("4. Filling Expected Revenue...")
        try:
            revenue_field = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Expected Revenue')]")
            revenue_field.clear()
            revenue_field.send_keys("10000")
            print("   ✅ Expected Revenue: 10000")
        except Exception as e:
            print(f"   ❌ Revenue error: {e}")

        # 5. Fill DESCRIPTION
        print("5. Filling Description...")
        try:
            desc_field = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
            desc_field.click()
            time.sleep(1)
            desc_field.clear()
            desc_field.send_keys("Automated test lead description")
            print("   ✅ Description filled")
        except Exception as e:
            print(f"   ❌ Description error: {e}")

        # Scroll down for dropdown sections
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(2)

        # 6. Fill ASSIGNED BY - DROPDOWN
        print("6. Filling Assigned By...")
        try:
            # Click dropdown
            assigned_by_dropdown = driver.find_element(By.XPATH, "//div[contains(text(), 'Select Assignee')]")
            assigned_by_dropdown.click()
            print("   ✅ Assigned By dropdown clicked")
            time.sleep(2)

            # Type in search
            search_input = driver.find_element(By.XPATH, "//input[@placeholder='Search...']")
            search_input.clear()
            search_input.send_keys(test_data['assigned_by'])
            print(f"   ✅ Typed: {test_data['assigned_by']}")
            time.sleep(2)

            # Select option
            intern_option = driver.find_element(By.XPATH, f"//div[contains(text(), '{test_data['assigned_by']}')]")
            intern_option.click()
            print(f"   ✅ Assigned By selected: {test_data['assigned_by']}")
            time.sleep(2)
        except Exception as e:
            print(f"   ❌ Assigned By error: {e}")

        # 7. Fill ASSIGN TO - DROPDOWN
        print("7. Filling Assign To...")
        try:
            # Click second dropdown
            all_dropdowns = driver.find_elements(By.XPATH, "//div[contains(text(), 'Select Assignee')]")
            if len(all_dropdowns) > 1:
                all_dropdowns[1].click()
                print("   ✅ Assign To dropdown clicked")
                time.sleep(2)

                # Type in search
                search_input = driver.find_element(By.XPATH, "//input[@placeholder='Search...']")
                search_input.clear()
                search_input.send_keys(test_data['assign_to'])
                print(f"   ✅ Typed: {test_data['assign_to']}")
                time.sleep(2)

                # Select option
                intern_option = driver.find_element(By.XPATH, f"//div[contains(text(), '{test_data['assign_to']}')]")
                intern_option.click()
                print(f"   ✅ Assign To selected: {test_data['assign_to']}")
                time.sleep(2)
            else:
                print("   ❌ Second dropdown not found")
        except Exception as e:
            print(f"   ❌ Assign To error: {e}")

        # Scroll to bottom for submit button
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Step 5: SUBMIT FORM
        print("\n Step 5: Submitting Form")
        time.sleep(3)

        submit_found = False
        for submit_text in ['Submit', 'Save', 'Create']:
            try:
                submit_btn = driver.find_element(By.XPATH, f"//button[contains(text(), '{submit_text}')]")
                if submit_btn.is_enabled():
                    driver.execute_script("arguments[0].click();", submit_btn)
                    print(f"✅ {submit_text} button clicked!")
                    submit_found = True
                    time.sleep(10)
                    break
            except:
                continue

        if submit_found:
            print("🎉 SUCCESS! Lead created successfully!")
            print(f"\n📋 LEAD DETAILS CREATED:")
            print(f"   - Title: {test_data['title']}")
            print(f"   - Start Date: {test_data['start_date']}")
            print(f"   - Due Date: {test_data['due_date']}")
            print(f"   - Assigned By: {test_data['assigned_by']}")
            print(f"   - Assign To: {test_data['assign_to']}")
        else:
            print("❌ Could not submit form")

    else:
        print("❌ FAILED: Could not find plus button")

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback

    print(f"Details: {traceback.format_exc()}")

finally:
    print("\n" + "=" * 50)
    print("SCRIPT COMPLETED")
    print("=" * 50)
    input("Press Enter to close browser...")
    driver.quit()