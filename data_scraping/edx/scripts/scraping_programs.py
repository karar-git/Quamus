import requests
import json

# Base URL and headers
url = "https://igsyv1z1xi-dsn.algolia.net/1/indexes/*/queries"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "x-algolia-agent": "Algolia for JavaScript (5.0.0); Search (5.0.0); Browser; instantsearch.js (4.74.2); react (18.3.0-canary-14898b6a9-20240318); react-instantsearch (7.13.2); react-instantsearch-core (7.13.2); next.js (14.2.18); JS Helper (3.22.5)",
    "x-algolia-api-key": "6658746ce52e30dacfdd8ba5f8e8cf18",
    "x-algolia-application-id": "IGSYV1Z1XI",
}

# Function to create the payload for a specific page
def create_payload(page):
    return {
        "requests": [
            {
                "indexName": "product", 
                "params": f"clickAnalytics=true&facetFilters=%5B%5B%22product%3AProgram%22%5D%5D&page={page}&hitsPerPage=24"
            }
        ]
    }

# Fetch data from all pages
def fetch_data(start_page=0, end_page=5):
    all_results = []
    for page in range(start_page, end_page):
        payload = create_payload(page)
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [{}])[0].get("hits", [])
            all_results.extend(results)
            print(f"Fetched page {page} successfully.")
        else:
            print(f"Failed to fetch page {page}: {response.status_code}")
            break
    return all_results

# Save data to a file
def save_to_file(data, filename="courses.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

# Fetch and save data
if __name__ == "__main__":
    data = fetch_data(start_page=0, end_page=27)
    save_to_file(data, "programs.json")

