from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

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

def close_popup():
    try:
        # Locate and close the popup if it appears
        popup = driver.find_element(By.ID, "ar-traffic-capture")
        close_button = popup.find_element(By.CSS_SELECTOR, "button[aria-label='Close']")
        close_button.click()
        print("Closed the popup")
    except Exception as e:
        # Popup not found or already closed
        print("No popup to close")

try:
    # Open Aritzia website
    driver.get("https://www.aritzia.com/en/sale")
    driver.maximize_window()
    time.sleep(2)  # Wait for the page to load

    # Locate the product grid container
    try:
        product_grid = driver.find_element(By.CLASS_NAME, "ar-product-grid__container")
        print("Found the grid")
    except Exception as e:
        print(f"Error locating the product grid: {e}")
        driver.quit()
        exit()

    # Scroll down slowly
    stop_scrolling = 0
    while True:
        stop_scrolling += 1
        # close_popup()  # Check and close popup if it appears
        driver.execute_script("window.scrollBy(0,60)")
        time.sleep(0.1)
        if stop_scrolling > 60:  # Adjust the number to control the total scroll duration
            break
    time.sleep(3)
    # close_popup()  # Check and close popup if it appears
    # Extract and print text from each <li> with class "ar-product-grid__tile"
    try:
        product_list = product_grid.find_elements(By.CLASS_NAME, "ar-product-grid__tile")
        print(f"Number of product tiles found: {len(product_list)}")
        with open("aritzia.txt", "w") as file:
            for index, product in enumerate(product_list):
                try:
                    product_text = product.text
                    print(f"Product {index}: {product_text}")
                    file.write(f"Product {index}: {product_text}\n\n")
                except Exception as e:
                    print(f"Error extracting text from product at index {index}: {e}")
                    print(f"HTML of the problematic item:\n{product.get_attribute('outerHTML')}")
    except Exception as e:
        print(f"Error extracting product details: {e}")

finally:
    # Close the WebDriver
    driver.quit()
