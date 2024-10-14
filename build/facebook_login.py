from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests_class
class FacebookLogin:
    def __init__(self, chromedriver_path):
        # Set Chrome options to disable notifications
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")  # Disable notifications

        # Initialize the webdriver with options and open the browser
        self.service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)  
        self.open = False
        self.scraping = False
        self.requests = {}
    def open_facebook(self, url):
        # Open the Facebook login page
        self.driver.get(url)
        self.open = True

    def close_browser(self):
        # Close the browser
        self.driver.quit()
        self.open = False

    def slow_type(self, element, text, delay=0.1):
        """Type text into an input element slowly."""
        for char in text:
            element.send_keys(char)
            time.sleep(delay)

    def login(self, username, password):
        if self.open:
            # Click on the "Decline optional cookies" button
            aria_label = "Decline optional cookies"
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@aria-label='{aria_label}']"))
            ).click()
            
            # Click on the "Close" button if it appears
            close_label = "Close"
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[@aria-label='{close_label}']"))
                ).click()
            except Exception as e:
                print("Close button not found or not clickable:", e)

            # Fill in the username
            username_field = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.NAME, "email"))
            )
            username_field.clear()  # Clear any pre-existing text
            self.slow_type(username_field, username)  # Use slow typing
            print("Email entered")
            
            # Fill in the password
            password_field = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.NAME, "pass"))
            )
            password_field.clear()  # Clear any pre-existing text
            self.slow_type(password_field, password)  # Use slow typing
            print("Password entered")
            
            # Click on the login button
            login_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Log in']"))
            )
            login_button.click()
            print("Login button pressed")


            self.scrape_instance()
    
    
    def scrape_instance(self):
        '''
        Scrapes posts and stores them as request objects in the set self.requests
        '''
        wait = WebDriverWait(self.driver, 5)  # Wait for up to 10 seconds
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Allow time for the page to load after scrolling

        try:
            

            # XPath
            xpath = #TODO having some trouble finding the right xpath

            # Use the wait to find elements
            elements = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, xpath)
            ))
            print(f"Found {len(elements)} elements.")
            
            for element in elements:
                link = element.get_attribute("href")  # Get the link URL
                if link:  # Only proceed if the link exists
                    # Open the link in a new tab
                    self.driver.execute_script(f"window.open('{link}', '_blank');")
                    time.sleep(2)  # Allow time for the new tab to load

                    # Switch to the new tab
                    self.driver.switch_to.window(self.driver.window_handles[-1])

                    # Scrape the desired information from the post

                    # Close the new tab
                    self.driver.close()

                    # Switch back to the original tab
                    self.driver.switch_to.window(self.driver.window_handles[0])

        except Exception as e:
            print(f"An error occurred: {e}")

        

# Usage example
if __name__ == "__main__":
    fb_login = FacebookLogin("/Users/seanlim/Camb /walraisian/chromedriver")
    fb_login.open_facebook("https://www.facebook.com/groups/1048169057102684/")
    fb_login.login("robersloane129@gmail.com", "xv4VfBS5T64;Mq8")
    input("Press Enter to close the browser...")
    fb_login.close_browser()
