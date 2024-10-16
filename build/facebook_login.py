from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

class FacebookLogin:
    def __init__(self, chromedriver_path):
        # Set Chrome options to disable notifications
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")  # Disable notifications

        # Initialize the webdriver with options and open the browser
        self.service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)  
        self.open = False

        self.name_class = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f"
        self.post_text_class = "xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"
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
    
    
    def scrape_instance(self):
        '''
        Scrapes posts from a Facebook group and stores them in a dictionary
        '''
        # Wait for the page to load initial content
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main']"))
        )

        # Scroll to load more content (adjust as needed)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load

        # Initialize the dictionary to store scraped posts
        scraped_posts = {}

        # Find all post containers
        posts = self.driver.find_elements(By.CSS_SELECTOR, 'div.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z')

        for index, post in enumerate(posts):
            # Extract post information
            try:
                author_element = post.find_element(By.CSS_SELECTOR, f'a.{self.name_class}')
                author = author_element.text
            except NoSuchElementException:
                author = "Unknown Author"
            
            try:
                text_element = post.find_element(By.CSS_SELECTOR, f'div.{self.post_text_class}')
                post_text = text_element.text
            except NoSuchElementException:
                post_text = "No Text"

            # Store the extracted information in the dictionary
            scraped_posts[index] = {
                "author": author,
                "text": post_text
            }

        # Store the scraped posts in the instance variable
        self.scraped_posts = scraped_posts

        print(f"Scraping completed. {len(scraped_posts)} posts found.")


    # Usage example
if __name__ == "__main__":
    fb_login = FacebookLogin("/Users/seanlim/Camb /walraisian/chromedriver")
    fb_login.open_facebook("https://www.facebook.com/groups/1048169057102684/")
    fb_login.login("robersloane129@gmail.com", "xv4VfBS5T64;Mq8")
    fb_login.scrape_instance()
    print(fb_login.scraped_posts)
    input("Press Enter to close the browser...")
    fb_login.close_browser()
