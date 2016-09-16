#!/usr/bin/python
# -*- coding: utf-8 -*-
#*********************************************
#
# SVM_learning_spectra_selected
# Perform SVM machine learning on Raman maps.
# version: 20160916a
#
# By: Nicola Ferralis <feranick@hotmail.com>
#
#**********************************************

import matplotlib
if matplotlib.get_backend() == 'TkAgg':
    matplotlib.use('Agg')

import numpy as np
from sklearn import svm
from sklearn.externals import joblib
import matplotlib.pyplot as plt

#**********************************************
# Input/Output files
#**********************************************
sampleFile = "Sample.txt"
mapfile = "Dracken-7-tracky_map1_bs_fit2_selected.txt"
trainedData = "trained.pkl"

#**********************************************
# Spectra normalization conditions
#**********************************************
Ynorm = True
YnormTo = 10
YnormX = 534

#**********************************************
# Training algorithm
# Use either 'linear' or 'rbf'
#   ('rbf' for large number of features)
#**********************************************
kernel = 'rbf'

#**********************************************
# Other
#**********************************************
showProbPlot = True
showTrainingDataPlot = True

#**********************************************
# Open and process training data
#**********************************************
f = open(mapfile, 'r')
M = np.loadtxt(f, unpack =False)
f.close()
        
En = np.delete(np.array(M[0,:]),np.s_[0:1],0)
M = np.delete(M,np.s_[0:1],0)
Cl = ['{:.2f}'.format(x) for x in M[:,0]]
A = np.delete(M,np.s_[0:1],1)


if Ynorm == True:
    print('\n Normalizing spectral intensity to: ' + str(YnormTo) + '; En(' + str(YnormX) + ') = ' + str(En[YnormX]) + '\n')
    for i in range(0,A.shape[0]):
        A[i,:] = np.multiply(A[i,:], YnormTo/A[i,YnormX])


print(' Number of datapoints = ' + str(A.shape[0]))
print(' Size of each datapoints = ' + str(A.shape[1]))


#**********************************************
# Load trained files or retrain
#**********************************************
try:
    with open(trainedData):
        print(" Opening training data...")
        clf = joblib.load(trainedData)
except:
    print(' Retraining data...')
    clf = svm.SVC(kernel = kernel, C = 1.0, decision_function_shape = 'ovr', probability=True)
    clf.fit(A,Cl)
    Z= clf.decision_function(A)
    print(' Number of classes = ' + str(Z.shape[1]))
    joblib.dump(clf, trainedData)

#**********************************************
# Run prediction
#**********************************************
f = open(sampleFile, 'r')
R = np.loadtxt(f, unpack =True, usecols=range(1,2))
R = R.reshape(1,-1)
f.close()

print(R.shape)

if Ynorm == True:
    R[0,:] = np.multiply(R[0,:], YnormTo/R[0,YnormX])

print('\n Predicted value = ' + str(clf.predict(R)[0]) + '\n')
print(' Probabilities of this sample within each class: \n')

prob = clf.predict_proba(R)[0].tolist()
for i in range(0,clf.classes_.shape[0]):
    print(' ' + str(clf.classes_[i]) + ': ' + str(round(100*prob[i],2)) + '%')

################
# Plot results
################
if showProbPlot == True:
    print('\n Stand by: Plotting probabilities for each class...')
    plt.title("Probability density per class")
    for i in range(0, clf.classes_.shape[0]):
        plt.scatter(clf.classes_[i], round(100*prob[i],2), label='probability', c = 'red')
    plt.show()

if showTrainingDataPlot == True:
    print(' Stand by: Plotting each datapoint from the map...')
    if Ynorm ==True:
        plt.title("Normalized Training Data")
    else:
        plt.title("Training Data")
    for i in range(0,A.shape[0]):
        plt.plot(En, A[i,:], label='Training data')
        plt.plot(En, R[0,:], linewidth = 2, label='Sample data')
    plt.show()

