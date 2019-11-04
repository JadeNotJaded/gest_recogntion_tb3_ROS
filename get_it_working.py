#!/usr/bin/env python
import cv2, time
# Import of keras model and hidden layers for our convolutional network
# from keras.models import Sequential
# from keras.layers.convolutional import Conv2D, MaxPooling2D
# from keras.layers import Dense, Flatten
from keras.models import load_model
import numpy as np
import os
from PIL import Image
import glob
image_list = []

X_test = []

for filename in glob.glob('/home/robotics/catkin_ws/src/HandRecognition/project3/images/*.png'): #assuming png
    im=Image.open(filename)
    img = cv2.imread(filename)
    # Reads image and returns np.array
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    # Converts into the corret colorspace(GRAY)
    img = cv2.resize(img, (320, 120)) # Reduce image size so training can be faster
    X_test.append(img)
X_test = np.array(X_test, dtype="uint8")
X_test = X_test.reshape(len(X_test), 120, 320, 1)

def getPrediction(model, gray):
    # class_names = ["down", "palm", "l", "fist", "fist_moved", "thumb", "index", "ok", "palm_moved", "c"] 
    predictions_array = model.predict(gray)
    for i in range(0, 5):
        printPrediciton(predictions_array[i])
    

def printPrediciton(prediction):
    class_names = ["down", "palm", "l", "fist", "fist_moved", "thumb", "index", "ok", "palm_moved", "c"] 
    predicted_label = np.argmax(prediction)
    print(class_names[predicted_label])

model = load_model("handrecognition_model.h5")
getPrediction(model, X_test)
