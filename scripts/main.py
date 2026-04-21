#!/usr/bin/env python3
import sys
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import BrowserConfig, AppConfig, UserData
from pages.registration_page import RegistrationPage
from utils.yopmail_helper import YopmailHelper
from utils.logger import logger
from exceptions.automation_errors import AutomationError, OTPExtractionError

def create_driver(browser_config: BrowserConfig) -> webdriver.Chrome:
    """Initialize Chrome driver with professional configuration."""
    options = Options()
    
    if browser_config.headless:
        options.add_argument("--headless=new")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(browser_config.implicit_wait)
    return driver

def execute_registration_flow(driver, user_ UserData, browser_config: BrowserConfig, app_config: AppConfig) -> bool:
    """Execute the complete registration workflow."""
    page = RegistrationPage(driver, browser_config)
    
    try:
        logger.info(f"Starting registration for {user_data.email}")
        driver.get(AppConfig.base_url)
        
        # Step 1: Account Creation
        logger.info("[1/4] Creating account...")
        page.fill_account_details(user_data)
        time.sleep(2)  # Allow transition
        
        # Step 2: OTP Verification
        logger.info("[2/4] Retrieving OTP from Yopmail...")
        otp = YopmailHelper.get_otp(driver, user_data.email, app_config)
        page.enter_otp(otp)
        time.sleep(2)
        
        # Step 3: Agency Details
        logger.info("[3/4] Submitting agency information...")
        page.fill_agency_details(user_data)
        time.sleep(2)
        
        # Step 4: Business Configuration
        logger.info("[4/4] Finalizing business details...")
        page.fill_business_details(user_data)
        
        # Optional: Wait for success confirmation
        time.sleep(3)
        logger.info("✅ Registration workflow completed successfully!")
        return True
        
    except OTPExtractionError as e:
        logger.error(f"OTP Error: {e}")
        return False
    except AutomationError as e:
        logger.error(f"Automation Error: {e}")
        return False
    except Exception as e:
        logger.exception(f"Unexpected error: {type(e).__name__}: {e}")
        return False

def main() -> int:
    """Entry point with proper exit codes."""
    browser_config = BrowserConfig()
    app_config = AppConfig()
    user_data = UserData()
    
    driver = None
    try:
        driver = create_driver(browser_config)
        driver.maximize_window()
        
        success = execute_registration_flow(driver, user_data, browser_config, app_config)
        return 0 if success else 1
        
    except KeyboardInterrupt:
        logger.warning("Automation interrupted by user")
        return 130
    finally:
        if driver:
            time.sleep(2)  # Allow final observations
            driver.quit()
            logger.info("Browser closed")

if __name__ == "__main__":
    sys.exit(main())