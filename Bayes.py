# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def loadDataSet():
    postingList = [['my','dog','has','flea','problems','help','please'],
                   ['maybe','not','take','him','to','dog','stupid'],
                   ['my','dalmation','is','so','cute','I','love','him'],
                   ['stop','posting','stupid','worthless','garbage'],
                   ['mr','licks','ate','my','steak','how','to','stop','him'],
                   ['quit','buying','worthless','dog','food','stupid']]
    
    classVec = [0,1,0,1,0,1]
    
    return  postingList,classVec
    
def creatVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document) #不重复出现
    return list(vocabSet)
    
def setOfWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else :print ("the word : %s is not in the Vocabulary!")%word
    return returnVec
        
def trainNB0(trainMartix,trainCategory):
    numTrainDocs = len(trainMartix)
    numwords = len(trainMartix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    c0Num = np.zeros(numwords)
    c1Num = np.zeros(numwords)
    c0Denom = 0.0
    c1Denom = 0.0
    
    for i in range(numTrainDocs):
        if trainCategory[i] == 0:
            c0Num += trainMartix[i]
            c0Denom += sum(trainMartix[i])
        else:
            c1Num += trainMartix[i]
            c1Denom += sum(trainMartix[i])
            
    c0Vect = c0Num/c0Denom
    c1Vect = c1Num/c1Denom
    
    return c0Vect,c1Vect,pAbusive    
                
    
    
    
    
    
    
        
