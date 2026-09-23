# Assignment 3: 

##This script downloads a CSV web log file from the internet and analyzes the site traffic to find image percentages and the top web browser.

### How the code works:

#1. Downloading the File: The script uses `argparse` to accept a `--url` link from the terminal, and then downloads the raw data using the `urllib.request` module.
#2. Reading the Data: It uses the `csv` module to loop through the file row by row, pulling out the file path, the date/time, and the user-agent (browser).
#3. Filtering with Regular Expressions: It uses the `re` module to search the text for specific patterns:
   ##- It looks for `.jpg`, `.gif`, and `.png` at the end of file paths to count image hits.
   ##- It searches the browser column for "Firefox", "Chrome", "Internet Explorer", or "Safari" to find the most popular browser.
#4. Sorting by Hour: It converts the date strings into real `datetime` objects to extract the specific hour of the day. It then tallies up the hits for each hour and sorts them from highest to lowest.** 

import argparse
import urllib.request
import csv
import re
import datetime

def download_data(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode


def process_data(file_content):
    total_hits = 0
    image_hits = 0

    browsers = {
        "Firefox": 0,
        "Chrome": 0,
        "Internet Explorer": 0,
        "Safari": 0
    }

    hours = {}
    for i in range(24):
        hours[i] = 0

    lines = file_content.splitlines()
    reader = csv.reader(lines)
    
    for row in reader:
        if not row or len(row) < 5:
            continue
            
        total_hits += 1
        
       
        file_path = row[0]
        datetime_str = row[1].strip() 
        user_agent = row[2]
        

        if re.search(r'\.(jpg|gif|png)$', file_path, re.IGNORECASE):
            image_hits += 1
            

        if re.search(r'Firefox', user_agent, re.IGNORECASE):
            browsers["Firefox"] += 1
        elif re.search(r'Chrome', user_agent, re.IGNORECASE):
            browsers["Chrome"] += 1
        elif re.search(r'Internet Explorer', user_agent, re.IGNORECASE):
            browsers["Internet Explorer"] += 1
        elif re.search(r'Safari', user_agent, re.IGNORECASE):
            browsers["Safari"] += 1
            
       
        try:
            dt_obj = datetime.datetime.strptime(datetime_str, "%m/%d/%Y %H:%M:%S")
            hours[dt_obj.hour] += 1
        except ValueError:
            pass 
            
    # Outputs Section
    
   
    if total_hits > 0:
        image_pct = (image_hits / total_hits) * 100
    else:
        image_pct = 0.0
    print(f"Image requests account for {image_pct:.1f}% of all requests")
    
    top_browser = ""
    max_count = -1
    for b in browsers:
        if browsers[b] > max_count:
            max_count = browsers[b]
            top_browser = b
    print(f"The most popular browser is {top_browser} with {max_count} hits.")
    

    print("\n--- Extra Credit ---")
    
    def get_hits(item):
        return item[1] 
        
    sorted_hours = sorted(hours.items(), key=get_hits, reverse=True)
    
    for hour, hits in sorted_hours:
        print(f"Hour {hour:02d} has {hits} hits")


def main(url):
    print(f"Running main with URL = {url}...\n")
    try:
        csvData = download_data(url)
        process_data(csvData)
    except Exception as e:
        print(f"An error occurred downloading the file: {e}")


def main(url):
    print(f"Running main with URL = {url}...")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    
