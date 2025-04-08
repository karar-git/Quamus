#ayooo

#    |███████|        |███████|
#    |███████|        |███████|
#    |███████|        |███████|
#    ...              ...
#    |███████|        |███████|
#    |███████|        |███████|
#    |███████|        |███████|
#    |███████|        |███████|
#==================================#
if __name__=='__main__':
    from tensorflow.keras.callbacks import ModelCheckpoint
    import numpy as np
    #from recom_mod import cos_sim, cos_sim_vec, cos_sim_mat, get_score
#cos_simi = tf.keras.layers.Dot(axes=-1, normalize=True)

import tensorflow as tf
import os
from tensorflow.keras import layers, Model, utils
class UserTower(layers.Layer):
    def __init__(self, vector_dim):
        super().__init__()
        self.dense = tf.keras.Sequential([
            layers.Dense(2 * vector_dim, activation="relu", name='user_dense1'),
            layers.Dense(128, activation='relu', name='user_dense2'),
            layers.Dense(64, name='user_dense3')
        ])
    
    def call(self, inputs):
        input_vec, personality = inputs
        concatenated = tf.concat([input_vec, personality], axis=-1)
        return self.dense(concatenated)

class ItemTower(layers.Layer):
    def __init__(self, vector_dim):
        super().__init__()
        self.dense = tf.keras.Sequential([
            layers.Dense(vector_dim, activation="relu", name = 'item_dense1'),
            layers.Dense(64, name='item_dense2')
        ])
    
    def call(self, item_input):
        return self.dense(item_input)



class TwoTowerModel(Model):
    def __init__(self, vector_dim):
        super(TwoTowerModel, self).__init__()
        self.user_tower = UserTower(vector_dim)
        self.item_tower = ItemTower(vector_dim)
        self.cosine_similarity = layers.Dot(axes=-1, normalize=True)
        
    def call(self, inputs):
        # Unpack the three input components
        user_input, personality_input, item_input = inputs
        
        # Process through towers
        user_embedding = self.user_tower([user_input, personality_input])
        item_embedding = self.item_tower(item_input)
        
        # Calculate similarity
        return self.cosine_similarity([user_embedding, item_embedding])
    
    #def build_model(self):
    #    # Explicit input definition for model summary/visualization
    #    user_input = layers.Input(shape=(vec_dim,), name='user_input')
    #    personality_input = layers.Input(shape=(vec_dim,), name='personality_input')
    #    item_input = layers.Input(shape=(vec_dim,), name='item_input')
    #    return Model(
    #        inputs=[user_input, personality_input, item_input],
    #        outputs=self.call([user_input, personality_input, item_input])
    #    )

class recommender():
    def __init__(self, vec_dim) -> None:
        self.model = TwoTowerModel(vec_dim)

        dummy_user = tf.zeros((1, vec_dim))
        dummy_personality = tf.zeros((1, vec_dim))
        dummy_item = tf.zeros((1, vec_dim))
        _ = self.model((dummy_user, dummy_personality, dummy_item))

        #base_dir = os.path.dirname(os.path.abspath(__file__))
        #weights_path = os.path.join(base_dir, '../recommendatoin_systems/final_Models/911.weights.h5')
        #weights_path = os.path.normpath(weights_path)
        self.model.load_weights('/home/karar/Desktop/recom/models/recommendatoin_systems/final_Models/911.weights.h5')


    def recommend(self, user_query, top_k=5):
        """
        Given a user query vector (of shape (446,) or (1, 446)), this method:
          1. Processes the query through the user tower (using a zero personality vector).
          2. Computes cosine similarity between the user embedding and all item embeddings.
          3. Returns the top_k indices of the best matching courses.
        """
        if len(user_query.shape) == 1:
            user_query = tf.expand_dims(user_query, axis=0)
        
        
        # Compute user embedding from the user tower.
        # We assume user_query is already a vector in the same space as the model expects.
        user_embedding = self.model.user_tower([user_query, user_personality])
        # Normalize the user embedding.
        user_embedding_norm = tf.nn.l2_normalize(user_embedding, axis=-1)
        # Normalize the item embeddings.
        item_embeddings_norm = tf.nn.l2_normalize(self.item_embeddings, axis=-1)
        # Compute cosine similarity: result shape (1, num_items)
        similarity_scores = tf.matmul(user_embedding_norm, item_embeddings_norm, transpose_b=True)
        similarity_scores = tf.squeeze(similarity_scores, axis=0)
        
        # Get the top_k indices from the similarity scores.
        top_values, top_indices = tf.math.top_k(similarity_scores, k=top_k)
        return top_indices
        
        


def generate_pairs_1(data, batch_size=1024):
    n = len(data)
    while True:
        # Randomly sample pairs without storing all combinations
        indices = np.random.randint(0, n, size=(batch_size, 3))
        vec1 = np.array([data[i] for i in indices[:, 0]], dtype=np.float32)
        vec2 = np.array([data[i] for i in indices[:, 1]], dtype=np.float32)
        vec3 = np.array([data[i] for i in indices[:, 2]], dtype=np.float32)
        target = 0.9 * vec1 + 0.1 * vec2
        norm_target = tf.nn.l2_normalize(target, axis=1)
        target = cos_simi([target, vec3])
        target = tf.reshape(target, [-1, 1])  # Ensures the shape is (batch_size, 1)
        yield (vec1, vec2, vec3), target


def main():
    data = np.load('../data/encoded_data.npy', allow_pickle=True)
    vector_dim = len(data[1])
    model = TwoTowerModel(vector_dim)
    dummy_user = tf.zeros((1, vector_dim))
    dummy_personality = tf.zeros((1, vector_dim))
    dummy_item = tf.zeros((1, vector_dim))
    _ = model((dummy_user, dummy_personality, dummy_item))
    
    cos_simi = layers.Dot(axes=-1, normalize=True)
    model.compile(optimizer='adam', loss='mse', metrics= ['mae'])
    # Create dataset with proper signature
    dataset = tf.data.Dataset.from_generator(
        lambda: generate_pairs_1(data, batch_size=1024),
        output_signature=(
            (
                tf.TensorSpec(shape=(None, vector_dim), dtype=tf.float32),
                tf.TensorSpec(shape=(None, vector_dim), dtype=tf.float32),
                tf.TensorSpec(shape=(None, vector_dim), dtype=tf.float32)
            ),
            tf.TensorSpec(shape=(None, 1), dtype=tf.float32)
        )
    )
    
    checkpoint_callback = ModelCheckpoint(
        './final_Models/911.weights.h5',
        monitor='loss',
        save_best_only=True,
        save_weights_only=True,
        verbose=1
    )
    
    model.fit(
        dataset,
        steps_per_epoch=100,
        epochs=100,
        callbacks=[checkpoint_callback]
    )

def get_item():
    import numpy as np
    data = np.load('../data/encoded_data.npy', allow_pickle=True)
    data = np.vstack(data)  # Convert list of arrays into a uniform 2D array.
    vector_dim = len(data[1])
    model = TwoTowerModel(vector_dim)

    dummy_user = tf.zeros((1, vector_dim))
    dummy_personality = tf.zeros((1, vector_dim))
    dummy_item = tf.zeros((1, vector_dim))
    _ = model((dummy_user, dummy_personality, dummy_item))
    model.load_weights('./final_Models/911.weights.h5')
    predic = model.item_tower(data)
    np.save('../../Tighba_gui/item_embedding.npy', predic)
    recom = recommender(vector_dim)
#if __name__ == '__main__':
recom = recommender(446)

