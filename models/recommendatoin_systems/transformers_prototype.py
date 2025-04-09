import tensorflow as tf
from tensorflow.keras import layers, models

class CourseTransformer(tf.keras.Model):
    def __init__(
        self,
        max_seq_len: int,
        num_courses: int,
        d_model: int = 128,
        num_heads: int = 8,
        dff: int = 512,
        num_layers: int = 4,
        dropout_rate: float = 0.1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.max_seq_len = max_seq_len
        self.num_courses = num_courses
        self.d_model = d_model
        self.num_heads = num_heads
        self.dff = dff
        self.num_layers = num_layers
        self.dropout_rate = dropout_rate

        # Input projection
        self.feature_proj = layers.Dense(d_model)
        self.dropout = layers.Dropout(dropout_rate)
        
        # Positional embeddings
        self.position_embedding = layers.Embedding(
            input_dim=max_seq_len, output_dim=d_model
        )
        
        # Transformer encoder layers
        self.attention_layers = [
            layers.MultiHeadAttention(num_heads=num_heads, key_dim=d_model, dropout=dropout_rate)
            for _ in range(num_layers)
        ]
        self.ffn_layers = [
            self.create_ffn() for _ in range(num_layers)
        ]
        self.layernorm_layers = [
            layers.LayerNormalization(epsilon=1e-6) for _ in range(2 * num_layers)
        ]
        
        # Output layer
        self.classifier = layers.Dense(num_courses, activation='softmax')

    def create_ffn(self):
        return tf.keras.Sequential([
            layers.Dense(self.dff, activation='relu'),
            layers.Dense(self.d_model),
            layers.Dropout(self.dropout_rate)
        ])

    def call(self, inputs, training=False):
        # inputs shape: (batch_size, seq_len, 446)
        seq_len = tf.shape(inputs)[1]
        
        # Create padding mask
        mask = tf.cast(tf.math.not_equal(inputs[:, :, 0], 0), tf.float32)
        mask = mask[:, tf.newaxis, tf.newaxis, :]  # (batch, 1, 1, seq_len)
        
        # Project features and add positional embeddings
        x = self.feature_proj(inputs)
        x = self.dropout(x, training=training)
        positions = tf.range(start=0, limit=seq_len, delta=1)
        positions = self.position_embedding(positions)
        x += positions

        # Transformer layers
        for i in range(self.num_layers):
            # Self-attention
            attn_output = self.attention_layers[i](
                x, x, attention_mask=mask, training=training
            )
            x = self.layernorm_layers[2*i](x + attn_output)
            
            # Feed-forward network
            ffn_output = self.ffn_layers[i](x, training=training)
            x = self.layernorm_layers[2*i+1](x + ffn_output)

        # Use last token output for prediction
        x = x[:, -1, :]  # (batch_size, d_model)
        return self.classifier(x)

    def get_config(self):
        config = super().get_config()
        config.update({
            'max_seq_len': self.max_seq_len,
            'num_courses': self.num_courses,
            'd_model': self.d_model,
            'num_heads': self.num_heads,
            'dff': self.dff,
            'num_layers': self.num_layers,
            'dropout_rate': self.dropout_rate
        })
        return config
def main():
    # Example usage
    model = CourseTransformer(
        max_seq_len=100,
        num_courses=1000  # Replace with actual number of courses
    )

    # Build the model by calling it with dummy input
    dummy_input = tf.keras.Input(shape=(100, 446))
    model(dummy_input)
    model.summary()

if __name__ == "__main__":
    main()
