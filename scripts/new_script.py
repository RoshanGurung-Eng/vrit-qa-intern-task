from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re

# --- CONFIGURATION ---
URL = "https://authorized-partner.vercel.app/register?step=setup"
EMAIL = "roshant99@yopmail.com"

# --- HELPER FUNCTIONS ---

def fill(driver, name, value):
    """Wait for input and fill it."""
    el = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.NAME, name))
    )
    el.clear()
    el.send_keys(value)

def click_submit(driver):
    """Finds and clicks the primary submit button."""
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    btn.click()

def pick(driver, text):
    """Handles Shadcn/Radix-style single dropdowns."""
    try:
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[role='combobox']"))
        )
        btn.click()
        
        # Look for the option in the newly opened portal
        option_xpath = f"//*[contains(@role, 'option')]//*[contains(text(), '{text}')] | //*[contains(@role, 'option') and contains(text(), '{text}')]"
        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        option.click()
    except Exception as e:
        print(f"Error picking {text}: {e}")

def pick_multi(driver, options):
    """Handles multi-select dropdowns by clicking each option."""
    try:
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[role='combobox']"))
        )
        btn.click()
        
        for opt in options:
            option_xpath = f"//*[contains(@role, 'option')]//*[contains(text(), '{opt}')] | //*[contains(@role, 'option') and contains(text(), '{opt}')]"
            el = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            el.click()
        
        # Click outside to close
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    except Exception as e:
        print(f"Error in pick_multi: {e}")

def tick(driver, labels):
    """Finds labels and clicks their associated checkboxes."""
    for lbl in labels:
        try:
            xpath = f"//label[contains(text(), '{lbl}')]"
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except:
            pass

def get_otp(driver, email):
    """Extracts 6-digit OTP from Yopmail."""
    user = email.split('@')[0]
    orig_window = driver.current_window_handle
    
    driver.execute_script("window.open('https://yopmail.com/', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    
    try:
        fill(driver, "login", user)
        driver.find_element(By.ID, "login").send_keys(Keys.ENTER)
        
        # Wait for the inbox frame and refresh if empty
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "ifinbox")))
        
        # Retry loop for email arrival
        for _ in range(5): 
            emails = driver.find_elements(By.CSS_SELECTOR, "div.m")
            if emails:
                emails[0].click()
                break
            driver.switch_to.default_content()
            driver.find_element(By.ID, "refresh").click()
            time.sleep(2)
            driver.switch_to.frame("ifinbox")

        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "ifmail")))
        
        body_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        ).text
        
        otp_match = re.search(r'\b(\d{6})\b', body_text)
        return otp_match.group(1) if otp_match else None
    finally:
        driver.close()
        driver.switch_to.window(orig_window)

# --- EXECUTION ---

driver = webdriver.Chrome()
driver.maximize_window()

try:
    driver.get(URL)

    # Step 1: Account Setup
    fill(driver, "firstName", "Roshan")
    fill(driver, "lastName", "Gurung")
    fill(driver, "email", EMAIL)
    fill(driver, "phoneNumber", "9800564571")
    fill(driver, "password", "98035bobU!")
    fill(driver, "confirmPassword", "98035bobU!")
    click_submit(driver)

    # Step 2: OTP
    otp = get_otp(driver, EMAIL)
    if otp:
        otp_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[maxlength='6']"))
        )
        otp_input.send_keys(otp)
        click_submit(driver)

    # Page 2: Agency Details
    fill(driver, "agency_name", "ClassEduCons")
    fill(driver, "role_in_agency", "HR")
    fill(driver, "agency_email", "ClassEduCons@yopmail.com")
    fill(driver, "agency_website", "https://ClassEduCons.com")
    fill(driver, "agency_address", "Charlotte")
    pick(driver, "Australia")
    click_submit(driver)

    # Page 3: Experience
    pick(driver, "3-5 years")
    tick(driver, ["Student Recruitment", "Counseling"])
    fill(driver, "number_of_students_recruited_annually", "40")
    fill(driver, "focus_area", "Ohio")
    fill(driver, "success_metrics", "67")
    click_submit(driver)

    # Page 4: Business Details
    fill(driver, "business_registration_number", "1232")
    pick_multi(driver, ["France", "New Zealand"])
    tick(driver, ["Universities", "Colleges", "Vocational School"])
    fill(driver, "certification_details", "ICEF Certified")
    click_submit(driver)

    print("Form submitted successfully.")
    time.sleep(5)

finally:
    driver.quit()