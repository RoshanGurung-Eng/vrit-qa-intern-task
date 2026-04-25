from dataclasses import dataclass, field
from typing import List

@dataclass
class RegistrationPayload:
    """Immutable registration data container."""
    # Account
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str
    
    # Agency
    agency_name: str
    role_in_agency: str
    agency_email: str
    agency_website: str
    agency_address: str
    country: str
    
    # Business
    experience_range: str
    services: List[str] = field(default_factory=list)
    students_annually: str = "40"
    
    def __post_init__(self):
        if not self.services:
            self.services = ["Student Recruitment", "Counseling"]