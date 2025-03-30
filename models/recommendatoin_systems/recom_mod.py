#ayooo Teeba. well, this is really bad system that it doesn't utilize a lot of features of the item and is just content based(means that it will not utilize the other user to predict better resulsts)
#and bigger problem, it is not personilized for the user. it will just see if the current prompt or message (just that one not the history, user interests, or what he had take)
#biggest problem
#i generated it with chatgpt
#but however, it is just a base one and could be change entirly, just a one so that I nevermind if we will can done on time for that part

# here is the main recommendation system
#import processing_text

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

class PersonalityVector:
    def __init__(self, dim=384):
        self.vector = torch.zeros(dim)
        self.decay = 0.9  # Base decay rate
    
    def update(self, course_embedding, weight=1.0):
        self.vector = self.decay * self.vector + weight * (1 - self.decay) * course_embedding
        self.vector /= torch.norm(self.vector)  # L2 normalize

course_data = pd.read_json('../various_preprocessing/combined_dataset.json')

course_embeddings = np.load('../data/encoded_data.npy')
course_embeddings.shape

device = torch.device("cpu")#"cuda" if torch.cuda.is_available() else "cpu")
course_embeddings = torch.tensor(course_embeddings).float().to(device)

# Load a SentenceTransformer model for encoding user queries
query_model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

personality_vector = torch.zeros(384, device = 'cpu')

nu_of_interaction = 0

def recommend(user_query, top = 5,top_k=40, beta = 0.33):
    
    query_embedding = query_model.encode(user_query, convert_to_tensor=True).to(device)
    def simi(query_embedding, course_embedding):
        query_embedding = query_embedding.to(personality_vector.device)
        course_embedding = course_embedding.to(personality_vector.device)
        return util.cos_sim(query_embedding, course_embedding)[0] * beta + (1-beta) *( util.euclidean_sim(query_embedding,course_embedding)[0])

    query_sim = simi(query_embedding, course_embeddings)
    top40 = torch.topk(query_sim, top_k).indices
    if nu_of_interaction >5:
        personality_sim = simi(personality_vector , course_embeddings[top40])
        hybrid_scores = 0.6 * query_sim[top40] + 0.3 * personality_sim
        return top40[torch.argsort(hybrid_scores, descending=True)][:top]
    return top40[torch.argsort(query_sim[top40], descending=True)][:top]

# Example usage:
user_query = "ayoooo, i wanna learn NLP in practical way"
user_query='i wanna learn linear algebra rigorosly'
recommended_courses = recommend(user_query, top=5)
for course in recommended_courses:
    course_idx = course.item()  
    course = course_data.iloc[course_idx]
    print(f"Course: {course['course_name']}, duration: {course['Duration']},Level: {course['level']}, Skills: {course['skills']}, provider : {course['provider']}, url : {course['url']}, type: {course['type']}, orginization: {course['organization']}")

