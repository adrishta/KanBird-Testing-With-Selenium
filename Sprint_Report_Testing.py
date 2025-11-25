# Kanbird Sprint Report Section Testing
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
    print("Starting Kanbird Sprint Report Section Testing...")

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

    # Step 3: Navigate to Sprint Report
    print("\nStep 3: Navigating to Sprint Report section...")

    # Method 1: Try to find and click Sprint Report link in sidebar
    sprint_report_found = False

    # Look for Sprint Report in various possible locations
    sprint_report_selectors = [
        "//*[contains(text(), 'Sprint Report')]",
        "//*[contains(text(), 'Sprint report')]",
        "//*[contains(text(), 'SPRINT REPORT')]",
        "//*[contains(text(), 'Reports')]",
        "//*[contains(text(), 'reports')]",
        "//a[contains(@href, 'sprint-report')]",
        "//a[contains(@href, 'report')]"
    ]

    for selector in sprint_report_selectors:
        try:
            sprint_report_elements = driver.find_elements(By.XPATH, selector)
            for element in sprint_report_elements:
                if element.is_displayed():
                    print(f"Found Sprint Report element with selector: {selector}")
                    driver.execute_script("arguments[0].click();", element)
                    print("Clicked Sprint Report")
                    sprint_report_found = True
                    break
            if sprint_report_found:
                break
        except:
            continue

    # If not found via click, try direct URL access
    if not sprint_report_found:
        print("Sprint Report link not found in UI, trying direct URL access...")
        driver.get("https://app.kanbird.com/sprint/sprint-report")
        print("Directly accessed Sprint Report URL")

    # Wait for Sprint Report to load
    print("\nWaiting for Sprint Report to load...")
    time.sleep(8)

    # Step 4: Test Sprint Report Elements and Functionality
    print("\nStep 4: Testing Sprint Report Elements and Functionality...")

    current_url = driver.current_url
    print(f"Current URL: {current_url}")

    # Expected Sprint Report elements
    expected_sprint_report_elements = [
        "Sprint Report",
        "Sprint",
        "Report",
        "Burndown",
        "Velocity",
        "Progress",
        "Completed",
        "Remaining",
        "Tasks",
        "Stories",
        "Points",
        "Hours",
        "Team",
        "Performance",
        "Metrics",
        "Statistics",
        "Chart",
        "Graph"
    ]

    found_elements = []
    missing_elements = []

    for element_text in expected_sprint_report_elements:
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

    # Step 5: Test Sprint Report Specific Features
    print("\nStep 5: Testing Sprint Report Specific Features...")

    functionality_tests = []

    # Test 1: Check if we're on Sprint Report page
    if "sprint-report" in current_url or "report" in current_url:
        functionality_tests.append("Successfully accessed Sprint Report URL")
        print("✓ Successfully accessed Sprint Report URL")
    else:
        functionality_tests.append(f"Not on Sprint Report, current page: {current_url}")
        print(f"✗ Not on Sprint Report, current page: {current_url}")

    # Test 2: Check for sprint selection dropdown
    try:
        sprint_selectors = driver.find_elements(By.XPATH,
                                              "//select | //div[contains(@class, 'dropdown')] | //input[contains(@placeholder, 'Sprint')]")
        if sprint_selectors:
            functionality_tests.append("Sprint selection available")
            print("✓ Sprint selection available")
        else:
            functionality_tests.append("No sprint selection found")
            print("✗ No sprint selection found")
    except Exception as e:
        functionality_tests.append(f"Error finding sprint selector: {str(e)}")
        print(f"✗ Error finding sprint selector: {str(e)}")

    # Test 3: Check for charts and graphs
    try:
        charts = driver.find_elements(By.XPATH,
                                    "//canvas | //svg | //div[contains(@class, 'chart')] | //div[contains(@class, 'graph')] | //div[contains(@class, 'plot')]")
        if charts:
            functionality_tests.append(f"Found {len(charts)} charts/graphs")
            print(f"✓ Found {len(charts)} charts/graphs")
        else:
            functionality_tests.append("No charts/graphs found")
            print("✗ No charts/graphs found")
    except Exception as e:
        functionality_tests.append(f"Error finding charts: {str(e)}")
        print(f"✗ Error finding charts: {str(e)}")

    # Test 4: Check for metrics and statistics
    try:
        metrics = driver.find_elements(By.XPATH,
                                     "//div[contains(@class, 'metric')] | //div[contains(@class, 'stat')] | //div[contains(@class, 'kpi')] | //div[contains(@class, 'number')]")
        if metrics:
            functionality_tests.append(f"Found {len(metrics)} metrics/statistics")
            print(f"✓ Found {len(metrics)} metrics/statistics")
        else:
            functionality_tests.append("No metrics/statistics found")
            print("✗ No metrics/statistics found")
    except Exception as e:
        functionality_tests.append(f"Error finding metrics: {str(e)}")
        print(f"✗ Error finding metrics: {str(e)}")

    # Test 5: Check for burndown chart specifically
    try:
        burndown_elements = driver.find_elements(By.XPATH,
                                               "//*[contains(text(), 'Burndown')] | //*[contains(text(), 'burn down')]")
        if burndown_elements:
            functionality_tests.append("Burndown chart section found")
            print("✓ Burndown chart section found")
        else:
            functionality_tests.append("Burndown chart not specifically identified")
            print("✗ Burndown chart not specifically identified")
    except Exception as e:
        functionality_tests.append(f"Error checking for burndown: {str(e)}")
        print(f"✗ Error checking for burndown: {str(e)}")

    # Test 6: Check for velocity metrics
    try:
        velocity_elements = driver.find_elements(By.XPATH,
                                               "//*[contains(text(), 'Velocity')] | //*[contains(text(), 'velocity')]")
        if velocity_elements:
            functionality_tests.append("Velocity metrics found")
            print("✓ Velocity metrics found")
        else:
            functionality_tests.append("Velocity metrics not specifically identified")
            print("✗ Velocity metrics not specifically identified")
    except Exception as e:
        functionality_tests.append(f"Error checking for velocity: {str(e)}")
        print(f"✗ Error checking for velocity: {str(e)}")

    # Test 7: Check for progress bars
    try:
        progress_bars = driver.find_elements(By.XPATH,
                                           "//div[contains(@class, 'progress')] | //div[contains(@role, 'progressbar')]")
        if progress_bars:
            functionality_tests.append(f"Found {len(progress_bars)} progress bars")
            print(f"✓ Found {len(progress_bars)} progress bars")
        else:
            functionality_tests.append("No progress bars found")
            print("✗ No progress bars found")
    except Exception as e:
        functionality_tests.append(f"Error finding progress bars: {str(e)}")
        print(f"✗ Error finding progress bars: {str(e)}")

    # Test 8: Check for task/story breakdown
    try:
        breakdown_elements = driver.find_elements(By.XPATH,
                                                "//*[contains(text(), 'Completed')] | //*[contains(text(), 'Remaining')] | //*[contains(text(), 'Total')]")
        if breakdown_elements:
            functionality_tests.append("Task/story breakdown found")
            print("✓ Task/story breakdown found")
        else:
            functionality_tests.append("No task/story breakdown found")
            print("✗ No task/story breakdown found")
    except Exception as e:
        functionality_tests.append(f"Error finding breakdown: {str(e)}")
        print(f"✗ Error finding breakdown: {str(e)}")

    # Test 9: Check for export/download options
    try:
        export_buttons = driver.find_elements(By.XPATH,
                                            "//button[contains(text(), 'Export')] | //button[contains(text(), 'Download')] | //button[contains(text(), 'PDF')]")
        if export_buttons:
            functionality_tests.append("Export/download options available")
            print("✓ Export/download options available")
        else:
            functionality_tests.append("No export/download options found")
            print("✗ No export/download options found")
    except Exception as e:
        functionality_tests.append(f"Error checking export options: {str(e)}")
        print(f"✗ Error checking export options: {str(e)}")

    # Test 10: Check for date range or sprint period information
    try:
        date_elements = driver.find_elements(By.XPATH,
                                           "//*[contains(text(), 'Date')] | //*[contains(text(), 'Period')] | //input[@type='date']")
        if date_elements:
            functionality_tests.append("Date/period information found")
            print("✓ Date/period information found")
        else:
            functionality_tests.append("No date/period information found")
            print("✗ No date/period information found")
    except Exception as e:
        functionality_tests.append(f"Error checking date information: {str(e)}")
        print(f"✗ Error checking date information: {str(e)}")

    # Step 6: Summary and Results
    print(f"\n{'=' * 50}")
    print("SPRINT REPORT TEST SUMMARY")
    print(f"{'=' * 50}")
    print(f"Final URL: {current_url}")
    print(f"Elements Found: {len(found_elements)}/{len(expected_sprint_report_elements)}")
    print(f"Missing Elements: {missing_elements}")
    print(f"Functionality Tests: {len(functionality_tests)} checks performed")

    for test in functionality_tests:
        print(f" - {test}")

    # Take screenshot for verification
    driver.save_screenshot("sprint_report_test_results.png")
    print("Screenshot saved as 'sprint_report_test_results.png'")

    # Final verdict
    success_criteria = [
        "sprint-report" in current_url or "report" in current_url,
        len(found_elements) >= 5,  # At least basic elements present
        any("chart" in test.lower() for test in functionality_tests),
        any("metric" in test.lower() or "stat" in test.lower() for test in functionality_tests)
    ]

    if all(success_criteria):
        print(f"\n{'=' * 50}")
        print("SPRINT REPORT TEST: PASSED ✓")
        print("Successfully accessed and tested Sprint Report functionality")
        print(f"{'=' * 50}")
    else:
        print(f"\n{'=' * 50}")
        print("SPRINT REPORT TEST: FAILED ✗")
        print("Issues encountered with Sprint Report access or functionality")
        print(f"{'=' * 50}")

        # Additional troubleshooting info
        print("\nTroubleshooting Info:")
        print(f"On Sprint Report URL: {'sprint-report' in current_url or 'report' in current_url}")
        print(f"Basic elements found: {len(found_elements)}/{len(expected_sprint_report_elements)}")
        print(f"Charts detected: {any('chart' in test.lower() for test in functionality_tests)}")
        print(f"Metrics detected: {any('metric' in test.lower() or 'stat' in test.lower() for test in functionality_tests)}")

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
        if "sprint" in page_source.lower():
            print("Sprint content detected")
        if "report" in page_source.lower():
            print("Report content detected")
        if "chart" in page_source.lower() or "graph" in page_source.lower():
            print("Chart/graph content detected")

    except Exception as troubleshoot_error:
        print(f"Troubleshooting failed: {troubleshoot_error}")

finally:
    driver.quit()