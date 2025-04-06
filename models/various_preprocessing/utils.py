import tensorflow as tf
import joblib
from tensorflow import keras
from tensorflow.keras import layers, losses, Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Model

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
#autoencoder
@tf.keras.utils.register_keras_serializable()
class Autoencoder(Model):
    def __init__(self, input_size, latent_dim):
        super().__init__()
        # Use standard Input with shape instead of InputLayer
        self.encoder = Sequential([
            layers.Input(shape=(input_size,), name='main_input'),
            layers.Dense(latent_dim, activation='relu')
        ])
        self.decoder = Sequential([
            layers.Dense(input_size, activation='sigmoid')
        ])

    def call(self, inputs):
        encoded = self.encoder(inputs)
        decoded = self.decoder(encoded)
        return decoded


def main():
    data = pd.read_json('./combined_dataset.json').copy()['skills']
    #data = data.apply(lambda x: [] if x == ['NaN'] else x)
    mlb = MultiLabelBinarizer()
    x  = mlb.fit_transform(data)
    joblib.dump(mlb, '../recommendatoin_systems/final_Models/mlb_skill.pkl')

    len(x[1])
    x_1 , y = x[:int(len(x)*0.85)], x[int(len(x)*0.85):]
    del x
    latent_dimension= 24
    modelly = Autoencoder(input_size=len(x_1[1]), latent_dim=latent_dimension)
    modelly.compile(optimizer = 'adam', loss= losses.BinaryCrossentropy(), metrics = ["accuracy"])

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=2,
        restore_best_weights=True
    )
    modelly.fit(x_1,x_1, epochs=150, batch_size=128, shuffle=True, validation_data=(y, y), callbacks = [early_stopping])

    #modelly.encoder.save('../recommendatoin_systems/final_Models/encoder_skill.keras')
    dummy_input = tf.keras.Input(shape=(x_1.shape[1],))
    modelly(dummy_input)  # Build the model
    
    # Save using legacy format
    modelly.save_weights('../recommendatoin_systems/final_Models/autoencoderweights.weights.h5')
    #modelly.save(
    #    '../recommendatoin_systems/final_Models/autoencoder_skill.h5',
    #)
if __name__ == "__main__":
    main()

