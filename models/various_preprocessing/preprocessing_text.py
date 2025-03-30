#from sentence_transformers import SentenceTransformer
#import pandas as pd
#
## Load the model
#my_vect_model = SentenceTransformer("all-MiniLM-L6-v2")
#
## Load JSON data
#data = pd.read_json('./combined_dataset.json').copy()
#
## Function to encode reviews directly inside the nested structure
#def encode_reviews(reviews):
#    if isinstance(reviews, list):
#        for review in reviews:
#            review["encoded_comment"] = my_vect_model.encode(review["comment"]).tolist()
#    return reviews
#
## Apply encoding to each course's reviews
#data["reviews"] = data["reviews"].apply(encode_reviews)
#
## Encode other text columns like description and course-name
#for col in ["description", "course_name"]:
#    data[f"{col}_encoding"] = list(my_vect_model.encode(data[col].astype(str)))
#
## Save the modified data with nested encoded reviews
#data.to_json("../data/encoded_data.json", orient="records", indent=4, force_ascii=False)
#
## Save the model
##my_vect_model.save('my_vect_model')
#|%%--%%| <LrGpMwDgM8|eobttcfESU>
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
data_1 = pd.read_json('./encoded_data.json').copy()
data_1.iloc[1]
len(data_1.iloc[1]['reviews'][1]['encoded_comment'])
len(data_1.iloc[1]['description_encoding'])
#|%%--%%| <eobttcfESU|qHOLAsV6DK>

from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

# Load the model
my_vect_model = SentenceTransformer("paraphrase-MiniLM-L12-v2")

# Load JSON data
data = pd.read_json('./combined_dataset.json').copy()

# Function to handle NaN values
def handle_nan(value, default_value="Not available"):
    # If the value is a list or array, check if it's empty
    if isinstance(value, (list, np.ndarray)):
        if not value:  # if the list is empty
            return default_value
        return ", ".join([str(v) for v in value])  # join list elements into a string
    # If the value is NaN or None, return default_value
    if pd.isna(value):
        return default_value
# Initialize an empty list to store the final concatenated strings
final_texts = []

# Iterate over each row in the DataFrame
for _, row in data.iterrows():
    text_parts = []

    # Concatenate course name, organization, skills, description, and top comments
    text_parts.append(f"course_name: {handle_nan(row['course_name'])}")
    text_parts.append(f"organization: {', '.join(row['organization']) if isinstance(row['organization'], list) else handle_nan(row['organization'])}")
    text_parts.append(f"instructor: {handle_nan(row['instructor'])}")
    text_parts.append(f"course or project(project will likely be practical): {handle_nan(row['type'])}")

    rating_default = "No rating" if row['has_rating'] == 1 else "Not available"
    num_reviews_default = 0 if row['has_rating'] == 1 else "Not available"
    text_parts.append(f"rating: {handle_nan(row['rating'], default_value=rating_default)}")
    text_parts.append(f"num_reviews: {handle_nan(row['nu_reviews'], default_value=num_reviews_default)}")

    text_parts.append(f"description: {handle_nan(row['description'])}")
    text_parts.append(f"level: {handle_nan(row['level'])}")
    text_parts.append(f"Duration: {handle_nan(row['Duration'])} hourse")

    # Add skills as a string
    text_parts.append(f"skills: {', '.join(row['skills']) if isinstance(row['skills'], list) else handle_nan(row['skills'])}")
    
    # Get top 3 comments (if any)
    top_comments = "No comments available"
    if isinstance(row['reviews'], list) and row['reviews']:
        top_comments = "the most 3 upvoted comments: " + " | ".join([r['comment'] for r in row['reviews'][:3]])

    text_parts.append(top_comments)

    text_parts.append(f"total_video: {handle_nan(row['total_video'])}")
    text_parts.append(f"total_assignment: {handle_nan(row['total_assignment'])}")
    text_parts.append(f"total_reading: {handle_nan(row['total_reading'])}")
    text_parts.append(f"total_discussion: {handle_nan(row['total_discussion'])}")
    text_parts.append(f"total_quiz: {handle_nan(row['total_quiz'])}")
    text_parts.append(f"total_peer: {handle_nan(row['total_peer'])}")
    text_parts.append(f"total_teammate: {handle_nan(row['total_teammate'])}")
    text_parts.append(f"total_plugin: {handle_nan(row['total_plugin'])}")
    text_parts.append(f"total_ungraded: {handle_nan(row['total_ungraded'])}")

    final_texts.append(" | ".join(text_parts))

encoded_final_ = my_vect_model.encode(final_texts)

np.save("../data/encoded_data.npy", encoded_final_)
print("Embeddings have been successfully saved!")
