# -*- coding: utf-8 -*-
from numpy import *
from os import listdir
import operator


def classify0(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distance = sqDistances**0.5
    sprtedDistIndicies = distance.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sprtedDistIndicies[i]]
        classCount[voteIlabel] =classCount.get(voteIlabel,0) +1
    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]    

def file2matrix(filename):
    fr = open(filename)
    arryOLines = fr.readlines()
    numberOfLines = len(arryOLines)
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arryOLines:
        line = line.strip()
        listFormLine = line.split('\t')
        returnMat[index,:] = listFormLine[0:3]
        classLabelVector.append(int(listFormLine[-1]))
        index +=1
    return returnMat,classLabelVector
    
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals
    
def datingCalssTest(filePath):
    hoRatio =0.1
    datingDataMat,datingLabels = file2matrix(filePath)
    normMat,ranges,minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d,the real answer is :%d"%(classifierResult,datingLabels[i])
        if(classifierResult != datingLabels[i]):errorCount +=1.0
    print "the total error rate is :%f"%(errorCount/float(numTestVecs))

def classifyPerson(path):
    resultList = ['not at all','in small does','in large does']
    percentTats = float(raw_input("percentage of time spent playing vedio game?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat,datingLabels = file2matrix(path)
    normMat,ranges,minVal = autoNorm(datingDataMat)
    inArr = array([ffMiles,percentTats,iceCream])
    classifierResult = classify0((inArr-minVal)/ranges,normMat,datingLabels,3) #此处返回1 or 2 or 3
    print "you will probably like this person:",resultList[classifierResult - 1]

def image2vector(filename):
        returnVector = zeros((1,1024))
        fr = open(filename)
        for i in range(32):
            line = fr.readline()
            for j in range(32):
                returnVector[0,i*32+j] = line[j]
        return returnVector

def handwritingClassText(dirPath):
    hwLabels = []
    trainingFileList = listdir(dirPath+"/"+"trainingDigits")
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split(".")[0]
        classNumStr = int(fileStr.split("_")[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = image2vector(dirPath+"/"+"trainingDigits"+"/"+fileNameStr)
    testFileList = listdir(dirPath + "/"+"testDigits")
    errorCount = 0.0
    mTest = len(testFileList)
    
    
    for j in range(mTest):
        testFileNameStr = testFileList[j]
        testFileStr = testFileNameStr.split(".")[0]
        classTestNumstr = int(testFileStr.split("_")[0])
        testMat = image2vector(dirPath+"/"+"testDigits"+"/"+testFileNameStr)
        classifierResult = classify0(testMat,trainingMat,hwLabels,5)
       # print("the classifier came back with:%d ,the real answer is:%d"%(classifierResult,classTestNumstr))
        if(classifierResult != classTestNumstr):errorCount += 1
    print("the total number of errors is:%d"%errorCount)
    print("the total error rate is:%f"%(errorCount/mTest))
        
        
        
        
        
        
         
        
        