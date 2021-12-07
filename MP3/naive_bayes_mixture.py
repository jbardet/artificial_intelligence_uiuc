# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020

"""
This is the main entry point for Part 2 of this MP. You should only modify code
within this file for Part 2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


import numpy as numpy
import math
from collections import Counter
import nltk





def naiveBayesMixture(train_set, train_labels, dev_set, bigram_lambda,unigram_smoothing_parameter, bigram_smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    bigram_lambda - float between 0 and 1

    unigram_smoothing_parameter - Laplace smoothing parameter for unigram model (between 0 and 1)

    bigram_smoothing_parameter - Laplace smoothing parameter for bigram model (between 0 and 1)

    pos_prior - positive prior probability (between 0 and 1)
    """



    # TODO: Write your code here
    posit1 = Counter()
    negat1 = Counter()
    posit2 = Counter()
    negat2 = Counter()
    for movie in train_set :
        bigrams = list(nltk.bigrams(movie))
        if train_labels[train_set.index(movie)] :
            posit1 += Counter(movie)
            posit2 += Counter(bigrams)
        else :
            negat1 += Counter(movie)
            negat2 += Counter(bigrams)

    k1 = unigram_smoothing_parameter
    k2 = bigram_smoothing_parameter
    lbda = bigram_lambda

    result = []
    nb_posit1 = sum(posit1.values())
    nb_negat1 = sum(negat1.values())
    nb_posit2 = sum(posit2.values())
    nb_negat2 = sum(negat2.values())

    for movie in dev_set :
        proba_pos1 = 0
        proba_neg1 = 0
        proba_pos2 = 0
        proba_neg2 = 0
        bigrams = list(nltk.bigrams(movie))
    
        for word in movie :
            proba_pos1 += math.log((posit1[word]+k1)/(nb_posit1+k1*len(posit1)))
            proba_neg1 += math.log((negat1[word]+k1)/(nb_negat1+k1*len(negat1)))
        for biword in bigrams :
            proba_pos2 += math.log((posit2[biword]+k2)/(nb_posit2+k2*len(posit2)))
            proba_neg2 += math.log((negat2[biword]+k2)/(nb_negat2+k2*len(negat2)))
        proba_pos = (1-lbda) * (math.log(nb_posit1 / (nb_posit1 + nb_negat1)) + proba_pos1) + lbda * (math.log(nb_posit2 / (nb_posit2 + nb_negat2)) + proba_pos2)
        proba_neg = (1-lbda) * (math.log(nb_negat1 / (nb_posit1 + nb_negat1)) + proba_neg1) + lbda * (math.log(nb_negat2 / (nb_posit2 + nb_negat2)) + proba_neg2)

        if proba_pos > proba_neg :
            result.append(1)
        else :
            result.append(0)

    return result

    # return predicted labels of development set (make sure it's a list, not a numpy array or similar)
