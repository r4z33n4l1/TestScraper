import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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

def load_cookies(driver, cookies_file):
    with open(cookies_file, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def get_image_sources(driver, file_path):
    # Locate the main div with class name "vbI XiG"
    try:
        main_div = driver.find_element(By.CLASS_NAME, "vbI.XiG")
        print("Found the main div")
    except Exception as e:
        print(f"Error locating the main div: {e}")
        return

    # Initialize a set to keep track of seen image sources to avoid duplicates
    seen_images = set()

    with open(file_path, "a") as file:
        while True:
            try:
                # Find all nested divs with class "Yl- MIw Hb7"
                nested_divs = main_div.find_elements(By.CLASS_NAME, "Yl-.MIw.Hb7")
                for index, div in enumerate(nested_divs):
                    try:
                        img = div.find_element(By.TAG_NAME, "img")
                        img_src = img.get_attribute("src")
                        if img_src not in seen_images:
                            seen_images.add(img_src)
                            print(f"Image {index}: {img_src}")
                            file.write(f"{img_src}\n")
                    except Exception as e:
                        print(f"Error extracting image source from div at index {index}: {e}")
                
                # Scroll down to load more content
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(2)  # Wait for new content to load

            except Exception as e:
                print(f"Error while scrolling and loading new content: {e}")
                break

try:
    # Open Pinterest page
    driver.get("https://www.pinterest.com")
    driver.maximize_window()
    time.sleep(5)  # Wait for the page to load

    # Load cookies from the file
    load_cookies(driver, 'cookies.pkl')

    # Refresh the page to apply cookies
    driver.refresh()
    time.sleep(5)  # Wait for the page to load

    # Now the session should be logged in
    print("Logged in using cookies")

    # Get image sources and append them to the file
    get_image_sources(driver, "image_sources.txt")

finally:
    # Close the WebDriver
    driver.quit()
