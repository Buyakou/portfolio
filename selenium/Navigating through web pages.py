from selenium import webdriver

# Initialize the web driver
driver = webdriver.Chrome()

# Open multiple web pages
driver.get("https://www.example.com/page1")
print("Page 1 Title:", driver.title)

driver.get("https://www.example.com/page2")
print("Page 2 Title:", driver.title)

# Navigate back to the previous page
driver.back()
print("Title of the previous page:", driver.title)

# Close the browser
driver.quit()
