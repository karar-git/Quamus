import requests
import json

# Base API URL
base_api_url = "https://www.udemy.com/api-2.0/course-subcategories/{}/labels/"
base_url = "https://www.udemy.com"

# List to hold all topics
all_topics = []

for i in range(0, 1001):
    url = base_api_url.format(i)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        results = data['results']
        
        for item in results:
            topic_name = item['topic_channel_url']
            topic_url = base_url + topic_name
            all_topics.append(topic_url)
    else:
        print(f"Failed to fetch data for ID: {i}")

# Save to JSON file
with open('udemy_topics.json', 'w') as f:
    json.dump(all_topics, f, indent=4)

print("All topics have been saved to 'udemy_topics.json'.")

