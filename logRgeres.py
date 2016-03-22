# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

#def loadDataSet(path):
#    dataMat =[]; labelMat = []
    #fr = open("E:/MyCraft/machinelearninginaction/Ch05/testSet.txt")
#    fr = open(path)
#    for line in fr.readlines():
#        linArr = line.strip().split()
        #print linArr[0]
#        dataMat.append([1,float(linArr[0]),float(linArr[1])])
#        labelMat.append(int(linArr[2]))
#    return dataMat,labelMat

def loadDataSet(path):
    dataMat =[]; labelMat = []
    #fr = open("E:/MyCraft/machinelearninginaction/Ch05/testSet.txt")
    fr = open(path)
    for line in fr.readlines():
        linArr = line.strip().split()
        #print linArr[0]
        dataMat.append([float(data) for data in linArr[:-1]])
        labelMat.append(float(linArr[-1]))
    return dataMat,labelMat
    
def sigmoid(inX):
    return 1.0/(1+np.exp(-inX))
    
    
def gardAscent(dataMatIn,classLabels):
    dataMatrix = np.mat(dataMatIn)
    labelMat = np.mat(classLabels).transpose()
    
    m,n = np.shape(dataMatrix)
    alpha = 0.001
    weights = np.ones((n,1))
    maxCycles = 500
    
    for k in range(maxCycles):
        h = sigmoid(dataMatrix*weights)
        error = labelMat - h
        weights = weights + alpha * dataMatrix.transpose() * error #here some questions must figure it out ,why should I used the trasposed matrix
    
    return np.array(weights)   
        
            
def plotBestFit(dataMat,labelsMat,weights):
     
    # dataMat,labelsMat = loadDataSet()
     dataArr = np.array(dataMat)
     n = np.shape(dataArr)[0]
     xcord1 = [] ; ycord1 = []
     xcord2 = [] ; ycord2 = []
     
     for i in range(n):
         if labelsMat[i] == 0:
             xcord1.append(dataArr[i][1]);ycord1.append(dataArr[i][2])
         else :
             xcord2.append(dataArr[i][1]);ycord2.append(dataArr[i][2])
             
     fig = plt.figure()
     ax = fig.add_subplot(111)
     ax.scatter(xcord1,ycord1,s=30,c='green',marker='s')
     ax.scatter(xcord2,ycord2,s=30,c='red',marker='>')
     
     x = np.arange(-3,3,0.1)
     y = np.array((-weights[1]*x-weights[0])/weights[2])
     
     ax.plot(x,y)
     
     plt.xlabel("X1");plt.ylabel("X2")
     
     plt.show()  
    
def stocGradAscent0(dataMatIn,classLabel):
#    dataMatrix = np.mat(dataMatIn)
    dataMatrix = np.array(dataMatIn)
    m,n = np.shape(dataMatrix)
    weights = np.ones(n)
    alpha = 0.01
    
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i] * weights))
        error = classLabel[i] - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights
    
        
def stocGradAscent1(dataMatIn,classLabel,numIter=500):
    dataMatrix = np.array(dataMatIn)
    m,n = np.shape(dataMatrix)
    weights = np.ones(n)
    for i in range(numIter):   
        dataIndex = range(m)
        for j in dataIndex:
            alpha = 4/(1.0+i+j) + 0.01
           # print j
            randIndex = int(np.random.uniform(len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex] * weights))
            error = classLabel[randIndex] - h
            weights = weights + alpha * error *dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights
            
     
     
     
def classify():
    trainMatrix,trainClass = loadDataSet('E:/MyCraft/machinelearninginaction/Ch05/horseColicTraining.txt')
    testMatrix,testClass = loadDataSet('E:/MyCraft/machinelearninginaction/Ch05/horseColicTraining.txt')
    #return trainMatrix,trainClass
    weights =  stocGradAscent1(trainMatrix,trainClass)
   # plotBestFit(trainMatrix,trainClass,weights)
    
    results = []
    for i in range(len(testMatrix)):
        if sigmoid(sum(testMatrix[i] * np.array(weights))) > 0.5:
            results.append(1)
        else :
            results.append(0)
    
    errorCount = 0.0
    
    for error in (testClass - np.array(results)):                
      if error != 0 : #不等于零就是不相等
          errorCount += 1.0
    
    print "error rate is :",errorCount/len(testMatrix)
    
    
    
        
                
