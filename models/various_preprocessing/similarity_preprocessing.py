import joblib
from tensorflow import convert_to_tensor, data
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sentence_transformers import SentenceTransformer
import pandas as pd
import tensorflow as tf
if __name__=='__main__':
    from utils import Autoencoder
    tf.experimental.numpy.experimental_enable_numpy_behavior()
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_colwidth', None)
## Load the model
#my_vect_model = SentenceTransformer("paraphrase-MiniLM-L12-v2")
## Load JSON data
#data = pd.read_json('./combined_dataset.json').copy()

def pipe_for_sim(dataaaa, my_vect_model, mlb_skill, encoder_skill, level_enc, provider_enc, type_enc):
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

    encoders = {
        'level': level_enc,
        'provider': provider_enc,
        'type': type_enc
    }

    for i in ['level', 'provider', 'type']:
       # encoded_= f"{i}_enc".transform(dataaaa[[i]])  
       # dataaaa[i] = encoded_.tolist()  
        encoded_ = encoders[i].transform(dataaaa[[i]])
        dataaaa[i] = encoded_.tolist()

    def change(rating):
        if rating == 'No rating':
            return 0
        return rating
    dataaaa['rating'] = dataaaa['rating'].apply(change)



    dataaaa['description'] = dataaaa['description'].astype(str)

    # 2) Encode descriptions
    desc_list = dataaaa['description'].tolist()
    desc_embs = my_vect_model.encode(desc_list)
    dataaaa['description'] = desc_embs.tolist()

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
def all_data(data, my_vect_model):

    #data['skills'] = data['skills'].apply(lambda x: [] if x == ['NaN'] else x)
    #dataa = pipe_for_sim(data)
    dataa = pipe_for_sim(dataa, my_vect_model)
    #dataa = np.array(dataa, dtype=np.float32)
    dataa.shape
    dataa = np.vstack(dataa.to_numpy())
    #tf.saved_model.save(normalization_layer, '../recommendatoin_systems/final_Models/norm_layer')



    # Suppose feature_dim = number of inputs (e.g. 446)
    feature_dim = 446

    # 1) Wrap your layer in a tiny Model

    inputs = tf.keras.Input(shape=(feature_dim,))

    normalization_layer = tf.keras.layers.Normalization()
    outputs = normalization_layer(inputs)
    normalization_layer.adapt(dataa)
    norm_model = tf.keras.Model(inputs=inputs, outputs=outputs)

    # 2) (Optional) call on dummy to build
    _ = norm_model(tf.zeros([1, feature_dim]))

    # 3) Save as a .keras file
    norm_model.save(
        '../recommendatoin_systems/final_Models/norm_layer.keras',
        save_format='keras'
    )

    encoded_data = normalization_layer(dataa)

    return encoded_data
def user_embedding(data, my_vect_model, mlb_skills, normalization_layer, encoder_skills,level_enc, provider_enc, type_enc):
    the_vector=pipe_for_sim(data, my_vect_model, mlb_skills, encoder_skills,level_enc, provider_enc, type_enc)

    matrix = np.stack(the_vector.values)  # shape=(N, D), dtype=float

    # 3) convert to tensor (if your norm layer expects tf.Tensor)
    tensor = tf.convert_to_tensor(matrix, dtype=tf.float32)

    
    encoded_data = normalization_layer(tensor)
    return encoded_data
#AWHAT = pipe_for_sim(data)
def main():
    #from sklearn.preprocessing import OneHotEncoder
    #import joblib

    #import pandas as pd
    #def level_handler(dataaaaaaa):
    #    if isinstance(dataaaaaaa, list):
    #        if len(dataaaaaaa) ==1:
    #            return dataaaaaaa[0]
    #        else: return "mixed"
    #    else: return dataaaaaaa 
    #dataa['level'] = dataa['level'].apply(level_handler)
    ## Suppose df_all is your full combined dataset
    #level_enc = OneHotEncoder(sparse_output=False, handle_unknown='ignore').fit(dataa[['level']])
    #provider_enc = OneHotEncoder(sparse_output=False, handle_unknown='ignore').fit(dataa[['provider']])
    #type_enc = OneHotEncoder(sparse_output=False, handle_unknown='ignore').fit(dataa[['type']])

    ## Save them
    #joblib.dump(level_enc, '../recommendatoin_systems/final_Models/level_enc.pkl')
    #joblib.dump(provider_enc, '../recommendatoin_systems/final_Models/provider_enc.pkl')
    #joblib.dump(type_enc, '../recommendatoin_systems/final_Models/type_enc.pkl')
    


    dataa = pd.read_json('./combined_dataset.json').copy()
    my_vect_model = SentenceTransformer("paraphrase-MiniLM-L12-v2")
    mlb_skill = joblib.load('../recommendatoin_systems/final_Models/mlb_skill.pkl')
    input_shape = 11898
    encoder_skill = Autoencoder(input_shape, latent_dim=24)

    dummy_input = tf.keras.Input(shape=(input_shape,))
    encoder_skill(dummy_input)  # Build the model
    encoder_skill.load_weights('../recommendatoin_systems/final_Models/autoencoderweights.weights.h5')
    
    # Check the encoder_skill's architecture
    encoder_skill.summary()
    encoded_final_ = all_data(dataa, my_vect_model)
    np.save("../data/encoded_data.npy", encoded_final_)
    print("Embeddings have been successfully saved!")


if __name__ == '__main__':
    main()
