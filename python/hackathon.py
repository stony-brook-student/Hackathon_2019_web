
import keras
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
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


default_img_size = 150

def loadData(prefix, names, classification):
    pixels = []
    for i in range(len(names)):
        im = Image.open(prefix + names[i])#.convert('L')
        pix = np.asarray(im)
        pixels.append(pix)
    df_temp = pd.DataFrame({'Name': names, 'Image': pixels})
    df_temp['Classification'] = classification
    return df_temp

def resize(original):
    length = len(original)
    pixels = np.zeros((length, default_img_size, default_img_size, 3), dtype=np.uint8)
    for i in range(length):
        pix = original[i]
        j, k, l = pix.shape
        resized = np.zeros((default_img_size, default_img_size, 3))
        resized[:j, :k, :l] = pix
        pixels[i] = resized
    return pixels

def main():
	# 路径前缀
	path_parasitized, path_uninfected = './cell_images/final_p/', './cell_images/final_u/'
	# 包含文件名的list
	files_parasitized = [f for f in listdir(path_parasitized) if isfile(join(path_parasitized, f))]
	files_uninfected = [f for f in listdir(path_uninfected) if isfile(join(path_uninfected, f))]
	if '.DS_Store' in files_parasitized:
	    files_parasitized.remove('.DS_Store')
	if '.DS_Store' in files_uninfected:
	    files_uninfected.remove('.DS_Store')
	print(len(files_parasitized), ' parasitized records\n', len(files_uninfected), ' uninfected records', sep='')

	df_parasitize = loadData(path_parasitized, files_parasitized, 1)
	df_uninfected = loadData(path_uninfected, files_uninfected, 0)	

	data = pd.concat([df_parasitize, df_uninfected])
	data = sklearn.utils.shuffle(data)
	data = data.reset_index(drop=True)

	total_data = data.shape[0]
	print('default_img_size: ', default_img_size, '\ntotal_data: ', total_data, sep='')	

	train_percentage = 0.75
	num_train_data = int(total_data * train_percentage)
	num_test_data = total_data - num_train_data
	
	data_train, data_test = data[:num_train_data], data[num_train_data:]
	X_train, y_train = data_train.Image.values, data_train.Classification.values
	X_test, y_test = data_test.Image.values, data_test.Classification.values

	print(X_train.shape, y_train.shape, X_test.shape, y_test.shape, sep='\n')

	X_train = resize(X_train)
	X_test = resize(X_test)
	print(X_train.shape, X_test.shape, sep='\n')

	y_train = y_train.astype(np.uint8)
	y_test = y_test.astype(np.uint8)

	print("Shape before one-hot encoding: ", y_train.shape, y_test.shape)
	y_train = np_utils.to_categorical(y_train, 2)
	y_test = np_utils.to_categorical(y_test, 2)
	print("Shape after one-hot encoding: ", y_train.shape, y_test.shape)

	batch_size, epoch = 1, 1

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

	opt = Adam(lr=1e-5, decay=1e-5)
	model.compile(optimizer=opt,
	              loss='categorical_crossentropy',
	              metrics=['accuracy'])

	bestAcc = -1

	best_path, load_old_model = 'bestmodel1.h5', True
	if os.path.exists(best_path) and load_old_model:
	    model.load_weights(best_path)
	    print('Loaded')

	save_path = 'bestmodel2.h5'

	for i in range(50):
	    print('Epoch:', i)
	    hist = model.fit(X_train, y_train, batch_size=batch_size, epochs=1, verbose=1, shuffle=True)
	    model_predicted = model.predict(X_test)
	    cm = confusion_matrix(y_test.argmax(axis=1), model_predicted.argmax(axis=1))
	    sns.heatmap(cm, annot=True, fmt="d")
	    plt.show()
	    acc = (cm[0][0] + cm[1][1]) / num_test_data
	    print('Test Accuracy:', acc)
	    if bestAcc < acc:
	        model.save_weights(save_path)


if __name__ == "__main__":
    main()


