# -*- coding: utf-8 -*-
import sys
sys.path.append('E:/MyCraft/Github/machine_learnint_simple/Bayes.py')
import Bayes
import numpy as np
import feedparser

def calMostFreq(vocabList,fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.items(),key=operator.itemgetter(1),reverse=True)
    return sortedFreq[:30]
    
def localWord(feed0,feed1):
   
    minLen = min(len(feed1['entries']),len(feed0['entries']))
    listOfPost = [];classVec = [];fullText = []
    for i in range(minLen):
        wordList = Bayes.textParse(feed1['entries'][i]['summary'])#数组从feed1开始
        listOfPost.append(wordList)
        fullText.extend(wordList)
        classVec.append(1)
        
        wordList = Bayes.textParse(feed0['entries'][i]['summary'])
        listOfPost.append(wordList)
        fullText.extend(wordList)
        classVec.append(0)
        
    vocabList = Bayes.creatVocabList(listOfPost)
    
    top30Words = calMostFreq(vocabList,fullText)
    
    for pairW in top30Words:
        if pairW in vocabList:vocabList.remove(pairW)
        
    trainingSet = range(2*minLen) ; dataSet = []
    
    for i in range(20):
        randIndex = int(np.random.uniform(len(trainingSet)))
        dataSet.append(randIndex)
        del(trainingSet[randIndex])
    
    trainMat = [];trainClass = []
    for docIndex in trainingSet:
        trainMat.append(Bayes.bagOfWords2Vec(vocabList,listOfPost[docIndex]))
        trainClass.append(classVec[docIndex])
                    
    p0V,p1V,pSpam = Bayes.trainNB0(np.array(trainMat),trainClass)
    
    errorCount = 0.0
    
    for docIndex in dataSet:
        dataMat = Bayes.bagOfWords2Vec(vocabList,listOfPost[docIndex])
        
        if Bayes.classifyNB(np.array(dataMat),p0V,p1V,pSpam) != classVec[docIndex]:
            errorCount += 1
   # print "the error rate is :",errorCount/float(len(dataSet))
    
    return vocabList,p0V,p1V        
            
            
    
ny = feedparser.parse("http://newyork.craigslist.org/stp/index.rss")
sf = feedparser.parse("http://sfbay.craigslist.org/stp/index.rss")

#vocabList,ny,sf = localWord(ny,sf)   
    
def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V = localWord(ny,sf)
    nyTop = []; sfTop = []
    for i in range(len(p0V)):
        if p0V[i] > -4.5 : nyTop.append((vocabList[i],p0V[i]))
        if p1V[i] > -4.5 : sfTop.append((vocabList[i],p1V[i]))
    
    sortedNy = sorted(nyTop,key=lambda pair:pair[1],reverse=True)
    print "NY******************************NY"
    for item in sortedNy:
        print item[0]
    
    
    sortedSf = sorted(sfTop,key=lambda pair:pair[1],reverse=True)
    print "SF******************************SF"
    for item in sortedSf:
        print item[0]
    
    
    
    
      
    
        
        
        
        
        
    
    
    
    
    
    
       
        
        
        
        
        
        
        
        
        
        
    
    
    
