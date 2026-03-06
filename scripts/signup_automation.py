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

input("Script complete!")
driver.quit()