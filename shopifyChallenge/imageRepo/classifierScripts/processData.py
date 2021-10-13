import pandas as pd
import os
import cv2
import numpy as np
import h5py
from constants import classMappingPath, classMappingIndexedPath, rawLabelSetPath, hotEncodedLabelSetPath, processedH5ImageDataPath, trainingImagesFolderPath

def processImages(size, verbose=False):
    index = 0
    imgList = []
    files = os.listdir(trainingImagesFolderPath)
    files.sort()
    for filename in files:
        if(index%100 == 0):
            pass
        img = cv2.imread(os.path.join(trainingImagesFolderPath, filename), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            img = cv2.resize(img, (size, size))
            img = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            imgList.append(img)

        if(verbose):
            print(index)
        index += 1
    h5f = h5py.File(processedH5ImageDataPath, 'w')
    h5f.create_dataset('dataset_1', data=imgList)
    h5f.close()

def indexLabelMapping():
    data = pd.read_csv(classMappingPath)
    indexRow = [i for i in range(data.shape[0])]
    data['index'] = indexRow
    print(data.head())
    data.to_csv(classMappingIndexedPath, index=False)

def hotEncodeLabelData(verbose=False):
    data = pd.read_csv(rawLabelSetPath)
    data = data[-500000 + 24111:]
    data = data[data['Confidence'] == 1]
    data = data[['ImageID', 'LabelName']]
    classes = pd.read_csv(classMappingIndexedPath)
    allowedClasses = set(classes['LabelName'])
    newRows = {}
    for index, dp in data.iterrows():
        if verbose:
            print(index)
        if(not dp['ImageID'] in newRows):
            newRows[dp['ImageID']] = [0 for i in range(data.shape[0])]

        if dp['LabelName'] in allowedClasses:
            newRows[dp['ImageID']][int(classes[classes['LabelName'] == dp['LabelName']]['index'])] = 1

    for k, v in newRows.items():
        newRows[k] = [''.join(map(str,v))]

    newData = pd.DataFrame.from_dict(newRows, orient='index', columns=['Labels'])
    newData['ImageID'] = newData.index
    newData = newData[['ImageID', 'Labels']]
    newData.to_csv(hotEncodedLabelSetPath, index=False)

#processImages(200)
#indexLabelMapping()
#hotEncodeLabelData()