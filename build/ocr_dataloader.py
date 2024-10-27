# class for loading data into a local_data
# scrolls facebook pages in batches
# OCR generates batch of request objects cross-checked against a memo
import os
from requests_class import TicketRequest
from typing import List
from facebook_scraper_using_cv import FacebookLogin
import datetime
from datetime import timedelta
import re
from collections import deque
from PIL import Image
import csv
import pytesseract

class OCR_Loader:
    def __init__(self, local_dir: str):
        self.seen = deque()

        base_dir = os.path.dirname(__file__)
        dir_path = os.path.join(base_dir, local_dir)
        os.makedirs(dir_path, exist_ok=True)
        self.dir_path = dir_path

        # NEEDS TO BE MAINTAINED
        self.club_map = {
            id(r".*(k|sn)iki(s.*)?$"): 'kikis',
            id(r".*\b(w|r|rev|revolu)?evs\b.*$"): 'revs',
            id(r".*\b(s?(m|fr)?ash)\b.*$"): 'mash',
            id(r".*\b(s?lolas?|lola)\b.*$"): 'kikis'
        }
    
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
        content = content.strip().lower()

        return {
            "username": username,
            "time_line": time_line,
            "content": content
        }
    
    def check_if_request(self, requestID: str) -> bool:
        if not self.seen:
            return True
        
        if requestID in self.seen:
            return False
        
        if len(self.seen) < 5:
            self.seen.appendleft(requestID)
            return True
        
        self.seen.pop()
        self.seen.appendleft(requestID)

        return True

    def process_screenshots(self) -> List[TicketRequest]:
        """
        Process all screenshot images in the specified folder using Tesseract OCR.
        Return list of TicketRequest objects which have been pre-filtered.
        """
        active_requests = []

        if not os.path.exists(self.dir_path):
            print(f"Error: The folder '{self.dir_path}' does not exist.")
            return

        image_files = [f for f in os.listdir(self.dir_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not image_files:
            print(f"No image files found in '{self.dir_path}'.")
            return

        current_time = datetime.now()
        for image_file in image_files:
            image_path = os.path.join(self.dir_path, image_file)
            print(f"Processing {image_file}...")
            try:
                info = self._process_image_with_tesseract(image_path)

                print(f"Username: {info['username']}")
                print(f"Time Line: {info['time_line']}")
                print(f"Content: {info['content']}")

                # parse data if invalid skip it
                if info["username"] and info["time_line"] and info["content"]:
                    userID = info['username']

                    # Catch clubID
                    for regex_id, club_name in self.club_map.items():
                        regex = re.compile(regex_id)
                        if regex.search(info["content"]):
                            clubID = club_name

                    # Catch buying/selling
                    for word in info["content"].split():
                        if word in set('wtb', 'buying', 'buy', 'buys'):
                            buyID = True
                        elif word in set('wts', 'selling', 'sell', 'sells'):
                            buyID = False
                    
                    # Regex pattern for matching time
                    pattern = r'(?P<days>\d+)\s*days\s*ago|(?:a\s*day\s*ago|aday\s*ago)|(?P<hours>\d+)\s*hours\s*ago|(?P<minutes>\d+)\s*minutes\s*ago|(?P<minutesShort>\d+)m\s*-\s*®|(?:about\s*an\s*hour\s*ago)'
                    
                    # Search for time patterns
                    time_match = re.search(pattern, info['time_line'])
                    
                    if time_match:
                        # Initialize a timedelta object
                        time_delta = timedelta()

                        # Calculate the time difference based on matched groups
                        if time_match.group("days"):
                            days = int(time_match.group("days"))
                            time_delta += timedelta(days=days)
                        elif 'aday' in info['time_line']:
                            time_delta += timedelta(days=1)  # Treat "aday" as 1 day

                        if time_match.group("hours"):
                            hours = int(time_match.group("hours"))
                            time_delta += timedelta(hours=hours)

                        if time_match.group("minutes"):
                            minutes = int(time_match.group("minutes"))
                            time_delta += timedelta(minutes=minutes)
                        elif time_match.group("minutesShort"):
                            minutes_short = int(time_match.group("minutesShort"))
                            time_delta += timedelta(minutes=minutes_short)

                        # Handle "about an hour ago"
                        if 'about an hour ago' in info['time_line']:
                            time_delta += timedelta(hours=1)

                        # Calculate the post time by subtracting the time delta from current time
                        post_time = current_time - time_delta

                        timeID = post_time.strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Display the post time in a readable format
                        print(f"User: {userID}, Posted at: {post_time.strftime('%Y-%m-%d %H:%M:%S')}, Content: {info['content']}")
                    else:
                        continue

                    # create unique requestID 
                    requestID = userID.replace(" ", "") + clubID + timeID
                    
                    # check if requestID is in the set
                    if self.check_if_request(requestID):
                    
                        # use regex to detect quantities
                        quantity_match = re.search(r'(\d+)x', info["content"])
                        if quantity:
                            quantity = int(quantity_match.group(1))  # convert _x to an int
                        else:
                            quantity = 1 # default 

                        # use regex to find prices
                        price_match  = re.search(r'([£$]\s*\d+(?:\.\d{1,2})?)', info["content"])  # captures anything after a $ or £
                        if price_match:
                            price = price_match.group(1)
                        else:
                            price = "market"

                        # create request object
                        ticket_request = TicketRequest(
                            club = clubID,
                            buy_or_sell= buyID,
                            timeID = timeID,
                            userID = userID,
                            ticket_quantity = quantity,
                            price = price,
                            requestID = requestID
                        )

                        active_requests.append(ticket_request)
                else:
                    continue

            except Exception as e:
                print(f"Error processing {image_file}: {str(e)}")
            print("-" * 50)

        self.flush_screenshot_directory()

        return active_requests
    
    def flush_screenshot_directory(self) -> None:
        '''
        Flushes the screenshot directory for the next run
        Also flushes the bug testing csv file
        '''
        if os.path.exists(self.dir_path):
             # Remove all files in the directory
            for filename in os.listdir(self.dir_path):
                file_path = os.path.join(self.dir_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Remove files
            print(f"Cleared directory: {self.dir_path}")
        else:
            print(f"Failed to find directory: {self.dir_path}")
        
        if os.path.exists("extracted_text.csv"):
            os.remove("extracted_text.csv")
            print("removed debugging csv file")
        else:
            print('No debugging file found')
                
