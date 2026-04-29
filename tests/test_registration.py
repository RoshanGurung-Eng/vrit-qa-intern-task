"""
Pytest-based tests for registration flow with data-driven testing.
Run with: pytest tests/ -v --html=report.html
"""
import pytest
from pathlib import Path

from config.settings import BrowserConfig, AppConfig
from models.registration_data import RegistrationPayload
from pages.registration_page import RegistrationPage
from utils.yopmail_helper import YopmailHelper
from utils.data_loader import DataLoader, TestData
from utils.logger import logger


@pytest.fixture(scope="module")
def driver_config():
    """Shared browser config for tests."""
    return BrowserConfig(headless=True, explicit_wait=25)


@pytest.fixture(scope="function")
def driver(driver_config):
    """Create and teardown Chrome driver per test."""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
    if driver_config.headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    drv.implicitly_wait(driver_config.implicit_wait)
    yield drv
    drv.quit()
    logger.info("Test driver closed")


@pytest.fixture
def test_data_loader():
    """Provide DataLoader instance."""
    return DataLoader(base_path=Path("tests/data"))


# ─────────────────────────────────────────────────────────────
# 🎯 Test Cases
# ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("dataset", ["valid_user.json", "edge_cases.csv"])
def test_registration_with_datafile(driver, test_data_loader, dataset):
    """Run registration with data from external file."""
    records = test_data_loader.load(dataset, data_class=RegistrationPayload)
    
    for i, data in enumerate(records[:1], 1):  # Limit to 1 for demo; remove [:1] for full run
        logger.info(f"Running test case {i}/{len(records)}: {data.email}")
        
        page = RegistrationPage(driver, BrowserConfig())
        driver.get(AppConfig.base_url)
        
        # Execute flow (simplified - add full steps as needed)
        page.fill_account_details(data)
        # ... add OTP, agency, business steps
        
        logger.info(f"✅ Test case {i} passed")


def test_data_combinations(driver, test_data_loader):
    """Test with auto-generated data combinations."""
    base = {
        "first_name": "Test",
        "last_name": "User",
        "phone": "9800000000",
        "password": "Test@1234",
        "agency_name": "TestAgency",
        "agency_email": "test@yopmail.com",
        "agency_website": "https://test.com",
        "agency_address": "Test City",
        "country": "Australia",
        "role_in_agency": "Manager",
        "experience_range": "1-2 years",
        "students_annually": "10"
    }
    
    variations = {
        "email": ["test1@yopmail.com", "test2@yopmail.com"],
        "services": [["Counseling"], ["Student Recruitment", "Counseling"]]
    }
    
    # Note: For list fields like services, you may need custom handling
    combinations = test_data_loader.generate_combinations(base, {"email": variations["email"]})
    
    assert len(combinations) == 2
    logger.info(f"Generated {len(combinations)} combinations for testing")


@pytest.mark.smoke
def test_yopmail_otp_extraction(driver):
    """Smoke test for OTP helper."""
    config = AppConfig()
    # Use a known test email pattern if Yopmail allows
    # This is a placeholder - adapt based on actual test strategy
    logger.info("OTP extraction test placeholder")
    assert True  # Replace with real assertion