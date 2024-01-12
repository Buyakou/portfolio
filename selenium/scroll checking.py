from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

url = input("Enter the URL: ")

driver = webdriver.Chrome()

try:
    # Open the website
    driver.get(url)

    # Get the current scroll position
    initial_scroll_position = driver.execute_script("return window.scrollY;")

    # Scroll down to trigger additional content loading
    actions = ActionChains(driver)
    actions.send_keys(Keys.END).perform()

    # Get the new scroll position
    new_scroll_position = driver.execute_script("return window.scrollY;")

    # Check if the scroll position has changed
    if new_scroll_position > initial_scroll_position:
        print("Scroll down was successful.")
    else:
        print("Test failed. Scroll did not occur.")

finally:
    # Close the browser window
    driver.quit()
