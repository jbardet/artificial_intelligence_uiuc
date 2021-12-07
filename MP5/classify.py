# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2018

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set
"""
import numpy as np

def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    length_training_set = len(train_set)
    W = np.array([0]*train_set[0])
    b = 0

    iter = 0
    while iter < max_iter :
        for i in range(length_training_set) :
            y_star = np.sum(np.multiply(W, train_set[i]))+b
            if ((y_star >= 0) and (train_labels[i] == False)) :
                W = W - learning_rate*train_set[i]
                b-=learning_rate
            elif ((y_star <= 0) and (train_labels[i] == True)) :
                W = W + learning_rate*train_set[i]
                b+=learning_rate
        iter+=1
    # return the trained weight and bias parameters
    return W,b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    W,b = trainPerceptron(train_set, train_labels, learning_rate, max_iter)
    length_dev_set =len(dev_set)
    dev_labels = []

    for i in range(length_dev_set) :
        sum_function = np.sum(np.multiply(W, dev_set[i])) + b
        if sum_function >= 0 :
            dev_labels.append(1)
        else :
            dev_labels.append(0)
    # Train perceptron model and return predicted labels of development set
    return dev_labels

def sigmoid(x):
    # TODO: Write your code here
    # return output of sigmoid function given input x
    return (1/(np.exp(-x)+1))

def trainLR(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    length_training_set = len(train_set)
    train_set_built=np.zeros([length_training_set, len(train_set[0])+1])
    for i in range(length_training_set) :
        train_set_built[i] = np.append(train_set[i],1)

    W = np.array([0]*train_set_built[0])

    iter = 0
    while iter < max_iter :
        derivative = 0

        for i in range(length_training_set) :
            f=sigmoid(np.dot(train_set_built[i],W))
            derivative += (np.multiply(np.transpose(train_set_built[i]),(f-train_labels[i])))

        if f!=train_labels[i] :
            W=W-(learning_rate*((1/length_training_set)*derivative))
        iter+=1
    # return the trained weight and bias parameters
    return (W[:-1],W[-1])

def classifyLR(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    W,b = trainLR(train_set, train_labels, learning_rate, max_iter)
    length_dev_set =len(dev_set)
    dev_labels = []

    for i in range(length_dev_set) :
        sum_function = sigmoid(np.sum(np.multiply(W , dev_set[i]))+b)

        if sum_function >= 0.5 :
            dev_labels.append(1)
        else :
            dev_labels.append(0)
    # Train LR model and return predicted labels of development set
    return dev_labels

def classifyEC(train_set, train_labels, dev_set, k):
    # Write your code here if you would like to attempt the extra credit
    return []
