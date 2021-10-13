import h5py
import numpy as np
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential, load_model
import pandas as pd
import cv2
import os
from constants import classMappingPath, classMappingIndexedPath, rawLabelSetPath, hotEncodedLabelSetPath, processedH5ImageDataPath, trainingImagesFolderPath

h = 200
w = 200
d = 1

modelPath = './models/model1_10000_literer'

def makeModel(ks, dr, bn, fm, de):
    model = Sequential()

    model.add(Conv2D(fm, kernel_size=(ks, ks), activation='relu', input_shape=(h, w, d)))
    model.add(MaxPool2D(pool_size=(2, 2)))
    if bn:
        model.add(BatchNormalization())
    model.add(Dropout(dr))

    model.add(Conv2D(filters=fm * 2, kernel_size=(ks, ks), padding='same', activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    if bn:
        model.add(BatchNormalization())
    model.add(Dropout(dr))

    model.add(Conv2D(filters=fm * 4, kernel_size=(ks, ks), padding='same', activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    if bn:
        model.add(BatchNormalization())
    model.add(Dropout(dr))

    model.add(Conv2D(filters=fm * 4, kernel_size=(ks, ks), padding='same', activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    if bn:
        model.add(BatchNormalization())
    model.add(Dropout(dr))

    model.add(Flatten())
    model.add(Dense(de))
    model.add(Dropout(dr))

    model.add(Dense(8, activation='sigmoid'))

    return model

def train(dataRange, useExisting=False, epochs=10, val_split=0.2):
    h5f = h5py.File(processedH5ImageDataPath, 'r')
    trd = h5f['dataset_1'][dataRange[0]:dataRange[1]]
    h5f.close()

    data = pd.read_csv(hotEncodedLabelSetPath, dtype=str)
    trl = [[int(y) for y in str(x)] for x in data['Labels'][dataRange[0]:dataRange[1]]]
    trd = np.array(trd)
    trd = np.array([x.reshape(200, 200, 1) for x in trd])

    trl = np.array(trl)
    if(useExisting):
        model = load_model(modelPath)
    else:
        model = makeModel(4, 0.2, 0, 32, 128)
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(trd, trl, validation_split=val_split, epochs=epochs, verbose=1)
    model.save(modelPath)

def predictionToEnglish(prediction, threshold=0.45):
    data = pd.read_csv(classMappingIndexedPath)
    classes = []
    for i in range(len(prediction)):
        if (prediction[i] > 0.45):
            classes.append(data['Word'][i])
    return classes

def classifyContent(img):
    testData = []
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (200, 200))
    img = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    testData.append(img)
    testData = np.array(testData)
    testData = np.array([x.reshape(200, 200, 1) for x in testData])

    model = load_model("models/model1_10000_literer")
    predictions = model.predict(testData)

    return predictionToEnglish(predictions[0])


#train((0,10000))

#img = cv2.imread(os.path.join('../../media/images/', '322868_1100-800x825.jpg'), cv2.IMREAD_UNCHANGED)
#print(classifyContent(img))
