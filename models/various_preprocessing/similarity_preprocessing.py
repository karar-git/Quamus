import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sentence_transformers import SentenceTransformer
import pandas as pd
import tensorflow as tf
from torch import norm

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
# Load the model
my_vect_model = SentenceTransformer("paraphrase-MiniLM-L12-v2")
# Load JSON data
data = pd.read_json('./combined_dataset.json').copy()
def pipe_for_sim(data):
    data['description'] = 'title: ' + data['course_name'] + " | description: "+ data['description']
    data.drop(columns=['url', 'course_name','organization', 'instructor', 'subject', 'has_subject', 'reviews'],inplace = True)
    data.fillna(0, inplace = True)
    for col in data.columns:
        if data[col].dtype == 'object':  # Check if it's stored as a string
            try:
                data[col] = pd.to_numeric(data[col])  # Convert if possible
            except (ValueError, TypeError):
                pass  # Skip
    #handle reviews? do it later :) u could encode them, take the average or whatever
    def level_handler(dataaaa):
        if isinstance(dataaaa, list):
            if len(dataaaa) ==1:
                return dataaaa[0]
            else: return "mixed"
        else: return dataaaa 
    data['level'] = data['level'].apply(level_handler)
    for i in ['level', 'provider', 'type']:
        encoder = OneHotEncoder(sparse_output=False)
        encoded_= encoder.fit_transform(data[[i]])  

        data[i] = encoded_.tolist()  
    def change(rating):
        if rating == 'No rating':
            return 0
        return rating
    data['rating'] = data['rating'].apply(change)
    data['description'] = my_vect_model.encode(data['description']).tolist()
    data['skills'] = mlb_skill.transform(data['skills'])
    data['skills'] = encoder_skill(data['skills'])
    data['skills'] = np.mean(data['skills'], axis = 1)
    lists= ['description', 'level', 'provider', 'type', 'skills']
    def conca(row):
        # Convert each list-like feature to a NumPy array
        list_features = np.concatenate([np.array(row[col]) for col in lists])
        # Drop the specified list columns using 'labels' instead of 'columns'
        numeric_features = row.drop(labels=lists).apply(lambda x: float(str(x).replace(',', ''))).values
        return np.concatenate([list_features, numeric_features])
    return data.apply(conca, axis =1)

normalization_layer = tf.keras.layers.Normalization()
def all_data(data):
    dataa = pipe_for_sim(data)
    normalization_layer = tf.keras.layers.Normalization()
    normalization_layer.adapt(dataa)
    tf.saved_model.save(,normalization_layer, 'norm_layer')
    encoded_data = normalization_layer(dataa)

    return encoded_data
def onecourse_(data):
    the_vector=pipe_for_sim(data)
    encoded_data = normalization_layer(the_vector)
def save_norm_lay():
    pass
#AWHAT = pipe_for_sim(data)
