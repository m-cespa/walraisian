from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import datetime
import re



import requests_class
import local_data

class FacebookLogin:
    def __init__(self, chromedriver_path):
        # Set Chrome options to disable notifications
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")  # Disable notifications

        # change profile path for testing 
        profile_path = "/Users/seanlim/Library/Application Support/Google/Chrome/Profile 1"
        chrome_options.add_argument(f"user-data-dir={profile_path}")

        # Initialize the webdriver with options and open the browser
        self.service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)  
        self.open = False

        self.name_class = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f"
        self.post_text_class = "xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"
        self.url_class = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f"
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
        
        # Go to ticketbridge page
        self.driver.get("https://www.facebook.com/groups/257070261826425/")
        
        # Wait for the page to load initial content manually enter capchas 
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main']"))
        )

        # Scroll to load more content (adjust as needed)
        for i in range(5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new content to load

        # Get the page source after scrolling and waiting
        page_source = self.driver.page_source

        # Create a BeautifulSoup object
        soup = BeautifulSoup(page_source, 'html.parser')

        # Initialize the dictionary to store scraped posts for this scrape instance (resets every scrape)
        scraped_posts = {}

        # Find all post containers
        posts = soup.find_all('div', class_="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")

        for index, post in enumerate(posts):
            # Extract post information
            author_element = post.find('a', class_=self.name_class)
            text_element = post.find('div', class_=self.post_text_class)
            author_url_element = post.find('a',class_= self.url_class)
            

            # Extract text content, handling potential None values
            author = author_element.text if author_element else "reject"
            post_text = text_element.text if text_element else "reject"
            
            if author_url_element and 'href' in author_url_element.attrs:
                full_url = author_url_element['href']
                url_parts = full_url.split('/')
                user_id = next((part for part in url_parts if part.isdigit()), "reject")
            else:
                user_id = "No ID"

            # Store the extracted information in the dictionary
            scraped_posts[index] = {
                "author": author,
                "text": post_text.lower(),
                "user_id": user_id,
                "scraped_time" : datetime.datetime.now(datetime.timezone.utc).isoformat()
            }

        # Store the scraped posts in the instance 
        self.scraped_posts = scraped_posts

        print(f"Scraping completed. {len(scraped_posts)} posts found.")

    def parse_request(self,post):
        '''
        Parses the scraped post item in the dictionary and returns a TicketRequest object
        If cannot be parsed, returns None
        '''
        if post["user_id"] != "reject":
            userID = post["user_id"]  # set as facebook user page ID
        else:
            return None
        
        if "mash" or "frash" in post["text"]:
            club = "mash"
        elif "rev" or "wev" in post["text"]:
            club = "revs"
        elif "lola" or "kiki" in post["text"]:
            club = "kikis"
        elif "junction" in post["text"]:
            club = "junction"
        else:
            return None

        if "wtb" in post["text"]:
            buy_or_sell = "buy"
        elif "wts" in post["text"]:
            buy_or_sell = "sell"
        else:
            return None
        
        # use regex to detect quantities
        quantity_match = re.search(r'(\d+)x', post["text"])
        if quantity:
            quantity = int(quantity_match.group(1))  # convert _x to an int
        else:
            quantity = 1 # default 

        # use regex to find prices
        price_match  = re.search(r'([£$]\s*\d+(?:\.\d{1,2})?)', post["text"])  # captures anything after a $ or £
        if price_match:
            price = price_match.group(1)
        else:
            price = "market"

        timeID = post["scraped_time"] 

        ticket_request_obj = requests_class.TicketRequest(club,timeID,userID,buy_or_sell,quantity,price) # create a ticket_request obj 
        return ticket_request_obj
    

    def parse_cached_requests(self,local_data_instance):
        '''
        For each item in the scraped cache, parses it into a ticket_requests object, then calls the local_data.add() method which checks for duplicates before
        adding it into the local cache.

        Args:
        Local data instance 

        Returns:
        None
        Prints the number of posts sent to database successfully 
        '''
        for index, post in self.scraped_posts.items():
            ticket_request = self.parse_request(post)
            if ticket_request is not None:
                # call add method
                if local_data_instance.add_node(ticket_request): # this should add the node to the local data structure and return true if it is a duplicate
                    break # stop the loop if there is a duplicate
    # Usage example
if __name__ == "__main__":
    fb_login = FacebookLogin("/Users/seanlim/Camb /walraisian/chromedriver")
    fb_login.open_facebook("https://www.facebook.com/groups/257070261826425/?sorting_setting=CHRONOLOGICAL")

    #fb_login.login("limsean12345@gmail.com", "")

    fb_login.scrape_instance()

    print(fb_login.scraped_posts)

    input("Press Enter to close the browser...")
    fb_login.close_browser()
