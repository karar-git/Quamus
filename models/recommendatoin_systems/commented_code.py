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
