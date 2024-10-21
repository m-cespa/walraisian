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

import requests_class
import local_data



class FacebookLogin:
    def __init__(self, chromedriver_path):
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

        # # Set class for comments
        # self.comment_class = "html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd"
    
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
        for i in range(10):
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

    def flush_screenshot_directory(self,output_dir="screenshots"):
        '''
        Flushes the screenshot directory for the next run
        Also flushes the bug testing csv file
        '''
        if os.path.exists(output_dir):
             # Remove all files in the directory
            for filename in os.listdir(output_dir):
                file_path = os.path.join(output_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Remove files
            print(f"Cleared directory: {output_dir}")
        else:
            print(f"Failed to find directory: {output_dir}")
        
        if os.path.exists("extracted_text.csv"):
            os.remove("extracted_text.csv")
            print("removed debugging csv file")
        else:
            print('No debugging file found')

    def _process_image_with_tesseract(self, image_path):
        """
        Process a single image file using Tesseract OCR and extract relevant information.
        :param image_path: Path to the image file.
        :return: A dictionary containing extracted information (username, time_line, content).
        """
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img,lang='eng')
        
        # save text to a csv file for debugging + testing
        csv_filename = "extracted_text.csv"
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([os.path.basename(image_path), text])

        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # Extract username (first non-empty line)
        username = lines[0] if lines else ""

        # Extract potential time line (second line, if it exists)
        time_line = lines[1] if len(lines) > 1 else ""

        # Extract content (everything after the second line)
        content = ' '.join(lines[2:]) if len(lines) > 2 else ""

        # Clean up content
        content = re.sub(r'\s+', ' ', content)  # Replace multiple spaces with single space
        content = content.strip()

        return {
            "username": username,
            "time_line": time_line,
            "content": content
        }

    def process_screenshots(self, folder_path="screenshots"):
        """
        Process all screenshot images in the specified folder using Tesseract OCR.
        :param folder_path: Path to the folder containing screenshot images.
        """
        if not os.path.exists(folder_path):
            print(f"Error: The folder '{folder_path}' does not exist.")
            return

        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))]

        if not image_files:
            print(f"No image files found in '{folder_path}'.")
            return

        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            print(f"Processing {image_file}...")
            try:
                info = self._process_image_with_tesseract(image_path)
                print(f"Username: {info['username']}")
                print(f"Time Line: {info['time_line']}")
                print(f"Content: {info['content']}")
            except Exception as e:
                print(f"Error processing {image_file}: {str(e)}")
            print("-" * 50)



if __name__ == "__main__":
    fb_login = FacebookLogin("/Users/seanlim/Camb /walraisian/chromedriver") # launch the web driver
    fb_login.open_facebook("https://www.facebook.com/groups/257070261826425/?sorting_setting=CHRONOLOGICAL") # open to the ticketbridge page sorted by chronological
    fb_login.take_screenshots_of_elements()
    fb_login.process_screenshots()


    input("Press Enter to close flush the directory...")
    fb_login.flush_screenshot_directory()
