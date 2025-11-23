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

    print(f"📄 Current page: {driver.current_url}")

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

    if plus_clicked:
        print(" PLUS BUTTON CLICKED SUCCESSFULLY!")
        time.sleep(8)

        # Step 4: Fill ALL Lead Form Fields with your specific data
        print("\n Step 4: Fill ALL Lead Form Fields")
        time.sleep(5)

        # Your specific test data for EVERY field
        test_data = {
            'start_date': '18.11.25',
            'due_date': '30.11.25',
            'title': 'Testing',
            'expected_revenue': '10000',
            'description': 'Automated test lead description',
            'assigned_by': 'Intern',
            'assignee': 'Intern',
            'contact': 'Test Contact',
            'organization': 'Test Organization',
            'product': 'Test Product'
        }

        print("📝 Filling all form fields with your data...")

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
                    print(f"   ✅ Title: {test_data['title']}")
                    break
                except:
                    continue
            else:
                print("   ❌ Title field not found")
        except Exception as e:
            print(f"   ❌ Title field error: {e}")

        # 2. Fill Start Date Field
        print("\n2. Filling Start Date Field...")
        try:
            start_date_selectors = [
                "//input[@id='module_startdate']",
                "//input[contains(@placeholder, 'Start Date')]",
                "//input[contains(@placeholder, 'Start date')]",
                "//label[contains(text(), 'Start Date')]/following::input[1]"
            ]
            for selector in start_date_selectors:
                try:
                    start_field = driver.find_element(By.XPATH, selector)
                    start_field.clear()
                    start_field.send_keys(test_data['start_date'])
                    print(f"   ✅ Start Date: {test_data['start_date']}")
                    break
                except:
                    continue
            else:
                print("   ❌ Start Date field not found")
        except Exception as e:
            print(f"   ❌ Start Date field error: {e}")

        # 3. Fill Due Date Field
        print("\n3. Filling Due Date Field...")
        try:
            due_date_selectors = [
                "//input[@id='module_duedate']",
                "//input[contains(@placeholder, 'Due Date')]",
                "//input[contains(@placeholder, 'Due date')]",
                "//label[contains(text(), 'Due Date')]/following::input[1]"
            ]
            for selector in due_date_selectors:
                try:
                    due_field = driver.find_element(By.XPATH, selector)
                    due_field.clear()
                    due_field.send_keys(test_data['due_date'])
                    print(f"   ✅ Due Date: {test_data['due_date']}")
                    break
                except:
                    continue
            else:
                print("   ❌ Due Date field not found")
        except Exception as e:
            print(f"   ❌ Due Date field error: {e}")

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
                    print(f"   ✅ Expected Revenue: {test_data['expected_revenue']}")
                    break
                except:
                    continue
            else:
                print("   ❌ Expected Revenue field not found")
        except Exception as e:
            print(f"   ❌ Expected Revenue field error: {e}")

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
                    print(f"   ✅ Description: {test_data['description']}")
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
                        print(f"   ✅ Description: {test_data['description']}")
                        description_filled = True
                        break
                    except:
                        continue
            except:
                pass

        if not description_filled:
            try:
                # Try input field for description
                desc_fields = driver.find_elements(By.XPATH, "//input[contains(@placeholder, 'Description')]")
                for desc_field in desc_fields:
                    try:
                        desc_field.clear()
                        desc_field.send_keys(test_data['description'])
                        print(f"   ✅ Description: {test_data['description']}")
                        description_filled = True
                        break
                    except:
                        continue
            except Exception as e:
                print(f"   ❌ Description field error: {e}")

        # 6. Fill Assigned By Field
        print("\n6. Filling Assigned By Field...")
        try:
            assigned_by_selectors = [
                "//input[contains(@placeholder, 'Assigned By')]",
                "//label[contains(text(), 'Assigned By')]/following::input[1]",
                "//select[contains(@name, 'assigned_by')]",
                "//div[contains(text(), 'Assigned By')]/following::input[1]"
            ]
            for selector in assigned_by_selectors:
                try:
                    assigned_by_field = driver.find_element(By.XPATH, selector)
                    if assigned_by_field.tag_name == 'select':
                        from selenium.webdriver.support.ui import Select

                        select = Select(assigned_by_field)
                        select.select_by_visible_text(test_data['assigned_by'])
                    else:
                        assigned_by_field.clear()
                        assigned_by_field.send_keys(test_data['assigned_by'])
                    print(f"   ✅ Assigned By: {test_data['assigned_by']}")
                    break
                except:
                    continue
            else:
                print("   ❌ Assigned By field not found")
        except Exception as e:
            print(f"   ❌ Assigned By field error: {e}")

        # 7. Fill Assignee Field
        print("\n7. Filling Assignee Field...")
        try:
            assignee_selectors = [
                "//input[contains(@placeholder, 'Assignee')]",
                "//input[contains(@placeholder, 'Select Assignee')]",
                "//label[contains(text(), 'Assignee')]/following::input[1]",
                "//select[contains(@name, 'assignee')]"
            ]
            for selector in assignee_selectors:
                try:
                    assignee_field = driver.find_element(By.XPATH, selector)
                    if assignee_field.tag_name == 'select':
                        from selenium.webdriver.support.ui import Select

                        select = Select(assignee_field)
                        select.select_by_visible_text(test_data['assignee'])
                    else:
                        assignee_field.clear()
                        assignee_field.send_keys(test_data['assignee'])
                    print(f"   ✅ Assignee: {test_data['assignee']}")
                    break
                except:
                    continue
            else:
                print("   ❌ Assignee field not found")
        except Exception as e:
            print(f"   ❌ Assignee field error: {e}")

        # 8. Fill Contact Field
        print("\n8. Filling Contact Field...")
        try:
            contact_selectors = [
                "//input[contains(@placeholder, 'Contact')]",
                "//input[contains(@placeholder, 'Select Contact')]",
                "//label[contains(text(), 'Contact')]/following::input[1]",
                "//select[contains(@name, 'contact')]"
            ]
            for selector in contact_selectors:
                try:
                    contact_field = driver.find_element(By.XPATH, selector)
                    if contact_field.tag_name == 'select':
                        from selenium.webdriver.support.ui import Select

                        select = Select(contact_field)
                        select.select_by_visible_text(test_data['contact'])
                    else:
                        contact_field.clear()
                        contact_field.send_keys(test_data['contact'])
                    print(f"   ✅ Contact: {test_data['contact']}")
                    break
                except:
                    continue
            else:
                print("   ❌ Contact field not found")
        except Exception as e:
            print(f"   ❌ Contact field error: {e}")

        # 9. Fill Organization Field
        print("\n9. Filling Organization Field...")
        try:
            org_selectors = [
                "//input[contains(@placeholder, 'Organization')]",
                "//label[contains(text(), 'Organization')]/following::input[1]",
                "//select[contains(@name, 'organization')]"
            ]
            for selector in org_selectors:
                try:
                    org_field = driver.find_element(By.XPATH, selector)
                    if org_field.tag_name == 'select':
                        from selenium.webdriver.support.ui import Select

                        select = Select(org_field)
                        select.select_by_visible_text(test_data['organization'])
                    else:
                        org_field.clear()
                        org_field.send_keys(test_data['organization'])
                    print(f"   ✅ Organization: {test_data['organization']}")
                    break
                except:
                    continue
            else:
                print("   ❌ Organization field not found")
        except Exception as e:
            print(f"   ❌ Organization field error: {e}")

        # 10. Fill Product Field
        print("\n10. Filling Product Field...")
        try:
            product_selectors = [
                "//input[contains(@placeholder, 'Product')]",
                "//label[contains(text(), 'Product')]/following::input[1]",
                "//select[contains(@name, 'product')]"
            ]
            for selector in product_selectors:
                try:
                    product_field = driver.find_element(By.XPATH, selector)
                    if product_field.tag_name == 'select':
                        from selenium.webdriver.support.ui import Select

                        select = Select(product_field)
                        select.select_by_visible_text(test_data['product'])
                    else:
                        product_field.clear()
                        product_field.send_keys(test_data['product'])
                    print(f"   ✅ Product: {test_data['product']}")
                    break
                except:
                    continue
            else:
                print("   ❌ Product field not found")
        except Exception as e:
            print(f"   ❌ Product field error: {e}")

        # Step 5: Submit Lead
        print("\n Step 5: Submit Lead")
        time.sleep(3)

        submit_found = False
        submit_selectors = [
            "//button[@type='submit']",
            "//button[contains(@class, 'ti-btn') and contains(@class, 'bg-primary')]",
            "//button[contains(text(), 'Submit')]",
            "//button[contains(text(), 'Save')]",
            "//button[contains(text(), 'Create')]"
        ]

        for selector in submit_selectors:
            try:
                submit_btn = driver.find_element(By.XPATH, selector)
                if submit_btn.is_enabled():
                    print(f"✅ Found submit button with: {selector}")
                    driver.execute_script("arguments[0].click();", submit_btn)
                    print(f"✅ Submit button clicked!")
                    submit_found = True
                    time.sleep(10)
                    break
            except Exception as e:
                continue

        if submit_found:
            print("🎉 SUCCESS! Lead created successfully with ALL your data!")
            print(f"\n📋 COMPLETE LEAD DETAILS CREATED:")
            print(f"   ┌─────────────────────────────────────")
            print(f"   │ Title: {test_data['title']}")
            print(f"   │ Start Date: {test_data['start_date']}")
            print(f"   │ Due Date: {test_data['due_date']}")
            print(f"   │ Expected Revenue: {test_data['expected_revenue']}")
            print(f"   │ Description: {test_data['description']}")
            print(f"   │ Assigned By: {test_data['assigned_by']}")
            print(f"   │ Assignee: {test_data['assignee']}")
            print(f"   │ Contact: {test_data['contact']}")
            print(f"   │ Organization: {test_data['organization']}")
            print(f"   │ Product: {test_data['product']}")
            print(f"   └─────────────────────────────────────")

            time.sleep(5)
            print(f"\n📄 Current URL after submission: {driver.current_url}")
        else:
            print("❌ Could not find or click submit button")

    else:
        print("❌ FAILED: Could not find navigation PLUS button")

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback

    print(f"🔍 Details: {traceback.format_exc()}")

finally:
    print("\n" + "=" * 50)
    print(" AUTOMATION COMPLETED")
    print("=" * 50)
    input("Press Enter to close browser...")
    driver.quit()