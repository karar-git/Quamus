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
import tensorflow as tf
from recom_mod import cos_sim
import numpy as np
from tensorflow.keras import layers, losses, Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Model
class personality_updater(Model):
    def __init__(input_dim, Dense_size = [128], num_hidden_layer = 1  ):
        super.__init__()
        self.input_dim = input_dim, self.Dense_Size = Dense_size, self.num_hidden_layer = num_hidden_layer
        self.model = Sequential(
            [layers.Input(shape = input_dim),
             layers.concat(),
             [layers.Dense(size, activation = 'relu') for size,i in zip(Dense_size, range(len(num_hidden_layer)))] 
             layer.Dense(shape = input_dim)
        ])
    def call(self.data):
        return self.model(x)
def train(modelly, input, output, epochs = 100, patience=2):
    modelly = personality_updater((len(input),),)
    modelly.compile(optimizer = 'adam', loss= losses.MSE, metrics = ["MSE"])
    output_val = output[int(len(output)* 0.9): ]
    input_val= input[int(len(input)* 0.9): ]

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=patience,
        restore_best_weights=True
    )
    modelly.fit([input[0],input[1]], output, epochs=epochs, batch_size=256, shuffle=True, validation_data=(input_val, output_val), callbacks = [early_stopping])

    modelly.encoder.save('../recommendatoin_systems/final_Models/personality.keras')
def main():
    data = np.load('../data/encoded_data.npy')
    data = product(data, 2)
    output = 0.9 data[0] + 0.1 data[1]
    model = personality_updater(len(data[0]))
    train(model, data, output)


if __name__== '__main__':
    main()

