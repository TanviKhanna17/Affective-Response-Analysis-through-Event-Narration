import tensorflow as tf
from transformers import TFAutoModel


# Load the model
loaded_model = tf.keras.models.load_model('MINOR_QUESTIONS/mcq_indecisiveness_model/saved_albert_model/saved_model.pb')

# Run inference
result = get_sentiment2(loaded_model, "I feel very sad and lonely")
plot_result(result)
