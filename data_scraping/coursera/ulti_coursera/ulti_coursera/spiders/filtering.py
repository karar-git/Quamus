import json
with open("output.json", "r") as f:
    data= json.load(f)
seen_urls = set()
filtered_data = []

for entry in data:
    if entry["url"] not in seen_urls:
        entry.pop("course_url", None)  # Remove 'course_url' field
        filtered_data.append(entry)
        seen_urls.add(entry["url"])

# Print or save the filtered data
with open("output_final.json", "w") as f:
    json.dump(filtered_data, f, indent=4, ensure_ascii=False)
print(len(filtered_data))
