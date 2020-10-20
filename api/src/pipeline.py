import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras import optimizers
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing import image
import os

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#setting up the preocesses and the classifier object
#building the architecture
#lets start with AlexNet
classifier = Sequential()


'''
    template of the networks 
    classifier.add(Convolution2D(, , strides = (), padding = "", activation = ""))
    classifier.add(MaxPooling2D(pool_size = (), strides = (), padding = ))
    classifier.add(BatchNormalization())
'''


#first convolution set
classifier.add(Convolution2D(96, 11, strides = (4,4), padding = 'valid', input_shape = (224,224,3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2,2), strides = (2,2), padding = "valid"))
classifier.add(BatchNormalization())

#second convolution set
classifier.add(Convolution2D(256, 11, strides = (1,1), padding = "valid", activation = "relu"))
classifier.add(MaxPooling2D(pool_size = (2,2), strides = (2,2), padding = "valid"))
classifier.add(BatchNormalization())

#third convolution set
classifier.add(Convolution2D(384, 3, strides = (1,1), padding = "valid", activation = "relu"))
classifier.add(BatchNormalization())

#fourth convolution set
classifier.add(Convolution2D(384, 3, strides = (1,1), padding = "valid", activation = "relu"))
classifier.add(BatchNormalization())

#fifth convolution set
classifier.add(Convolution2D(256, 3, strides = (1,1), padding = "valid", activation = "relu"))
classifier.add(MaxPooling2D(pool_size = (2,2), strides = (2,2), padding = "valid"))
classifier.add(BatchNormalization())

#flattening step
classifier.add(Flatten())

#dense network
classifier.add(Dense(units = 4096, activation = "relu"))
classifier.add(Dropout(0.4))
classifier.add(BatchNormalization())

classifier.add(Dense(units = 4096, activation = "relu"))
classifier.add(Dropout(0.4))
classifier.add(BatchNormalization())

classifier.add(Dense(units = 1000, activation = 'relu'))
classifier.add(Dropout(0.2))
classifier.add(BatchNormalization())

classifier.add(Dense(units = 10, activation = "softmax"))
dir_name = os.path.dirname(os.path.abspath(__file__))
classifier.load_weights(dir_name + '/best_weights_late_2020.hdf5')

li = ['Bacterial_spot','Early_blight','Late_blight','Leaf_Mold','Septoria_leaf_spot','Target_Spot','Yellow_Leaf_Curl','healthy','mosaic_virus','spider_mite']

def get_class(image_path):
    img_width, img_height = 224, 224
    img = image.load_img(image_path, target_size = (img_width, img_height))
    img = image.img_to_array(img) / 255
    img = np.expand_dims(img, axis = 0)
    value = classifier.predict(img)
    value_argmax = np.argmax(value)
    return {'disease': li[value_argmax]}

# get_class('../ai_models/003a5321-0430-42dd-a38d-30ac4563f4ba___Com.G_TgS_FL 8121_180deg.jpeg')