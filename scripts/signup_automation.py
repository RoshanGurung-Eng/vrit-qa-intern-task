from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://authorized-partner.vercel.app/register?step=setup")

wait = WebDriverWait(driver, 10) 

# 1. Setup Account
first_name = driver.find_element(By.NAME, "firstName")
first_name.send_keys("Roshan")

last_name = driver.find_element(By.NAME, "lastName")
last_name.send_keys("Gurung")

email = driver.find_element(By.NAME, "email")
email.send_keys("roshan_ts@yopmail.com")

phone_number = driver.find_element(By.NAME, "phoneNumber")
phone_number.send_keys("9803564459")

password = driver.find_element(By.NAME, "password")
password.send_keys("98035bobU!")

confirm_password = driver.find_element(By.NAME, "confirmPassword")
confirm_password.send_keys("98035bobU!")

submit_next_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
submit_next_btn.click()

wait.until(EC.presence_of_element_located((By.NAME, "agencyName")))

# 2. Agency Details

agency_name = driver.find_element(By.NAME, "agencyName")
agency_name.send_keys("ClassEduCons")

role = driver.find_element(By.NAME, "role_in_agency")
role.send_keys("HR")

email_of_agency = driver.find_element(By.NAME, "agency_email")
email_of_agency.send_keys("ClassEduCons@yopmail.com")

website = driver.find_element(By.NAME, "agency_website")
website.send_keys("ClassEduCons.com")

submit_next_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
submit_next_btn.click()
# 3. Professional Experience
Number_of_Students_Recruited_Annually = driver.find_element(By.NAME, "number_of_students_recruited_annually")
Number_of_Students_Recruited_Annually.send_keys("40")

Focus_Area = driver.find_element(By.NAME, "focus_area")
Focus_Area.send_keys("Ohio")

Success_Metrics = driver.find_element(By.NAME, "success_metrics")
Success_Metrics.send_keys("67")

submit_next_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
submit_next_btn.click()

# 4. Verification and Preference
Business_Registration_Number = driver.find_element(By.NAME, "business_registration_number")
Business_Registration_Number.send_keys("67")


certification_details = driver.find_element(By.NAME, "certification_details")
certification_details.send_keys("67")

submit_next_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
submit_next_btn.click()

input("Script complete!")
driver.quit()