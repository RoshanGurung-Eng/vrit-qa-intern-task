import re
import time
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from config.settings import AppConfig
from utils.logger import logger
from exceptions.automation_errors import OTPExtractionError

class YopmailHelper:
    """Utility for OTP extraction from Yopmail with retry logic."""
    
    OTP_PATTERN = re.compile(r'\b\d{6}\b')
    
    @classmethod
    def get_otp(cls, driver, email: str, config: AppConfig) -> str:
        """
        Extract OTP from Yopmail inbox with retry mechanism.
        
        Raises:
            OTPExtractionError: If OTP cannot be retrieved after retries.
        """
        username = email.split('@')[0]
        original_window = driver.current_window_handle
        
        try:
            driver.execute_script("window.open('', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(config.yopmail_url)
            
            wait = WebDriverWait(driver, config.explicit_wait)
            
            # Login to Yopmail
            wait.until(EC.visibility_of_element_located((By.ID, "login"))).send_keys(
                username + Keys.ENTER
            )
            
            # Wait for email with retries
            for attempt in range(config.otp_retry_attempts):
                logger.debug(f"Checking inbox (attempt {attempt + 1}/{config.otp_retry_attempts})")
                
                driver.switch_to.default_content()
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "ifinbox")))
                
                emails = driver.find_elements(By.CSS_SELECTOR, "div.m")
                if emails:
                    emails[0].click()
                    logger.info("Opened latest email")
                    break
                
                driver.switch_to.default_content()
                driver.find_element(By.ID, "refresh").click()
                time.sleep(config.otp_retry_delay)
            else:
                raise OTPExtractionError("No emails found after retries")
            
            # Extract OTP from email body
            driver.switch_to.default_content()
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "ifmail")))
            body_text = wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            ).text
            
            otp_match = cls.OTP_PATTERN.search(body_text)
            if otp_match:
                otp = otp_match.group(1)
                logger.info("OTP extracted successfully")
                return otp
            
            raise OTPExtractionError(f"OTP pattern not found in email. Content preview: {body_text[:200]}")
            
        finally:
            driver.close()
            driver.switch_to.window(original_window)
            logger.debug("Returned to original window")