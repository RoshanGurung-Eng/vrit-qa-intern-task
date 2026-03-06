from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://authorized-partner.vercel.app/register?step=setup")

first_name = driver.find_element(By.NAME, "firstName")
first_name.send_keys("Roshan")

last_name = driver.find_element(By.NAME, "lastName")
last_name.send_keys("Gurung")

email = driver.find_element(By.NAME, "email")
email.send_keys("roshantheaomine@gmail.com")

phone_number = driver.find_element(By.NAME, "phoneNumber")
phone_number.send_keys("9803564454")

password = driver.find_element(By.NAME, "password")
password.send_keys("98035bobU!")

confirm_password = driver.find_element(By.NAME, "confirmPassword")
confirm_password.send_keys("98035bobU!")

submit_next_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
submit_next_btn.click()


input("Script complete!")
driver.quit()