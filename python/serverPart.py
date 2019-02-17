
from google.cloud import storage

import keras
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pprint
import seaborn as sns
import sklearn.utils
import tensorflow as tf
from keras.layers import Conv2D, Activation, Dense, MaxPooling2D, Flatten, Dropout
from keras.models import Sequential
from keras.optimizers import Adam
from keras.utils import np_utils
from os import listdir
from os.path import isfile, join
from PIL import Image
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score


def img_to_nparray(path: str):
    min_size, max_size = 120, 150
    im = Image.open(path)
    pix = np.asarray(im)
    row, col, rgb = pix.shape
    if min_size < row < max_size and min_size < col < max_size:
        b = np.zeros((max_size, max_size, 3), dtype=np.uint8)
        b[:row, :col, :rgb] = pix
        return b
    return None


def get_result(array):
    optimizer, loss, metric = Adam(lr=1e-5, decay=1e-5), 'categorical_crossentropy', ['accuracy']
    batch_size, model_path = 1, 'bestmodel2.h5'
    default_img_size = 150
    model = Sequential([
        Conv2D(32, (5, 5), input_shape=(default_img_size,default_img_size, 3), activation='relu'),
        MaxPooling2D(pool_size=(3, 3)),
        Conv2D(32, (5, 5), activation='relu'),
        MaxPooling2D(pool_size=(3, 3)),
        Conv2D(64, (5, 5), activation='relu'),
        MaxPooling2D(pool_size=(3, 3)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.45),
        Dense(2, activation='softmax')
    ])
    model.compile(optimizer=optimizer, loss=loss, metrics=metric)
    model.load_weights(model_path)
    temp = np.zeros((1, default_img_size, default_img_size, 3), dtype=np.uint8)
    temp[0] = array
    pred = model.predict(temp, batch_size=batch_size)
    pred = pred.argmax(axis=1)[0]
    if pred == 0:
        return "Uninfected"
    return "Infected"


