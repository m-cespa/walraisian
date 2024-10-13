from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class FacebookLogin:
    def __init__(self, chromedriver_path):
        # Set Chrome options to disable notifications
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")  # Disable notifications

        # Initialize the webdriver with options and open the browser
        self.service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)  
        self.open = False

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
    
    def start_scrape(self, time_interval):
        '''
        Initialises the scraping of the facebook group, updates the database of request objects, checking for any new posts and adding them to the database
        it should also update the market buy/sell price and update any transactions that have been made every time step

        args:
        time_interval(bool) : sets the time interval between scrapes 
        '''
        if self.open: 
            NotImplementedError
    def stop_scrape(self):
        '''
        Stops the scraping of the group
        '''
        NotImplementedError
        
# Usage example
if __name__ == "__main__":
    fb_login = FacebookLogin("/Users/seanlim/Walraisian/apps/backend/scripts/chromedriver")
    fb_login.open_facebook("https://www.facebook.com/groups/1048169057102684/")
    fb_login.login("robersloane129@gmail.com", "xv4VfBS5T64;Mq8")
    input("Press Enter to close the browser...")
    fb_login.close_browser()
