#from selenium_stealth import stealth
#import json
#from selenium.webdriver.chrome.options import Options
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#import time
#
## Paths
#input_file = "cleaned_labels.json"  # Input JSON file containing topic URLs
#output_file = "labels_with_ids.json"  # Output JSON file to save extracted label IDs
#
## Setup Chrome options
#options = Options()
#options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.264 Safari/537.36")
#options.add_argument('--headless')  # Optional, to run in headless mode
#options.add_argument('--disable-gpu')  # Optional, for stability
#options.add_argument('--no-sandbox')  # Helps with some setups
#options.add_argument('window-size=1920x1080')  # Optional screen size
#options.add_argument('--disable-performance')  # Disable performance logs
#
## Setup WebDriver service
#driver = webdriver.Chrome(service=Service("/sbin/chromedriver"), options=options)
#stealth(driver,
#        languages=["en-US", "en"],
#        vendor="Google Inc.",
#        platform="Win32",
#        webgl_vendor="Intel Inc.",
#        renderer="Intel Iris OpenGL Engine",
#        fix_hairline=True,
#)
#
## Load topic URLs from labels.json
#with open(input_file, "r") as file:
#    topics = json.load(file)
#
## Prepare the output dictionary
#label_data = {}
#
#try:
#    for topic_url in topics:
#        print(f"Processing: {topic_url}")
#        try:
#            # Visit the topic URL
#            time.sleep(3)
#            driver.get(topic_url)
#            driver.implicitly_wait(10)  # Wait for the page to load
#
#            # Capture network logs
#            #logs = driver.get_log("performance")
#            logs = driver.get_log("browser")
#            if not logs:  # Check browser logs if performance logs are not present
#                logs = driver.get_log("browser")
#
#            print(logs)
#            for entry in logs:
#                log = entry["message"]
#                if "Network.responseReceived" in log and "application/json" in log:
#                    # Check for label_id in the response
#                    if '"label_id":' in log:
#                        label_id = log.split('"label_id":')[1].split(",")[0].strip()
#                        label_data[topic_url] = label_id
#                        print(f"Found Label ID {label_id} for {topic_url}")
#                        break  # Stop checking logs once label_id is found
#
#        except Exception as e:
#            print(f"Error processing {topic_url}: {e}")
#            continue
#
#        # Save progress periodically
#        with open(output_file, "w") as out_file:
#            json.dump(label_data, out_file, indent=4)
#            print("Progress saved!")
#
#finally:
#    # Quit the WebDriver
#    driver.quit()
#
## Final save
#with open(output_file, "w") as out_file:
#    json.dump(label_data, out_file, indent=4)
#print("All labels have been processed and saved.")
