from numpy import nan
from sentence_transformers import SentenceTransformer
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
# Load the model
my_vect_model = SentenceTransformer("paraphrase-MiniLM-L12-v2")
# Load JSON data
data = pd.read_json('./combined_dataset.json').copy()
data.shape
karar =set()
for i in data['instructor']:
    if i:
        karar.update(i)
len(karar)

filtered = data[data['organization'] == nan]

#len(data)
#data = data.dropna(subset=['organization'])
#len(data)
#data = data[data['organization'].apply(lambda x: isinstance(x, float) and len(x) == 0)]
#len(data)





# Function to encode reviews directly inside the nested structure
def encode_reviews(reviews):
    if isinstance(reviews, list):
        for review in reviews:
            review["encoded_comment"] = my_vect_model.encode(review["comment"]).tolist()
    return reviews

# Apply encoding to each course's reviews
data["reviews"] = data["reviews"].apply(encode_reviews)

# Encode other text columns like description and course-name
for col in ["description", "course_name"]:
    data[f"{col}_encoding"] = list(my_vect_model.encode(data[col].astype(str)))

# Save the modified data with nested encoded reviews
data.to_json("../data/encoded_data.json", orient="records", indent=4, force_ascii=False)
