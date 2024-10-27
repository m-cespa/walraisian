from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import cv2
import numpy as np
import time
import re
import os 
import pytesseract
from PIL import Image
import csv
import random
from datetime import datetime,timedelta
import requests_class
import local_data



class FacebookLogin:
    def __init__(self, chromedriver_path,stored_scraped_post_ids=set()):
        # Set Chrome options to disable notifications
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")  # Disable notifications
        chrome_options.add_argument("--start-maximized")

        # change profile path for testing 
        profile_path = "/Users/seanlim/Library/Application Support/Google/Chrome/Profile 1"
        chrome_options.add_argument(f"user-data-dir={profile_path}")
        

        # Initialize the webdriver with options and open the browser
        self.service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)  
        self.open = False

        # Set post class for screenshots
        self.post_class = "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"

        # Initialise seen set 
        self.current_set = stored_scraped_post_ids

    def open_facebook(self, url):
        # Open the Facebook login page
        self.driver.get(url)
        self.open = True

        # Zoom in to increase picture resolution 
        self.driver.execute_script("document.body.style.zoom='100%'")
        # Remove the annoying banner elements
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Scroll back to top slowly to get past bot detection
        for i in range(5):
            self.driver.execute_script(f"window.scrollTo(0, {random.randint(-100,-10)} );")
        

        # Locate the banner elements using XPath
        top_banner_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]')
        bottom_banner_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[3]')

        # Execute JavaScript to remove the element from the DOM
        self.driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, top_banner_element)
        self.driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, bottom_banner_element)
        
        # Scroll to Load Posts
        for i in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new content to load
            self.driver.execute_script("window.scrollTo(0, -100);")

    def take_screenshots_of_elements(self, output_dir="screenshots"):
        """
        This function iterates through all elements with the given class name and takes a screenshot of each.
        :param class_name: The class name of the elements to capture screenshots from.
        :param output_dir: Directory where the screenshots will be saved.
        """
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Find all elements with the specified class name
        elements = self.driver.find_elements(By.CSS_SELECTOR, f"div.{self.post_class.replace(' ', '.')}")

        # Iterate through each element and take a screenshot
        for index, element in enumerate(elements):
            if index == 0:
                continue  # Skip the first element (Garbage always)
            
            screenshot_filename = os.path.join(output_dir, f"element_{index}.png")
            
            try:
                element.screenshot(screenshot_filename)
                print(f"Screenshot saved: {screenshot_filename}")

                # Open the image using Pillow
                image = Image.open(screenshot_filename)

                # Crop the image
                cropped_image = image.crop((0, 0, image.width, 140))

                # Convert the cropped image to grayscale 
                img_cv = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2GRAY)

                # Define the coordinates of the profile picture area
                x_start, y_start, width, height = 0, 0, 63, 63  

                # Fill the area with white 
                img_cv[y_start:y_start+height, x_start:x_start+width] = 255

                # _, thresholded_img = cv2.threshold(img_cv, 210, 255, cv2.THRESH_BINARY)

                final_image = Image.fromarray(img_cv)
                resized_image = final_image.resize(
                    (int(final_image.width * 1.5), int(final_image.height * 1.5)),
                    Image.LANCZOS  
                )

                resized_image.save(screenshot_filename)
                print(f"Resized image saved as original: {screenshot_filename}")

            except Exception as e:
                print(f"Failed to take screenshot for element {index}: {e}")
        
# if __name__ == "__main__":
#     fb_login = FacebookLogin("/Users/seanlim/Camb /walraisian/chromedriver") # launch the web driver
#     fb_login.open_facebook("https://www.facebook.com/groups/257070261826425/?sorting_setting=CHRONOLOGICAL") # open to the ticketbridge page sorted by chronological
#     fb_login.take_screenshots_of_elements()
#     fb_login.process_screenshots()


#     input("Press Enter to close flush the directory...")
#     fb_login.flush_screenshot_directory()
