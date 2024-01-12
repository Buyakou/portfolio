from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the web driver
driver = webdriver.Chrome()

# Open a web page with a form
driver.get("https://www.example.com/login")

# Fill in the form fields
username_input = driver.find_element(By.ID, "username")
password_input = driver.find_element(By.ID, "password")

username_input.send_keys("your_username")
password_input.send_keys("your_password")

# Submit the form
password_input.submit()

# Close the browser
driver.quit()
