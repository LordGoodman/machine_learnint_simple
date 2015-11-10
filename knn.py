from numpy import *
import operator

def creatDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

def classify0(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffmat.sum(axis=1)
    distance = sqDistances**0.5
    sprtedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = label[sortedDistindicies[i]]
        classCount[voteIlabel] =classCount.get(voteIlabel,0) +1
    sortedClassCount = sorted(classCount.iteritems(),key=operate.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]    
    
    
group,labels = creatDataSet()
