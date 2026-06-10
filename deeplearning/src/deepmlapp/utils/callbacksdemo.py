import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

#load the MNIST dataset - 10 digits (0-9) handwritten images
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

#normalize the pixel values to be between 0 and 1
x_train, x_test = x_train / 255.0, x_test / 255.0

#build a simple model with a callback to stop training when accuracy reaches 99%
model = keras.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])


