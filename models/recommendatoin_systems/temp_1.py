
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

class personalityvector:
    def __init__(self, dim=384):
        self.vector = np.zeros(dim)
        self.decay = 0.85  # base decay rate
    
    def update(self, course_embedding, weight=1.0):
        self.vector = self.decay * self.vector + (1 - self.decay) * course_embedding
        self.vector = norm(self.vector)  # l2 normalize


def simi(query_embedding, course_embedding):
    query_embedding = tf.expand_dims(query_embedding, axis=0)
    query_embedding = tf.math.l2_normalize(query_embedding, axis = -1)
    course_embedding = tf.math.l2_normalize(course_embedding, axis = -1)
    return tf.linalg.matmul(query_embedding, course_embedding, transpose_b =True )

def get_score(query_embedding, course_embedding, old_personality, last_liked_item):
    query_sim = simi(query_embedding, course_embeddings)
    new_personality = 0.85 * old_personality+ 0.15 * last_liked_item
    personality_sim = simi(new_personality, course_embeddings)
    hybrid_scores = 0.8 * query_sim + 0.2 * personality_sim
    return hybrid_scores
    

    
def recommend(user_query, top = 5,top_k=40):
    
    query_embedding = query_model.encode(user_query)
    query_embedding = tf.convert_to_tensor(query_embedding, dtype = tf.float32)
    query_sim = simi(query_embedding, course_embeddings)
    topk = tf.argsort(query_sim, direction='DESCENDING')[:top_k]


    if nu_of_interaction > 5:
        # Use personality vector
        personality_sim = cosine_sim(personality_vector[None, :], tf.gather(course_embeddings, topk))[0]
        hybrid_scores = 0.8 * tf.gather(query_sim, topk) + 0.2 * personality_sim
        sorted_indices = tf.argsort(hybrid_scores, direction='DESCENDING')[:top]
        return tf.gather(topk, sorted_indices)



    sorted_indices = tf.argsort(tf.gather(query_sim, topk), direction='DESCENDING')[:top]
    return tf.gather(topk, sorted_indices)

def main():
    course_data = pd.read_json('../various_preprocessing/combined_dataset.json')

    course_embeddings = np.load('../data/encoded_data.npy')
    course_embeddings = tf.convert_to_tensor(course_embeddings, dtype= tf.float32)
    course_embeddings.shape

    #course_embeddings = torch.tensor(course_embeddings).float().to(device)

    # load a sentencetransformer model for encoding user queries
    query_model = SentenceTransformer('paraphrase-minilm-l12-v2')

    personality_vector = tf.zeros(384)

    nu_of_interaction = 0


    # example usage:
    user_query = "ayoooo, i wanna learn nlp in practical way"
    user_query='i wanna learn linear algebra rigorosly'
    recommended_courses = recommend(user_query, top=5)
    for course in recommended_courses:
        course_idx = course.item()  
        course = course_data.iloc[course_idx]
        print(f"course: {course['course_name']}, duration: {course['Duration']},level: {course['level']}, skills: {course['skills']}, provider : {course['provider']}, url : {course['url']}, type: {course['type']}, orginization: {course['organization']}")

if __name__ == "__main__":
    main()














import numpy as np
import pandas as pd
import tensorflow as tf
from sentence_transformers import SentenceTransformer

class PersonalityVector:
    def __init__(self, dim=384):
        self.vector = tf.Variable(tf.zeros(dim), dtype=tf.float32)
        self.decay = 0.9  # Base decay rate
    
    def update(self, course_embedding, weight=1.0):
        updated_vector = self.decay * self.vector + weight * (1 - self.decay) * course_embedding
        normalized_vector = updated_vector / tf.norm(updated_vector)
        self.vector.assign(normalized_vector)

# Load data
course_data = pd.read_json('../various_preprocessing/combined_dataset.json')
course_embeddings = tf.constant(np.load('../data/encoded_data.npy'), dtype=tf.float32)

# Load model
query_model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

# Initialize personality vector
personality_vector = tf.Variable(tf.zeros(384, dtype=tf.float32))
nu_of_interaction = 0

def recommend(user_query, top=5, top_k=40):
    # Encode query
    query_embedding = query_model.encode(user_query)
    query_embedding = tf.convert_to_tensor(query_embedding, dtype=tf.float32)
    
    # Cosine similarity function
    def cos_sim(a, b):
        a = tf.nn.l2_normalize(a, axis=-1)
        b = tf.nn.l2_normalize(b, axis=-1)
        return tf.linalg.matvec(b, a, transpose_a=False)  # (num_courses,)
    
    # Get similarities
    query_sim = cos_sim(query_embedding, course_embeddings)
    
    # Get top candidates
    top40 = tf.math.top_k(query_sim, top_k).indices
    
    if nu_of_interaction > 5:
        personality_sim = cos_sim(personality_vector, tf.gather(course_embeddings, top40))
        hybrid_scores = 0.8 * tf.gather(query_sim, top40) + 0.2 * personality_sim
        sorted_indices = tf.argsort(hybrid_scores, direction='DESCENDING')
        return tf.gather(top40, sorted_indices)[:top]
    
    sorted_indices = tf.argsort(tf.gather(query_sim, top40), direction='DESCENDING')
    return tf.gather(top40, sorted_indices)[:top]

# Example usage
user_query = "i wanna learn linear algebra rigorosly"
recommended_courses = recommend(user_query, top=5)

for course_idx in recommended_courses.numpy():
    course = course_data.iloc[course_idx]
    print(f"Course: {course['course_name']}, Duration: {course['Duration']}, "
          f"Level: {course['level']}, Skills: {course['skills']}, "
          f"Provider: {course['provider']}, URL: {course['url']}, "
          f"Type: {course['type']}, Organization: {course['organization']}")
