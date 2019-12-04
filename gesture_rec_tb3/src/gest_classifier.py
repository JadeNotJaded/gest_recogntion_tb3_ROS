#!/usr/bin/env python
import cv2, time
# Import of keras model and hidden layers for our convolutional network
# from keras.models import Sequential
# from keras.layers.convolutional import Conv2D, MaxPooling2D
# from keras.layers import Dense, Flatten
from keras.models import load_model
import numpy as np
import os
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import freenect

#global variables
X_test = []  #used to store images
model = load_model("handrecognition_model.h5") #load hand_recognition model

#get image information from image_ir
def callback(msg):
    value = msg
    depthMap = numby.array([value]) #image that you have subscribed to
    img = cv2.imread(depthMap) # Reads image and returns np.array
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converts into the corret colorspace(GRAY)
    img = cv2.resize(img, (320, 120)) # Reduce image size so training can be faster
    X_test.append(img)
    X_test = np.array(X_test, dtype="uint8")
    X_test = X_test.reshape(len(X_test), 120, 320, 1)

#get prediction
def getPrediction(model, gray):
    predictions_array = model.predict(gray) #check this out 
    for i in range(0,1):
        return predict(predictions_array[i])
    
def predict(prediction):
    class_names = ["down", "palm", "l", "fist", "fist_moved", "thumb", "index", "ok", "palm_moved", "c"] 
    predicted_label = np.argmax(prediction)
    return (class_names[predicted_label])

if __name__ == "__main__":
    #init node
    rospy.init_node('gest_classifier')
    #subscribe to image_ir
    sub = rospy.Subscriber('/image_ir', String, callback) #get full path and type
    #get_prediciton
    prediction = getPrediction(model, X_test) #check this out
    #publish predicition
    pub = rospy.Publisher('/command', String, queue_size=10) #publish command 
    pub.publish(prediction)
    rospy.spin()