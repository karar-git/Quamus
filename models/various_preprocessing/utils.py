import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, losses, Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Model

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
#autoencoder :)
class autoencoder(Model):
    def __init__(self, input_size: tuple or int, latent_dimension: tuple or int) -> None:
        super().__init__()
        self.encoder = Sequential([
        layers.Input(shape = input_size),
        layers.Dense(latent_dimension, activation= 'relu')
        ])
        self.decoder = Sequential([
        layers.Dense(input_size[0], activation= 'sigmoid')
        ])
    def call(self, data):
        encoded = self.encoder(data)
        decoded = self.decoder(encoded)

        return decoded
def main():
    data = pd.read_json('./combined_dataset.json').copy()['skills']

    mlb = MultiLabelBinarizer()
    x  = mlb.fit_transform(data)
    len(x[1])
    x_1 , y = x[:int(len(x)*0.85)], x[int(len(x)*0.85):]
    del x
    latent_dimension= 24
    modelly = autoencoder(input_size=(len(x_1[1]),), latent_dimension=latent_dimension)
    modelly.compile(optimizer = 'adam', loss= losses.BinaryCrossentropy, metrics = ["accuracy"])

    early_stopping = EarlyStopping(
        monitor='val_loss',  # Metric to monitor (e.g., 'val_loss' or 'val_accuracy')
        patience=3,          # Number of epochs to wait before stopping if no improvement
        restore_best_weights=True  # Restores the best weights when stopping
    )
    modelly.fit(x_1,x_1, epochs=100, batch_size=128, shuffle=True, validation_data=(y, y), callbacks = [early_stopping])

    encoded = modelly.encoder(x)
    #normalization_layer = tf.keras.layers.Normalization()
    #normalization_layer.adapt(encoded)
    #encoded = normalization_layer(encoded)

if __name__ == "__main__":
    main()

