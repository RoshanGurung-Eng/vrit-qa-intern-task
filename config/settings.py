import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class BrowserConfig:
    headless: bool = os.getenv("HEADLESS", "false").lower() == "true"
    implicit_wait: int = int(os.getenv("IMPLICIT_WAIT", "10"))
    explicit_wait: int = int(os.getenv("EXPLICIT_WAIT", "20"))
    screenshot_on_failure: bool = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"

@dataclass(frozen=True)
class AppConfig:
    base_url: str = os.getenv("BASE_URL", "https://authorized-partner.vercel.app/register?step=setup")
    yopmail_url: str = "https://yopmail.com"
    otp_retry_attempts: int = int(os.getenv("OTP_RETRY_ATTEMPTS", "5"))
    otp_retry_delay: int = int(os.getenv("OTP_RETRY_DELAY", "2"))

@dataclass
class UserData:
    email: str = os.getenv("USER_EMAIL", "roshant99@yopmail.com")
    password: str = os.getenv("USER_PASSWORD", "98035bobU!")
    first_name: str = "Roshan"
    last_name: str = "Gurung"
    phone: str = "9800564571"
    
    # Agency Data
    agency_name: str = "ClassEduCons"
    agency_role: str = "HR"
    agency_email: str = "ClassEduCons@yopmail.com"
    agency_website: str = "https://ClassEduCons.com"
    agency_address: str = "Charlotte"
    country: str = "Australia"
    experience: str = "3-5 years"
    services: list = None
    students_recruited: str = "40"
    
    def __post_init__(self):
        if self.services is None:
            self.services = ["Student Recruitment", "Counseling"]