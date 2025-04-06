#ayooo teeba. well, this is really bad system that it doesn't utilize a lot of features of the item and is just content based(means that it will not utilize the other user to predict better resulsts)
#and bigger problem, it is not personilized for the user. it will just see if the current prompt or message (just that one not the history, user interests, or what he had take)
#biggest problem
#i generated it with chatgpt
#but however, it is just a base one and could be change entirly, just a one so that i nevermind if we will can done on time for that part

# here is the main recommendation system
#import processing_text

import numpy as np
import tensorflow as tf
import pandas as pd
from sentence_transformers import SentenceTransformer

class PersonalityVector:
    def __init__(self, dim=384):
        self.vector = tf.Variable(tf.zeros(dim), dtype=tf.float32)
        self.decay = 0.85  # Base decay rate
    
    def update(self, course_embedding, weight=1.0):
        updated_vector = self.decay * self.vector + weight * (1 - self.decay) * course_embedding
        normalized_vector = updated_vector / tf.norm(updated_vector)
        self.vector.assign(normalized_vector)


def cos_sim(a, b):
    a = tf.nn.l2_normalize(a, axis=-1)
    b = tf.nn.l2_normalize(b, axis=-1)
    return tf.linalg.matvec(b, a, transpose_a=False)  # (num_courses,)
def cos_sim_vec(a,b):
    a = tf.nn.l2_normalize(a, axis=-1)
    b = tf.nn.l2_normalize(b, axis=-1)
    return a @ b.T
def cos_sim_mat(a,b):
    a = tf.nn.l2_normalize(a, axis=-1)
    b = tf.nn.l2_normalize(b, axis=-1)
    return a @ b.T


def get_score(query_embedding, course_embedding, new_personality):
    query_sim = cos_sim(query_embedding, course_embeddings)
    personality_sim = cos_sim(new_personality, course_embeddings)
    hybrid_scores = 0.8 * query_sim + 0.2 * personality_sim
    return hybrid_scores
    

    
def recommend(user_query, top=5, top_k=40):
    # Encode query
    query_embedding = query_model.encode(user_query)
    query_embedding = tf.convert_to_tensor(query_embedding, dtype=tf.float32)
    
    # Cosine similarity function
    # Get similarities
    query_sim = cos_sim(query_embedding, course_embeddings)
    
    # Get top candidates
    topk = tf.math.top_k(query_sim, top_k).indices
    
    if nu_of_interaction > 5:
        personality_sim = cos_sim(personality_vector, tf.gather(course_embeddings, topk))
        hybrid_scores = 0.8 * tf.gather(query_sim, topk) + 0.2 * personality_sim
        sorted_indices = tf.argsort(hybrid_scores, direction='DESCENDING')
        return tf.gather(topk, sorted_indices)[:top]
    
    sorted_indices = tf.argsort(tf.gather(query_sim, topk), direction='DESCENDING')
    return tf.gather(topk, sorted_indices)[:top]

def main():
    course_data = pd.read_json('../various_preprocessing/combined_dataset.json')

    course_embeddings = np.load('../data/encoded_data.npy')
    course_embeddings = tf.convert_to_tensor(course_embeddings, dtype= tf.float32)
    #course_embeddings.shape

    #course_embeddings = torch.tensor(course_embeddings).float().to(device)

    # load a sentencetransformer model for encoding user queries
    query_model = SentenceTransformer('paraphrase-minilm-l12-v2')

    personality_vector = tf.Variable(tf.zeros(384, dtype=tf.float32))
    nu_of_interaction = 0
    # example usage:
    user_query = "ayoooo, i wanna learn nlp in practical way"
    user_query='i wanna learn linear algebra rigorosly'
    recommended_courses = recommend(user_query, top=5)
    for course in recommended_courses:
        course  = course.numpy()
        course_idx = course.item()  
        course = course_data.iloc[course_idx]
        print(f"course: {course['course_name']}, duration: {course['Duration']},level: {course['level']}, skills: {course['skills']}, provider : {course['provider']}, url : {course['url']}, type: {course['type']}, orginization: {course['organization']}")

if __name__ == "__main__":
    main()

