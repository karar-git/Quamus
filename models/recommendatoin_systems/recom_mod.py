#ayooo Teeba. well, this is really bad system that it doesn't utilize a lot of features of the item and is just content based(means that it will not utilize the other user to predict better resulsts)
#and bigger problem, it is not personilized for the user. it will just see if the current prompt or message (just that one not the history, user interests, or what he had take)
#biggest problem
#i generated it with chatgpt
#but however, it is just a base one and could be change entirly, just a one so that I nevermind if we will can done on time for that part

# here is the main recommendation system
#import processing_text
from huggingface_hub.inference._generated.types import question_answering
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

course_data = pd.read_json('../various_preprocessing/combined_dataset.json')

course_embeddings = np.load('../data/encoded_data.npy')
course_embeddings.shape

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
course_embeddings = torch.tensor(course_embeddings).float().to(device)

# Load a SentenceTransformer model for encoding user queries
query_model = SentenceTransformer('paraphrase-MiniLM-L12-v2')
def get_course_recommendations(user_query, top_k=5, beta = 0.66):
    # Encode the user query into a 384-dim vector and move to the correct device
    query_embedding = query_model.encode(user_query, convert_to_tensor=True).to(device)
    print(query_embedding.shape)
    
    # Compute cosine similarities between the query and all course description embeddings
    cosine_scores = util.cos_sim(query_embedding, course_embeddings)[0]
    euc_sim=-(util.euclidean_sim(query_embedding, course_embeddings)[0])

    euc_sim = torch.exp(-euc_sim)
    total_sim = beta * cosine_scores + (1-beta )* euc_sim
    
    # Get the indices of top-k most similar courses
    top_results = torch.argsort(total_sim, descending=True)[:top_k]

    
    # Retrieve and return the corresponding courses using .iloc for DataFrame indexing
    recommendations = [course_data.iloc[idx] for idx in top_results.cpu().numpy()]
    return recommendations

# Example usage:
user_query = "ayoooo, i wanna learn NLP in practical way"
user_query='i wanna learn linear algebra rigorosly, in short courses, I don\' like long courses, just only small courses, i would love the course to be from deeplearning.ai'
recommended_courses = get_course_recommendations(user_query, top_k=5)
for course in recommended_courses:
    print(f"Course: {course['course_name']}, duration: {course['Duration']},Level: {course['level']}, Skills: {course['skills']}, provider : {course['provider']}, url : {course['url']}, type: {course['type']}, orginization: {course['organization']}")

