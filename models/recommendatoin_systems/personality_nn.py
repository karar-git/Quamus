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
    import numpy as np
    import tensorflow as tf
    from tensorflow.keras import layers, Model, utils

# 1. Create a simplified model that handles the weighted combination directly
class VectorCombiner(Model):
    def __init__(self, vector_dim):
        super(VectorCombiner, self).__init__()
        self.dense = layers.Dense(vector_dim, activation='linear')
        
    def call(self, inputs):
        # inputs should be a tuple of (vector1, vector2)
        combined = tf.concat(inputs, axis=-1)
        return self.dense(combined)

# 2. Memory-efficient data generation
def generate_pairs(data, batch_size=1024):
    n = len(data)
    while True:
        # Randomly sample pairs without storing all combinations
        indices = np.random.randint(0, n, size=(batch_size, 2))
        vec1 = data[indices[:, 0]]
        vec2 = data[indices[:, 1]]
        target = 0.9 * vec1 + 0.1 * vec2
        yield [vec1, vec2], target

# 3. Modified main function
def main():
    # Load your data
    data = np.load('../data/encoded_data.npy', allow_pickle=True)
    
    # Create model
    vector_dim = len(data[1])
    model = VectorCombiner(vector_dim)
    
    # Compile model
    model.compile(optimizer='adam', loss='mse')
    
    # Create dataset using generator
    dataset = tf.data.Dataset.from_generator(
        lambda: generate_pairs(data),
        output_types=(tf.float64, tf.float64),
        output_shapes=([None, vector_dim], [None, vector_dim])
    ).prefetch(tf.data.AUTOTUNE)
    
    # Train with memory-efficient approach
    model.fit(
        dataset,
        steps_per_epoch=100,  # Adjust based on your needs
        epochs=10,
        callbacks=[
            tf.keras.callbacks.ModelCheckpoint(
                '../recommendatoin_systems/final_Models/personality.keras',
                save_best_only=True
            )
        ]
    )

if __name__ == '__main__':
    main()



