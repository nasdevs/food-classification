import tensorflow as tf
from keras.models import load_model

def confidence(y_true, y_pred):
    return tf.reduce_max(y_pred, axis=-1)

def load_custom_model(model_path):
    return load_model(model_path, custom_objects={'confidence': confidence})
