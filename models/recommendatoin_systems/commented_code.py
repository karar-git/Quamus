#class PersonalityUpdater(Model):
#    def __init__(self, input_dim):
#        super(PersonalityUpdater, self).__init__()
#        self.input_dim = input_dim
#        self.dense_sizes = 128
#        
#        # Define model architecture
#        self.input_layer1 = layers.Input(shape=(input_dim,))
#        self.input_layer2 = layers.Input(shape=(input_dim,))
#        self.concat = layers.Concatenate()([self.input_layer1, self.input_layer2])
#        
#        self.dense_layers = layers.Dense(self.dense_sizes, activation='relu')
#        
#        self.output_layer = layers.Dense(input_dim)
#        
#    def call(self, inputs):
#        x = self.concat(inputs)
#        x=self.dense_layers(x)
#        return self.output_layer(x)
#
#def train(model, input_pairs, output, epochs=100, patience=2):
#    model.compile(optimizer='adam', loss=losses.MSE, metrics=["MSE"])
#    
#    # Split data
#    split_idx = int(len(output) * 0.9)
#    train_data = ([input_pairs[0][:split_idx], input_pairs[1][:split_idx]], output[:split_idx])
#    val_data = ([input_pairs[0][split_idx:], input_pairs[1][split_idx:]], output[split_idx:])
#
#    early_stopping = EarlyStopping(
#        monitor='val_loss',
#        patience=patience,
#        restore_best_weights=True
#    )
#    
#    model.fit(
#        x=train_data[0],
#        y=train_data[1],
#        epochs=epochs,
#        batch_size=256,
#        shuffle=True,
#        validation_data=val_data,
#        callbacks=[early_stopping]
#    )
#    
#    model.save('../recommendatoin_systems/final_Models/personality.keras')
#
#def main():
#    # Load and prepare data
#    data = np.load('../data/encoded_data.npy', allow_pickle=True)
#
#    
#    # Generate all possible pairs (this could be memory intensive!)
#    pairs = list(product(data, repeat=2))
#    input1 = np.array([p[0] for p in pairs])
#    input2 = np.array([p[1] for p in pairs])
#    output = 0.9 * input1 + 0.1 * input2
#    
#    # Create model
#    input_dim = len(data[1])
#    model = PersonalityUpdater(input_dim)
#    
#    # Train
#    train(model, (input1, input2), output)
#    model.predict((input1, input2))
#
#    model.save_weights('../recommendatoin_systems/final_Models/personlity.weights.h5')
#
#if __name__ == '__main__':
#    main()
#




#class user_tower(Model):
#    def __init__(self, vector_dim) -> None:
#        super().__init__()
#
#        self.dense = tf.keras.Sequential([
#            tf.keras.layers.Dense((2*vector_dim,), activation="relu"),
#            tf.keras.layers.Dense(128, activation = 'relu'),
#            tf.keras.layers.Dense(64)
#        ])
#    def call(self, inputs):
#        input_vec, personality = inputs
#        concatenated = tf.concat([input_vec, personality], axis=-1)
#        return self.dense(concatenated)
#
#class item_tower(Model):
#    def __init__(self, vector_dim) -> None:
#        super().__init__()
#
#        self.dense = tf.keras.Sequential([
#            tf.keras.layers.Dense((vector_dim,), activation="relu"),
#            tf.keras.layers.Dense(64)
#        ])
#    def call(self,item):
#        return self.dense(item)
#
#class Two_tower_recommender(Model):
#    def __init__(self, vector_dim):
#        super(Two_tower_recommender, self).__init__()
#        self.user = user_tower(vector_dim*2)
#        self.item= item_tower(vector_dim)
#        #self.dense = layers.Dense()
#        #self.output = layers.Tanh()
#        
#        self.cosine_similarity = layers.Dot(axes=1, normalize=True, name='cosine_similarity')
#    def call(self, inputs):
#        # inputs should be a tuple of (vector1, vector2)
#        user, person, item = inputs
#        user_ = self.user((user,person))
#        item_ = self.item(item)
#
#        return self.cosine_similarity(user_, item_)
#
#
#def generate_pairs_1(data, batch_size=1024):
#    n = len(data)
#    while True:
#        # Randomly sample pairs without storing all combinations
#        indices = np.random.randint(0, n, size=(batch_size, 3))
#        vec1 = np.array([data[i] for i in indices[:, 0]], dtype=np.float32)
#        vec2 = np.array([data[i] for i in indices[:, 1]], dtype=np.float32)
#        vec3 = np.array([data[i] for i in indices[:, 2]], dtype=np.float32)
#        target = 0.9 * vec1 + 0.1 * vec2
#        target = cos_simi(target, vec3)
#        yield (vec1, vec2, vec3), target
#
#
#
#def main():
#    # Load your data
#    data = np.load('../data/encoded_data.npy', allow_pickle=True)
#    cos_simi= layers.Dot(axes=1, normalize=True)
#    # Create model
#    vector_dim = len(data[1])
#    model = Two_tower_recommender(vector_dim)
#    
#    # Compile model
#    model.compile(optimizer='adam', loss='mse', metrics= ['mae'])
#    
#
#    dataset = tf.data.Dataset.from_generator(
#        lambda: generate_pairs_1(data, batch_size=1024),
#        output_signature=(
#            (
#                tf.TensorSpec(shape=(None, vector_dim), dtype=tf.float32),  # vec1
#                tf.TensorSpec(shape=(None, vector_dim), dtype=tf.float32),  # vec2
#                tf.TensorSpec(shape=(None, vector_dim), dtype=tf.float32),  # vec3
#            ),
#            tf.TensorSpec(shape=(None, 1), dtype=tf.float32)       # target
#        )
#    )
#    
#    # Train with memory-efficient approach
#
#    checkpoint_callback = ModelCheckpoint(
#        filepath='./final_Models/911.weights.h5',  # file to save weights
#        monitor='loss',                    # metric to monitor; change to 'val_loss' if using validation data
#        save_best_only=True,               # only save weights if the monitored metric improves
#        save_weights_only=True,            # only save the weights (not the entire model)
#        verbose=1
#    )
#
#    model.fit(
#        dataset,
#        steps_per_epoch=100,
#        epochs=100,
#        #shuffle=True,
#        callbacks=[checkpoint_callback]
#        #validation_data=(how to add validatoin for data generation?, ?)
#    )
#
#if __name__ == '__main__':
#    main()
