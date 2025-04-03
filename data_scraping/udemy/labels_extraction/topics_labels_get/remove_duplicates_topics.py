import json

# Load JSON data from the file
with open('udemy_topics.json', 'r') as file:
    data = json.load(file)

# Convert the list to a set to remove duplicates
unique_data = list(set(data))

# Save the cleaned data to a new JSON file
with open('../cleaned_labels.json', 'w') as file:
    json.dump(unique_data, file, indent=4)

print("Duplicates removed and saved to 'cleaned_labels.json'.")

