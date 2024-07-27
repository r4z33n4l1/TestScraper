import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless")  # Uncomment this line to run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")  # Suppress logs
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppress logs

# Specify the path to chromedriver if it's not in your PATH
service = Service('./chromedriver.exe')  # Update this path to the new ChromeDriver

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open Pinterest login page
    driver.get("https://www.pinterest.com")
    driver.maximize_window()
    time.sleep(10)  # Wait for user to manually log in

    # Save cookies to a file
    with open('cookies.pkl', 'wb') as file:
        pickle.dump(driver.get_cookies(), file)
    print("Cookies have been saved")

finally:
    # Close the WebDriver
    driver.quit()
