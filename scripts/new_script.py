import re
import time
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- DATA CLASS ---
class RegistrationData:
    URL = "https://authorized-partner.vercel.app/register?step=setup"
    USER_EMAIL = "roshant99@yopmail.com"
    PASSWORD = "98035bobU!"

# --- PAGE OBJECTS ---
class BasePage:
    """Base class for common browser actions."""
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def find(self, locator: tuple):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: tuple):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator: tuple, text: str):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

class RegistrationPage(BasePage):
    """Encapsulates interaction with the registration form."""
    
    # Locators
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    COMBOBOX = (By.CSS_SELECTOR, "button[role='combobox']")
    OTP_INPUT = (By.CSS_SELECTOR, "input[maxlength='6']")

    def select_dropdown(self, text: str):
        self.click(self.COMBOBOX)
        xpath = f"//*[contains(@role, 'option')]//*[contains(text(), '{text}')] | //*[contains(@role, 'option') and contains(text(), '{text}')]"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def select_multi_dropdown(self, options: List[str]):
        self.click(self.COMBOBOX)
        for opt in options:
            xpath = f"//*[contains(@role, 'option')]//*[contains(text(), '{opt}')]"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    def tick_checkboxes(self, labels: List[str]):
        for lbl in labels:
            xpath = f"//label[contains(text(), '{lbl}')]"
            self.click((By.XPATH, xpath))

class YopmailHelper:
    """Utility to handle OTP extraction from Yopmail."""
    @staticmethod
    def get_otp(driver, email: str) -> Optional[str]:
        user = email.split('@')[0]
        orig_window = driver.current_window_handle
        
        driver.execute_script("window.open('https://yopmail.com/', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        
        try:
            wait = WebDriverWait(driver, 15)
            # Input username
            wait.until(EC.visibility_of_element_located((By.ID, "login"))).send_keys(user + Keys.ENTER)
            
            # Inbox Handling
            for _ in range(5):
                driver.switch_to.default_content()
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "ifinbox")))
                emails = driver.find_elements(By.CSS_SELECTOR, "div.m")
                if emails:
                    emails[0].click()
                    break
                driver.switch_to.default_content()
                driver.find_element(By.ID, "refresh").click()
                time.sleep(2)

            # Email Content Handling
            driver.switch_to.default_content()
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "ifmail")))
            body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text
            
            match = re.search(r'\b(\d{6})\b', body)
            return match.group(1) if match else None
        finally:
            driver.close()
            driver.switch_to.window(orig_window)

# --- MAIN EXECUTION ---
def run_automation():
    driver = webdriver.Chrome()
    driver.maximize_window()
    page = RegistrationPage(driver)
    data = RegistrationData()

    try:
        driver.get(data.URL)

        # Step 1: Account
        print("[1/4] Filling Account Details...")
        page.type((By.NAME, "firstName"), "Roshan")
        page.type((By.NAME, "lastName"), "Gurung")
        page.type((By.NAME, "email"), data.USER_EMAIL)
        page.type((By.NAME, "phoneNumber"), "9800564571")
        page.type((By.NAME, "password"), data.PASSWORD)
        page.type((By.NAME, "confirmPassword"), data.PASSWORD)
        page.click(page.SUBMIT_BTN)

        # Step 2: OTP
        print("[2/4] Retrieving OTP...")
        otp_code = YopmailHelper.get_otp(driver, data.USER_EMAIL)
        if otp_code:
            page.type(page.OTP_INPUT, otp_code)
            page.click(page.SUBMIT_BTN)
        else:
            raise Exception("OTP not found")

        # Step 3: Agency Details
        print("[3/4] Filling Agency Details...")
        page.type((By.NAME, "agency_name"), "ClassEduCons")
        page.type((By.NAME, "role_in_agency"), "HR")
        page.type((By.NAME, "agency_email"), "ClassEduCons@yopmail.com")
        page.type((By.NAME, "agency_website"), "https://ClassEduCons.com")
        page.type((By.NAME, "agency_address"), "Charlotte")
        page.select_dropdown("Australia")
        page.click(page.SUBMIT_BTN)

        # Step 4: Business & Experience
        print("[4/4] Finalizing Business Details...")
        page.select_dropdown("3-5 years")
        page.tick_checkboxes(["Student Recruitment", "Counseling"])
        page.type((By.NAME, "number_of_students_recruited_annually"), "40")
        page.click(page.SUBMIT_BTN)

        print("✔ Workflow completed successfully.")
        
    except Exception as e:
        print(f"✘ Automation failed: {e}")
    finally:
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    run_automation()