import joblib
from tensorflow import convert_to_tensor, data
import numpy as np
from utils import Autoencoder
from sklearn.preprocessing import OneHotEncoder
from sentence_transformers import SentenceTransformer
import pandas as pd
import tensorflow as tf

tf.experimental.numpy.experimental_enable_numpy_behavior()
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_colwidth', None)
## Load the model
#my_vect_model = SentenceTransformer("paraphrase-MiniLM-L12-v2")
## Load JSON data
#data = pd.read_json('./combined_dataset.json').copy()
def pipe_for_sim(dataaaa):
    #dataaaa['description'] = 'title: ' + dataaaa['course_name'] + " | description: "+ dataaaa['description']
    dataaaa.drop(columns=['url', 'course_name','organization', 'instructor', 'subject', 'has_subject', 'reviews'],inplace = True)
    dataaaa.fillna(0, inplace = True)
    for col in dataaaa.columns:
        if dataaaa[col].dtype == 'object':  # Check if it's stored as a string
            try:
                dataaaa[col] = pd.to_numeric(dataaaa[col])  # Convert if possible
            except (ValueError, TypeError):
                pass  # Skip
    #handle reviews? do it later :) u could encode them, take the average or whatever
    def level_handler(dataaaaaaa):
        if isinstance(dataaaaaaa, list):
            if len(dataaaaaaa) ==1:
                return dataaaaaaa[0]
            else: return "mixed"
        else: return dataaaaaaa 
    dataaaa['level'] = dataaaa['level'].apply(level_handler)
    for i in ['level', 'provider', 'type']:
        encoder = OneHotEncoder(sparse_output=False)
        encoded_= encoder.fit_transform(dataaaa[[i]])  

        dataaaa[i] = encoded_.tolist()  
    def change(rating):
        if rating == 'No rating':
            return 0
        return rating
    dataaaa['rating'] = dataaaa['rating'].apply(change)
    dataaaa['description'] = my_vect_model.encode(dataaaa['description']).tolist()


    skills_array = mlb_skill.transform(dataaaa['skills'])  # Expecting shape: (13793, 11898)
    skills_tensor = tf.convert_to_tensor(skills_array, dtype=tf.float32)
    skills_tensor.shape
    #dataaaa['skills'] = encoder_skill.encoder(skills_tensor).numpy()
    dataaaa['skills'] = list(encoder_skill.encoder(skills_tensor).numpy())
    #encoded_skills = encoder_skill.encoder(skills_tensor).numpy()
    #dataaaa['skills'] = np.mean(encoded_skills, axis=0)
    
    lists= ['description', 'level', 'provider', 'type', 'skills']
    def conca(row):
        # Convert each list-like feature to a NumPy array
        list_features = np.concatenate([np.array(row[col]) for col in lists])
        # Drop the specified list columns using 'labels' instead of 'columns'
        numeric_features = row.drop(labels=lists).apply(lambda x: float(str(x).replace(',', ''))).values
        return np.concatenate([list_features, numeric_features])
    return dataaaa.apply(conca, axis =1)

#normalization_layer = tf.keras.layers.Normalization()
def all_data(data):

    #data['skills'] = data['skills'].apply(lambda x: [] if x == ['NaN'] else x)
    #dataa = pipe_for_sim(data)
    dataa = pipe_for_sim(data)
    normalization_layer = tf.keras.layers.Normalization()
    normalization_layer.adapt(dataa)
    tf.saved_model.save(normalization_layer, '../recommendatoin_systems/final_Models/norm_layer')
    encoded_data = normalization_layer(dataa)

    return encoded_data
def user_embedding(data):
    the_vector=pipe_for_sim(data)
    encoded_data = normalization_layer(the_vector)
    return encoded_data
#AWHAT = pipe_for_sim(data)
def main():

    my_vect_model = SentenceTransformer("paraphrase-MiniLM-L12-v2")
    dataa = pd.read_json('./combined_dataset.json')
    mlb_skill = joblib.load('../recommendatoin_systems/final_Models/mlb_skill.pkl')
    input_shape = 11898
    encoder_skill = Autoencoder(input_shape, latent_dim=24)
    encoder_skill.build(input_shape)
    encoder_skill.load_weights('../recommendatoin_systems/final_Models/autoencoderweights.weights.h5')
    
    # Check the encoder_skill's architecture
    encoder_skill.summary()
    encoded_final_ = all_data(dataa)
    np.save("../data/encoded_data.npy", encoded_final_)
    print("Embeddings have been successfully saved!")


if __name__ == '__main__':
    main()
