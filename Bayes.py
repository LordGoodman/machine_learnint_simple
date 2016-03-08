# -*- coding: utf-8 -*-
import numpy as np


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

def bagOfWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
     #   else :print ("the word : %s is not in the Vocabulary!")%word
    return returnVec

def trainNB0(trainMartix,trainCategory):
    numTrainDocs = len(trainMartix)
    numwords = len(trainMartix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    c0Num = np.ones(numwords)
    c1Num = np.ones(numwords)
    c0Denom = 2.0
    c1Denom = 2.0
    
    for i in range(numTrainDocs):
        if trainCategory[i] == 0:
            c0Num += trainMartix[i]
            c0Denom += sum(trainMartix[i])
        else:
            c1Num += trainMartix[i]
            c1Denom += sum(trainMartix[i])
            
    c0Vect = np.log(c0Num/c0Denom)
    c1Vect = np.log(c1Num/c1Denom)
    
    return c0Vect,c1Vect,pAbusive    
                
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
     p0 = sum(vec2Classify*p0Vec) + np.log(1.0-pClass1)
     p1 = sum(vec2Classify*p1Vec) + np.log(pClass1)
     if p1>p0:
         return 1
     else:
         return 0
         
def testNB():
    listOfPosts,classVec = loadDataSet()
    vocabList = creatVocabList(listOfPosts)
    trainMat = []
    for postInDoc in listOfPosts:
        trainMat.append(setOfWords2Vec(vocabList,postInDoc))
    p0vec,p1vec,pAbusive =  trainNB0(trainMat,classVec)
    
    testEntry = ['love','my','dalmation']
    thisDoc = np.array(setOfWords2Vec(vocabList,testEntry)) #统一classify参数格式
   # print thisDoc
    print testEntry,'classify as :',classifyNB(thisDoc,p0vec,p1vec,pAbusive)
    print '---------------------------------------'
    testEntry = ['stupid','garbage','dalmation','cute','love','my']
    thisDoc = np.array(setOfWords2Vec(vocabList,testEntry)) #统一classify参数格式
    #print thisDoc
    print testEntry,'classify as :',classifyNB(thisDoc,p0vec,p1vec,pAbusive)

#emailText = open('E:/MyCraft/machinelearninginaction/Ch04/email/ham/6.txt').read()
#listOfTokens = regEx.split(emailText)  for testing

def textParse(bigString):
    import re
    regEx = re.compile('\\W*')
    listOfTokens = regEx.split(bigString)
    return [tok.lower() for tok in listOfTokens if len(tok)>2]


def spamtext():
    docList = []; classList = []; fullText = []
    for i in range(1,26):
        wordList = textParse(open("E:/MyCraft/machinelearninginaction/Ch04/email/spam/%d.txt"%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        
        wordList = textParse(open("E:/MyCraft/machinelearninginaction/Ch04/email/ham/%d.txt"%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
        
        vocabList = creatVocabList(docList)
        
        trainingSet = range(50);testSet = []
       
    for i in range(10):
            randIndex = int(np.random.uniform(0,len(trainingSet)))
            testSet.append(trainingSet[randIndex])
            del(trainingSet[randIndex])
    trainMat = [];trainclass = []
        
    for doctIndex in trainingSet:
            trainMat.append(setOfWords2Vec(vocabList,docList[doctIndex]))
            trainclass.append(classList[doctIndex])

    p0V,p1V,pSpam = trainNB0(np.array(trainMat),np.array(classList))
    errorCount = 0
    for testIndex in testSet:
        test = setOfWords2Vec(vocabList,docList[testIndex])
        p=classifyNB(np.array(test),p0V,p1V,pSpam)
        if p !=classList[testIndex]:
                errorCount += 1
                print docList[testIndex],"has been classificated wrongly"
    print "error rate is :",float(errorCount)/len(testSet)
        
        
            
        
        
        
        
        
        
    
    
    
    
    
