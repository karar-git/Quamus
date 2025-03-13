from sentence_transformers import SentenceTransformer
import pandas as pd

# Load the model
my_vect_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load JSON data
data = pd.read_json('./combined_dataset.json').copy()

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

# Save the model
my_vect_model.save('my_vect_model')
#|%%--%%| <LrGpMwDgM8|eobttcfESU>
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
data_1 = pd.read_json('./encoded_data.json').copy()
data_1.iloc[1]
len(data_1.iloc[1]['reviews'][1]['encoded_comment'])
len(data_1.iloc[1]['description_encoding'])
#|%%--%%| <eobttcfESU|qHOLAsV6DK>





