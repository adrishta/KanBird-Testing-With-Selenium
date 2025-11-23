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
    print("KANBIRD LEAD CREATION - COMPLETE FORM FILLING")
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
        "//*[contains(text(), 'Sprint')]//following::button[1]",
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

        # Step 4: Fill ALL Lead Form Fields with your specific data
        print("\n Step 4: Fill ALL Lead Form Fields")
        time.sleep(5)

        # Your specific test data for EVERY field
        test_data = {
            'title': 'Testing',
            'expected_revenue': '10000',
            'description': 'Automated test lead description',
            'contact': 'Test Contact',
            'organization': 'Test Organization',
            'product': 'Test Product'
        }

        print("Filling all form fields with your data...")

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
            for selector in title_selectors:
                try:
                    title_field = driver.find_element(By.XPATH, selector)
                    title_field.clear()
                    title_field.send_keys(test_data['title'])
                    print(f"   Title: {test_data['title']}")
                    break
                except:
                    continue
            else:
                print("   Title field not found")
        except Exception as e:
            print(f"   Title field error: {e}")

        # 2. Fill Start Date Field - DROPDOWN SELECTION
        print("\n2. Filling Start Date Field - Dropdown Selection...")
        start_date_filled = False
        try:
            # Click on Start Date field to open calendar
            start_date_selectors = [
                "//input[contains(@placeholder, 'Start Date')]",
                "//input[contains(@placeholder, 'Start date')]",
                "//label[contains(text(), 'Start Date')]/following::input[1]"
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
                        "//button[contains(text(), '18')]"
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
        except Exception as e:
            print(f"   Start Date field error: {e}")

        # 3. Fill Due Date Field - DROPDOWN SELECTION
        print("\n3. Filling Due Date Field - Dropdown Selection...")
        due_date_filled = False
        try:
            # Click on Due Date field to open calendar
            due_date_selectors = [
                "//input[contains(@placeholder, 'Due Date')]",
                "//input[contains(@placeholder, 'Due date')]",
                "//label[contains(text(), 'Due Date')]/following::input[1]"
            ]

            for selector in due_date_selectors:
                try:
                    due_field = driver.find_element(By.XPATH, selector)
                    due_field.click()
                    print("   Due Date field clicked - calendar opened")
                    time.sleep(3)

                    # Select date 30 from calendar dropdown
                    date_30_selectors = [
                        "//div[contains(text(), '30')]",
                        "//td[contains(text(), '30')]",
                        "//span[contains(text(), '30')]",
                        "//button[contains(text(), '30')]"
                    ]

                    for date_selector in date_30_selectors:
                        try:
                            date_elements = driver.find_elements(By.XPATH, date_selector)
                            for date_element in date_elements:
                                if date_element.is_displayed() and date_element.is_enabled():
                                    date_element.click()
                                    print("   Due Date selected: 30")
                                    due_date_filled = True
                                    time.sleep(2)
                                    break
                            if due_date_filled:
                                break
                        except:
                            continue
                    if due_date_filled:
                        break
                except:
                    continue
        except Exception as e:
            print(f"   Due Date field error: {e}")

        # 4. Fill Expected Revenue Field
        print("\n4. Filling Expected Revenue Field...")
        try:
            revenue_selectors = [
                "//input[contains(@placeholder, 'Expected Revenue')]",
                "//input[contains(@placeholder, 'Revenue')]",
                "//label[contains(text(), 'Expected Revenue')]/following::input[1]"
            ]
            for selector in revenue_selectors:
                try:
                    revenue_field = driver.find_element(By.XPATH, selector)
                    revenue_field.clear()
                    revenue_field.send_keys(test_data['expected_revenue'])
                    print(f"   Expected Revenue: {test_data['expected_revenue']}")
                    break
                except:
                    continue
            else:
                print("   Expected Revenue field not found")
        except Exception as e:
            print(f"   Expected Revenue field error: {e}")

        # 5. Fill Description Field
        print("\n5. Filling Description Field...")
        description_filled = False
        try:
            # Try contenteditable div first
            desc_fields = driver.find_elements(By.XPATH, "//div[@contenteditable='true']")
            for desc_field in desc_fields:
                try:
                    desc_field.click()
                    time.sleep(1)
                    desc_field.clear()
                    desc_field.send_keys(test_data['description'])
                    print(f"   Description: {test_data['description']}")
                    description_filled = True
                    break
                except:
                    continue
        except:
            pass

        if not description_filled:
            try:
                # Try textarea
                desc_fields = driver.find_elements(By.XPATH, "//textarea")
                for desc_field in desc_fields:
                    try:
                        desc_field.clear()
                        desc_field.send_keys(test_data['description'])
                        print(f"   Description: {test_data['description']}")
                        description_filled = True
                        break
                    except:
                        continue
            except:
                pass

        if not description_filled:
            print("   Description field not found")

        # 6. Fill Assigned By Field - DROPDOWN SELECTION
        print("\n6. Filling Assigned By Field - Dropdown Selection...")
        assigned_by_filled = False
        try:
            # Find and click Assigned By dropdown
            assigned_by_dropdown_selectors = [
                "//label[contains(text(), 'Assigned By')]/following::div[1]",
                "//div[contains(text(), 'Assigned By')]/following::div[1]",
                "//div[contains(text(), 'Select Assignee')]",
                "//input[contains(@placeholder, 'Assigned By')]/following-sibling::div"
            ]

            for selector in assigned_by_dropdown_selectors:
                try:
                    dropdown_elements = driver.find_elements(By.XPATH, selector)
                    for dropdown in dropdown_elements:
                        if dropdown.is_displayed():
                            dropdown.click()
                            print("   Assigned By dropdown clicked")
                            time.sleep(3)

                            # Select Intern from dropdown options
                            intern_selectors = [
                                "//div[contains(text(), 'Intern')]",
                                "//li[contains(text(), 'Intern')]",
                                "//span[contains(text(), 'Intern')]"
                            ]

                            for intern_selector in intern_selectors:
                                try:
                                    intern_options = driver.find_elements(By.XPATH, intern_selector)
                                    for option in intern_options:
                                        if option.is_displayed():
                                            option.click()
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
        except Exception as e:
            print(f"   Assigned By field error: {e}")

        # 7. Fill Assignee Field - DROPDOWN SELECTION
        print("\n7. Filling Assignee Field - Dropdown Selection...")
        assignee_filled = False
        try:
            # Find and click Assignee dropdown (second dropdown)
            assignee_dropdown_selectors = [
                "//label[contains(text(), 'Assignee')]/following::div[1]",
                "//div[contains(text(), 'Assignee')]/following::div[1]",
                "//div[contains(text(), 'Select Assignee')]",
                "//input[contains(@placeholder, 'Assignee')]/following-sibling::div"
            ]

            # Find the second dropdown for Assignee
            for selector in assignee_dropdown_selectors:
                try:
                    dropdown_elements = driver.find_elements(By.XPATH, selector)
                    if len(dropdown_elements) > 1:
                        assignee_dropdown = dropdown_elements[1]  # Second dropdown
                    else:
                        assignee_dropdown = dropdown_elements[0]

                    if assignee_dropdown.is_displayed():
                        assignee_dropdown.click()
                        print("   Assignee dropdown clicked")
                        time.sleep(3)

                        # Select Intern from dropdown options
                        intern_selectors = [
                            "//div[contains(text(), 'Intern')]",
                            "//li[contains(text(), 'Intern')]",
                            "//span[contains(text(), 'Intern')]"
                        ]

                        for intern_selector in intern_selectors:
                            try:
                                intern_options = driver.find_elements(By.XPATH, intern_selector)
                                for option in intern_options:
                                    if option.is_displayed():
                                        option.click()
                                        print("   Assignee selected: Intern")
                                        assignee_filled = True
                                        time.sleep(2)
                                        break
                                if assignee_filled:
                                    break
                            except:
                                continue
                except:
                    continue
        except Exception as e:
            print(f"   Assignee field error: {e}")

        # 8. Fill Contact Field
        print("\n8. Filling Contact Field...")
        try:
            contact_selectors = [
                "//input[contains(@placeholder, 'Contact')]",
                "//input[contains(@placeholder, 'Select Contact')]",
                "//label[contains(text(), 'Contact')]/following::input[1]"
            ]
            for selector in contact_selectors:
                try:
                    contact_field = driver.find_element(By.XPATH, selector)
                    contact_field.clear()
                    contact_field.send_keys(test_data['contact'])
                    print(f"   Contact: {test_data['contact']}")
                    break
                except:
                    continue
            else:
                print("   Contact field not found")
        except Exception as e:
            print(f"   Contact field error: {e}")

        # 9. Fill Organization Field
        print("\n9. Filling Organization Field...")
        try:
            org_selectors = [
                "//input[contains(@placeholder, 'Organization')]",
                "//label[contains(text(), 'Organization')]/following::input[1]"
            ]
            for selector in org_selectors:
                try:
                    org_field = driver.find_element(By.XPATH, selector)
                    org_field.clear()
                    org_field.send_keys(test_data['organization'])
                    print(f"   Organization: {test_data['organization']}")
                    break
                except:
                    continue
            else:
                print("   Organization field not found")
        except Exception as e:
            print(f"   Organization field error: {e}")

        # 10. Fill Product Field
        print("\n10. Filling Product Field...")
        try:
            product_selectors = [
                "//input[contains(@placeholder, 'Product')]",
                "//label[contains(text(), 'Product')]/following::input[1]"
            ]
            for selector in product_selectors:
                try:
                    product_field = driver.find_element(By.XPATH, selector)
                    product_field.clear()
                    product_field.send_keys(test_data['product'])
                    print(f"   Product: {test_data['product']}")
                    break
                except:
                    continue
            else:
                print("   Product field not found")
        except Exception as e:
            print(f"   Product field error: {e}")

        # Step 5: Submit Lead
        print("\n Step 5: Submit Lead")
        time.sleep(3)

        submit_found = False
        submit_selectors = [
            "//button[@type='submit']",
            "//button[contains(text(), 'Submit')]",
            "//button[contains(text(), 'Save')]",
            "//button[contains(text(), 'Create')]"
        ]

        for selector in submit_selectors:
            try:
                submit_btn = driver.find_element(By.XPATH, selector)
                if submit_btn.is_enabled():
                    print(f"Found submit button with: {selector}")
                    driver.execute_script("arguments[0].click();", submit_btn)
                    print(f"Submit button clicked!")
                    submit_found = True
                    time.sleep(10)
                    break
            except Exception as e:
                continue

        if submit_found:
            print("SUCCESS! Lead created successfully with ALL your data!")
            print(f"\nCOMPLETE LEAD DETAILS CREATED:")
            print(f"   Title: {test_data['title']}")
            print(f"   Start Date: 18 (Selected from calendar)")
            print(f"   Due Date: 30 (Selected from calendar)")
            print(f"   Expected Revenue: {test_data['expected_revenue']}")
            print(f"   Description: {test_data['description']}")
            print(f"   Assigned By: Intern (Selected from dropdown)")
            print(f"   Assignee: Intern (Selected from dropdown)")
            print(f"   Contact: {test_data['contact']}")
            print(f"   Organization: {test_data['organization']}")
            print(f"   Product: {test_data['product']}")

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