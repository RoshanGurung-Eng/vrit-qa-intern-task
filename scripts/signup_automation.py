from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re


# Helper function: Fill input fields
def fill(driver, name, value):
    try:
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, name))
        )
        el.clear()
        time.sleep(0.2)
        el.send_keys(value)
    except:
        pass


# Helper function: Select single dropdown option
def pick(driver, text):
    try:
        btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[role='combobox']"))
        )
        btn.click()
        time.sleep(2)
        
        driver.execute_script(f"""
            const t = "{text.lower()}";
            for (const o of document.querySelectorAll('[role="option"], [data-radix-collection-item]')) {{
                const txt = o.textContent?.trim()?.toLowerCase();
                if (txt && txt.includes(t)) {{ o.click(); return; }}
            }}
        """)
        time.sleep(1)
        try:
            driver.find_element(By.TAG_NAME, "body").click()
        except:
            pass
    except:
        pass


# Helper function: Select multiple dropdown options
def pick_multi(driver, options):
    try:
        btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[role='combobox']"))
        )
        btn.click()
        time.sleep(2)
        
        for opt in options:
            driver.execute_script(f"""
                const t = "{opt.lower()}";
                for (const o of document.querySelectorAll('[role="option"], [data-radix-collection-item]')) {{
                    const txt = o.textContent?.trim()?.toLowerCase();
                    if (txt && txt.includes(t) && o.getAttribute('data-selected') !== 'true') {{ o.click(); return; }}
                }}
            """)
            time.sleep(0.5)
        
        time.sleep(1)
        try:
            driver.find_element(By.TAG_NAME, "body").click()
        except:
            pass
    except:
        pass


# Helper function: Tick checkboxes by label text
def tick(driver, labels):
    for lbl in labels:
        for label in driver.find_elements(By.TAG_NAME, "label"):
            if lbl.lower() in label.text.lower():
                try:
                    label.click()
                except:
                    pass
                break


# Helper function: Extract OTP from Yopmail inbox
def get_otp(driver, email):
    user = email.split('@')[0]
    orig = driver.current_window_handle
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get("https://yopmail.com/")
        time.sleep(3)
        
        login = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "login"))
        )
        login.clear()
        login.send_keys(user)
        login.send_keys("\n")
        time.sleep(5)
        
        driver.switch_to.frame(
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.NAME, "ifinbox"))
            )
        )
        emails = driver.find_elements(By.CSS_SELECTOR, "div.m, tr.m")
        if not emails:
            return None
        emails[0].click()
        time.sleep(2)
        
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.NAME, "ifmail"))
        text = driver.find_element(By.TAG_NAME, "body").text
        match = re.search(r'\b(\d{6})\b', text)
        
        driver.switch_to.default_content()
        driver.close()
        driver.switch_to.window(orig)
        return match.group(1) if match else None
    except:
        try:
            driver.switch_to.default_content()
            driver.close()
            driver.switch_to.window(orig)
        except:
            pass
        return None


# Main Script

driver = webdriver.Chrome()
driver.maximize_window()

# Load signup page
driver.get("https://authorized-partner.vercel.app/register?step=setup")
time.sleep(3)

# Step 1: Account Setup
fill(driver, "firstName", "Roshan")
fill(driver, "lastName", "Gurung")
email = "roshant99@yopmail.com"
fill(driver, "email", email)
fill(driver, "phoneNumber", "9800564571")
fill(driver, "password", "98035bobU!")
fill(driver, "confirmPassword", "98035bobU!")

driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(4)

# Step 2: OTP Verification
time.sleep(3)
otp = get_otp(driver, email) or "123456"

try:
    otp_in = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[maxlength='6']"))
    )
    otp_in.clear()
    otp_in.send_keys(otp)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(4)
except:
    pass

# Page 2: Agency Details
time.sleep(3)
fill(driver, "agency_name", "ClassEduCons")
fill(driver, "role_in_agency", "HR")
fill(driver, "agency_email", "ClassEduCons@yopmail.com")
fill(driver, "agency_website", "ClassEduCons.com")
fill(driver, "agency_address", "Chorlette")

pick(driver, "Australia")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(6)

# Page 3: Professional Experience
pick(driver, "3-5 years")
tick(driver, ["Student Recruitment", "Counseling"])
fill(driver, "number_of_students_recruited_annually", "40")
fill(driver, "focus_area", "Ohio")
fill(driver, "success_metrics", "67")

driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(6)

# Page 4: Business Details
fill(driver, "business_registration_number", "1232")
pick_multi(driver, ["France", "New Zealand"])
tick(driver, ["Universities", "Colleges", "Vocational School"])
fill(driver, "certification_details", "ICEF Certified")

# Final Submit
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

time.sleep(5)
driver.quit()