from tensorflow.keras import layers, Model, utils
import tensorflow as tf
if __name__=='__main__':
    import numpy as np
    from tensorflow.keras.callbacks import EarlyStopping
    from tensorflow.keras.callbacks import ModelCheckpoint

class VectorCombiner(Model):
    def __init__(self, vector_dim):
        super(VectorCombiner, self).__init__()
        self.dense = tf.keras.Sequential([
            layers.Dense(128,activation = 'relu', input_shape=(vector_dim * 2,)),
            layers.Dense(vector_dim,activation = 'linear')
                                          ])
        
    def call(self, inputs):
        combined = tf.concat(inputs, axis=-1)
        return self.dense(combined)

def generate_pairs(data, batch_size=1024):
    n = len(data)
    while True:
        indices = np.random.randint(0, n, size=(batch_size, 2))
        # Build the batch arrays using list comprehensions
        vec1 = np.array([data[i] for i in indices[:, 0]], dtype=np.float32)
        vec2 = np.array([data[i] for i in indices[:, 1]], dtype=np.float32)
        target = 0.9 * vec1 + 0.1 * vec2
        yield (vec1, vec2), target
        

# 3. Modified main function
def main():
    # Load your data
    data = np.load('../data/encoded_data.npy', allow_pickle=True)
    
    # Create model
    vector_dim = len(data[1])
    model = VectorCombiner(vector_dim)
    
    # Compile model
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4, clipnorm=1.0)
    model.compile(optimizer=optimizer , loss='mse', metrics=['mae'])
    
    # Create dataset using generator
#    dataset = tf.data.Dataset.from_generator(
#        lambda: generate_pairs(data)
#    )#.prefetch(tf.data.AUTOTUNE)
    dataset = tf.data.Dataset.from_generator(
        lambda: generate_pairs(data, batch_size=1024),
        output_signature=(
            (
                tf.TensorSpec(shape=(None, vector_dim), dtype=tf.float32),  # vec1
                tf.TensorSpec(shape=(None, vector_dim), dtype=tf.float32),  # vec2
            ),
            tf.TensorSpec(shape=(None, vector_dim), dtype=tf.float32)       # target
        )
    )
    
    # Train with memory-efficient approach


    #early_stopping = EarlyStopping(
    #    #monitor='val_loss',
    #    patience=2,
    #    restore_best_weights=True
    #)
    checkpoint_callback = ModelCheckpoint(
        filepath='./final_Models/personality.weights.h5',  # file to save weights
        monitor='loss',                    # metric to monitor; change to 'val_loss' if using validation data
        save_best_only=True,               # only save weights if the monitored metric improves
        save_weights_only=True,            # only save the weights (not the entire model)
        verbose=1
    )
    model.fit(
        dataset,
        steps_per_epoch=100,
        epochs=100,
        #shuffle=True,
        callbacks=[checkpoint_callback]
        #validation_data=(how to add validatoin for data generation?, ?)
    )
    #test_dataset = tf.data.Dataset.from_generator(
    #    lambda: generate_pairs(data, batch_size=1024),
    #    output_signature=(
    #        (
    #            tf.TensorSpec(shape=(None, vector_dim), dtype=tf.float32),
    #            tf.TensorSpec(shape=(None, vector_dim), dtype=tf.float32),
    #        ),
    #        tf.TensorSpec(shape=(None, vector_dim), dtype=tf.float32)
    #    )
    #)

    #results = model.evaluate(test_dataset, steps=10, verbose=1)


if __name__ == '__main__':
    main()

vec_dim = 446
personality_updater = VectorCombiner(vec_dim)
dummy_vec1 = tf.zeros([1, vec_dim], dtype=tf.float32)
dummy_vec2 = tf.zeros([1, vec_dim], dtype=tf.float32)
personality_updater((dummy_vec1, dummy_vec2))
personality_updater.load_weights('/home/karar/Desktop/recom/models/recommendatoin_systems/final_Models/personality.weights.h5')
