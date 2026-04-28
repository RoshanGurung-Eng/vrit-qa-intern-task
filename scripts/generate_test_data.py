#!/usr/bin/env python3
"""Generate sample test data files for automation."""
from utils.data_loader import DataLoader, TestData
from models.registration_data import RegistrationPayload

def main():
    loader = DataLoader("tests/data")
    
    # Sample records
    samples = [
        RegistrationPayload(
            first_name="Roshan", last_name="Gurung",
            email="roshan1@yopmail.com", phone="9800564571",
            password="Secure@123", agency_name="EduConsult1",
            role_in_agency="HR", agency_email="edu1@yopmail.com",
            agency_website="https://edu1.com", agency_address="Kathmandu",
            country="Nepal", experience_range="1-2 years",
            services=["Counseling"], students_annually="20"
        ),
        RegistrationPayload(
            first_name="Sita", last_name="Sharma",
            email="sita@yopmail.com", phone="9801234567",
            password="Strong#456", agency_name="GlobalEdu",
            role_in_agency="Manager", agency_email="global@yopmail.com",
            agency_website="https://globaledu.com", agency_address="Pokhara",
            country="Australia", experience_range="3-5 years",
            services=["Student Recruitment", "Visa Support"], students_annually="75"
        )
    ]
    
    # Save in multiple formats
    loader.save("sample_users", samples, format='json')
    loader.save("sample_users", samples, format='csv')
    loader.save("sample_users", samples, format='excel')
    
    print("✅ Generated test data in tests/data/ (JSON, CSV, Excel)")

if __name__ == "__main__":
    main()