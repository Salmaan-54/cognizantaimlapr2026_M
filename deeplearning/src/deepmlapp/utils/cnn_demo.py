#create cnn model classification using tf and keras for Rosary Church.jpeg image and save the model in resources folder
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from sympy import python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import cv2
from deepmlapp.configurations.conf import MODEL_FILE_PATH
import matplotlib.pyplot as plt

plt.rc('image', cmap='gray')
plt.rc('figure', autolayout=True)


image_path = MODEL_FILE_PATH

#use opencv to read the image and convert it to grayscale
#import cv2 from opencv-python package and read the image using cv2.imread() function and convert it to grayscale using cv2.cvtColor() function and resize it to 300x300 using cv2.resize() function and normalize the pixel values to be between 0 and 1 by dividing the pixel values by 255.0


image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
image = cv2.resize(image, (300, 300))
image = image.astype('float32') / 255.0

print("Original Image Shape:", image.shape)

plt.figure(figsize=(5,5))
plt.imshow(tf.squeeze(image))
plt.title("Original Image")
plt.axis('off')
plt.show()