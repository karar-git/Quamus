import json
from tqdm import tqdm
from urllib.parse import parse_qs, urlparse
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
with open('cleaned_labels.json', 'r') as urls_file:
    urls = json.load(urls_file)

with open('labels_with_ids.json', 'r') as labels_file:
    label_ids = json.load(labels_file)

# Extract URLs without labels
urls_without_labels = [url for url in urls if url not in label_ids]
print("the lenght of url without labels", len(urls_without_labels))

# Paths
#input_file = "cleaned_labels.json"  # Input JSON file containing topic URLs
output_file = "second_try.json"  # Output JSON file to save extracted label IDs
#with open(input_file, "r") as file:
#   topics = json.load(file)
data_without_labels = []
label_data = {}
for _ in tqdm(range(20), desc="Outer Loop Progress"):
    print("the lenght of url without labels", len(urls_without_labels))
    for topic_url in urls_without_labels:
        # Setup Chrome options
        options = Options()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--disable-gpu')  # Optional, for stability
        options.add_argument('--no-sandbox')  # Helps with some setups
        options.add_argument('window-size=1920x1080')  # Optional screen size
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.264 Safari/537.36")
        #options.add_argument("--disable-application-cache")
        #options.add_argument("--disable-cache")
        #options.add_argument("--disable-dev-shm-usage")  # Helps with stability in some setups
        
        
        # Enable performance logging
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        
        # Setup WebDriver
        driver = webdriver.Chrome(service=Service("/sbin/chromedriver"), options=options)
        
        # Load topic URLs from input JSON file
        
        # Prepare the output dictionary
        
        try:
            print(f"Processing: {topic_url}")
            found = False
            # Visit the topic URL
            driver.get(topic_url)
            #driver.execute_script("window.location.reload();")
            #driver.delete_all_cookies()
            #driver.execute_script("window.localStorage.clear();")
            #driver.execute_script("window.sessionStorage.clear();")
        
            driver.implicitly_wait(10)  # Wait for the page to load
            time.sleep(5)
        
            # Capture performance logs
            logs = driver.get_log("performance")
        
            for entry in logs:
                log = json.loads(entry["message"])["message"]
                
                # Filter only 'Network.responseReceived' entries for GET requests
                if log["method"] == "Network.responseReceived":
                    response = log["params"]["response"]
                    if response["mimeType"] == "application/json" and response["status"] == 200:
                        url = response.get("url", "")
                        
                        # Extract label_id from headers
                        if "label_id" in url:
                            query_params = parse_qs(urlparse(url).query)
                            label_id = query_params.get("label_id", [None])[0]  # Extract label_id
                            if label_id:
                                print("label_id found:", label_id)
                                label_data[topic_url] = label_id
                                print(f"Found Label ID {label_id} for {topic_url}")
                                #label_id = None
                                found = True
                                break  # Stop once label_id is found
            if not found:
                data_without_labels.append(topic_url)
            driver.quit()
        
        except Exception as e:
            print(f"Error processing {topic_url}: {e}")
            data_without_labels.append(topic_url)
            driver.quit()
            continue
    urls_without_labels = data_without_labels   
    data_without_labels = []
        # Save progress periodically
    with open(output_file, "w") as out_file:
        json.dump(label_data, out_file, indent=4)
        print("Progress saved!")


# Final save
with open(output_file, "w") as out_file:
    json.dump(label_data, out_file, indent=4)
print("All labels have been processed and saved.")
print("urls_without_label: ", urls_without_labels)

