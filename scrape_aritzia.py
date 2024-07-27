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

# Specify the path to chromedriver if it's not in your PATH
service = Service('./chromedriver.exe')  # Update this path to the new ChromeDriver

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open Aritzia website
    driver.get("https://www.aritzia.com/en/sale")
    time.sleep(5)  # Wait for the page to load

    # Locate the product grid container
    try:
        product_grid = driver.find_element(By.CSS_SELECTOR, "ul.ar-product-grid__container.js-product-grid__container.list.flex.flex-wrap.justify-between.justify-start-ns")
        print("Found the grid")
    except Exception as e:
        print(f"Error locating the product grid: {e}")
        driver.quit()
        exit()

    # Scroll to load more items until there are at least 100 items
    try:
        while len(product_grid.find_elements(By.TAG_NAME, "li")) < 100:
            driver.execute_script("arguments[0].scrollIntoView(true);", product_grid.find_elements(By.TAG_NAME, "li")[-1])
            time.sleep(2)  # Wait for the new items to load
        print("Loaded 100 items")
    except Exception as e:
        print(f"Error while scrolling and loading items: {e}")

    # Extract product details
    try:
        product_list = product_grid.find_elements(By.TAG_NAME, "li")
        with open("aritzia.txt", "w") as file:
            for product in product_list:
                try:
                    # brand_element = product.find_element(By.CSS_SELECTOR, "div.f0.product-brand.ar-product-brand.js-product-plp-brand.pr4.mt2-ns > h6 > a")
                    # brand = brand_element.text
                    # print(f"Brand: {brand}")
                    # file.write(f"Brand: {brand}\n\n")
                    all_text = product.text
                    print(f"Product: {all_text}")
                    file.write(f"Product: {all_text}\n\n")
                except Exception as e:
                    print(f"Error extracting brand from product")
    except Exception as e:
        print(f"Error extracting product details: {e}")

finally:
    # Close the WebDriver
    driver.quit()
