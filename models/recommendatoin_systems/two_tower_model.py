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
    import tensorflow as tf
    from tensorflow.keras import layers, Model, utils
    #from recom_mod import cos_sim, cos_sim_vec, cos_sim_mat, get_score
#cos_simi = tf.keras.layers.Dot(axes=-1, normalize=True)
class UserTower(layers.Layer):
    def __init__(self, vector_dim):
        super().__init__()
        self.dense = tf.keras.Sequential([
            layers.Dense(2 * vector_dim, activation="relu"),
            layers.Dense(128, activation='relu'),
            layers.Dense(64)
        ])
    
    def call(self, inputs):
        input_vec, personality = inputs
        concatenated = tf.concat([input_vec, personality], axis=-1)
        return self.dense(concatenated)

class ItemTower(layers.Layer):
    def __init__(self, vector_dim):
        super().__init__()
        self.dense = tf.keras.Sequential([
            layers.Dense(vector_dim, activation="relu"),
            layers.Dense(64)
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
    
    def build_model(self):
        # Explicit input definition for model summary/visualization
        user_input = layers.Input(shape=(vector_dim,), name='user_input')
        personality_input = layers.Input(shape=(vector_dim,), name='personality_input')
        item_input = layers.Input(shape=(vector_dim,), name='item_input')
        return Model(
            inputs=[user_input, personality_input, item_input],
            outputs=self.call([user_input, personality_input, item_input])
        )


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
    model = TwoTowerModel(vector_dim).build_model()
    
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

if __name__ == '__main__':
    main()
