import requests
import json

# URL for the Algolia API request
url = "https://igsyv1z1xi-dsn.algolia.net/1/indexes/*/queries"

# Headers
headers = {
    #"User-Agent": ensure to put a user agent,
    "Content-Type": "application/json",
    "X-Algolia-API-Key": "6658746ce52e30dacfdd8ba5f8e8cf18",
    "X-Algolia-Application-Id": "IGSYV1Z1XI",
}

# Payload
payload = {
    "requests": [
        {
            "clickAnalytics": True,
            "facetFilters": [
                "product:Executive Education"
            ],
            "facets": [
                "availability",
                "language",
                "learning_type",
                "level",
                "partner",
                "product",
                "program_type",
                "skills.skill",
                "subject"
            ],
            "filters": (
                '(product:"Course" OR product:"Boot Camp" OR product:"Program" '
                'OR product:"Executive Education" OR product:"2U Degree") '
                'AND NOT blocked_in:"IQ" AND (allowed_in:"null" OR allowed_in:"IQ")'
            ),
            "highlightPostTag": "__/ais-highlight__",
            "highlightPreTag": "__ais-highlight__",
            "hitsPerPage": 24,
            "indexName": "product",
            "maxValuesPerFacet": 100,
            "page": 0
        }
    ]
}

def fetch_hits(page: int):
    """Fetch only the hits from the Algolia API for a specific page."""
    # Update the page number in the payload
    payload["requests"][0]["page"] = page
    
    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]["hits"]
        else:
            print(f"No hits found on page {page}.")
            return []
    else:
        print(f"Error: {response.status_code}")
        return []

def main():
    all_hits = []
    for page in range(100):  # Adjust range according to how many pages you want to retrieve
        print(f"Fetching hits from page {page}...")
        hits = fetch_hits(page)
        if hits:
            all_hits.extend(hits)
        else:
            break
    
    # Save all hits to a JSON file
    with open("edx_executive_education.json", "w") as file:
        json.dump(all_hits, file, indent=4)
    print("Hits saved successfully!")

if __name__ == "__main__":
    main()
