from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from utils.logger import logger

class RegistrationPage(BasePage):
    """Page Object for Registration workflow."""
    
    class Locators:
        """Centralized locator definitions."""
        # Step 1: Account
        FIRST_NAME = (By.NAME, "firstName")
        LAST_NAME = (By.NAME, "lastName")
        EMAIL = (By.NAME, "email")
        PHONE = (By.NAME, "phoneNumber")
        PASSWORD = (By.NAME, "password")
        CONFIRM_PASSWORD = (By.NAME, "confirmPassword")
        
        # Common
        SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
        COMBOBOX = (By.CSS_SELECTOR, "button[role='combobox']")
        OTP_INPUT = (By.CSS_SELECTOR, "input[maxlength='6']")
        
        # Step 3: Agency
        AGENCY_NAME = (By.NAME, "agency_name")
        ROLE = (By.NAME, "role_in_agency")
        AGENCY_EMAIL = (By.NAME, "agency_email")
        WEBSITE = (By.NAME, "agency_website")
        ADDRESS = (By.NAME, "agency_address")
        
        # Step 4: Business
        EXPERIENCE = (By.NAME, "experience")  # Adjust selector as needed
        STUDENTS_COUNT = (By.NAME, "number_of_students_recruited_annually")
        CHECKBOX_LABEL = "//label[contains(text(), '{label}')]"
        DROPDOWN_OPTION = "//*[contains(@role, 'option') and contains(., '{text}')]"
    
    def fill_account_details(self, data) -> None:
        """Complete Step 1: Account registration."""
        logger.info("Filling account details...")
        self.type(self.Locators.FIRST_NAME, data.first_name, "First Name")
        self.type(self.Locators.LAST_NAME, data.last_name, "Last Name")
        self.type(self.Locators.EMAIL, data.email, "Email")
        self.type(self.Locators.PHONE, data.phone, "Phone")
        self.type(self.Locators.PASSWORD, data.password, "Password")
        self.type(self.Locators.CONFIRM_PASSWORD, data.password, "Confirm Password")
        self.click(self.Locators.SUBMIT_BTN, "Submit Account")
    
    def enter_otp(self, otp: str) -> None:
        """Complete Step 2: OTP verification."""
        logger.info(f"Entering OTP: {otp[:2]}****")
        self.type(self.Locators.OTP_INPUT, otp, "OTP Field")
        self.click(self.Locators.SUBMIT_BTN, "Submit OTP")
    
    def fill_agency_details(self, data) -> None:
        """Complete Step 3: Agency information."""
        logger.info("Filling agency details...")
        fields = [
            (self.Locators.AGENCY_NAME, data.agency_name, "Agency Name"),
            (self.Locators.ROLE, data.agency_role, "Role"),
            (self.Locators.AGENCY_EMAIL, data.agency_email, "Agency Email"),
            (self.Locators.WEBSITE, data.agency_website, "Website"),
            (self.Locators.ADDRESS, data.agency_address, "Address"),
        ]
        for locator, value, desc in fields:
            self.type(locator, value, desc)
        
        self.select_single_dropdown(data.country)
        self.click(self.Locators.SUBMIT_BTN, "Submit Agency")
    
    def fill_business_details(self, data) -> None:
        """Complete Step 4: Business configuration."""
        logger.info("Finalizing business details...")
        self.select_single_dropdown(data.experience)
        self.tick_checkboxes(data.services)
        self.type(self.Locators.STUDENTS_COUNT, data.students_recruited, "Students Recruited")
        self.click(self.Locators.SUBMIT_BTN, "Submit Final")
    
    def select_single_dropdown(self, text: str) -> None:
        """Select single option from combobox dropdown."""
        self.click(self.Locators.COMBOBOX, "Dropdown Toggle")
        xpath = self.Locators.DROPDOWN_OPTION.format(text=text)
        self.click((By.XPATH, xpath), f"Option: {text}")
    
    def tick_checkboxes(self, labels: List[str]) -> None:
        """Select multiple checkbox options."""
        for label in labels:
            xpath = self.Locators.CHECKBOX_LABEL.format(label=label)
            self.click((By.XPATH, xpath), f"Checkbox: {label}")