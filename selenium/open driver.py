from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the web driver (e.g., Chrome)
driver = webdriver.Chrome()

# Open a web page
driver.get("https://www.example.com")

# Find an element by its ID and print the text
element = driver.find_element(By.ID, "example_id")
print("Element text:", element.text)

# Close the browser
driver.quit()
