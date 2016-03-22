
from numpy import *
from time import sleep
import matplotlib.pyplot as plt

def loadDataSet(fileName):
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat

def selectJrand(i,m):
    j=i #we want to select any J not equal to i
    while (j==i):
        j = int(random.uniform(0,m))
    return j

def clipAlpha(aj,H,L):
    if aj > H: 
        aj = H
    if L > aj:
        aj = L
    return aj

def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMatrix = mat(dataMatIn); labelMat = mat(classLabels).transpose()
    b = 0; m,n = shape(dataMatrix)
    alphas = mat(zeros((m,1)))
    iter = 0
    while (iter < maxIter):
        alphaPairsChanged = 0
        for i in range(m):
            fXi = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T)) + b
            Ei = fXi - float(labelMat[i])#if checks if an example violates KKT conditions
            if ((labelMat[i]*Ei < -toler) and (alphas[i] < C)) or ((labelMat[i]*Ei > toler) and (alphas[i] > 0)):
                j = selectJrand(i,m)
                fXj = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T)) + b
                Ej = fXj - float(labelMat[j])
                alphaIold = alphas[i].copy(); alphaJold = alphas[j].copy();
                if (labelMat[i] != labelMat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L==H: print "L==H"; continue
                eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >= 0: print "eta>=0"; continue
                alphas[j] -= labelMat[j]*(Ei - Ej)/eta
                alphas[j] = clipAlpha(alphas[j],H,L)
                if (abs(alphas[j] - alphaJold) < 0.00001): print "j not moving enough"; continue
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])#update i by the same amount as j
                                                                        #the update is in the oppostie direction
                b1 = b - Ei- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - Ej- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if (0 < alphas[i]) and (C > alphas[i]): b = b1
                elif (0 < alphas[j]) and (C > alphas[j]): b = b2
                else: b = (b1 + b2)/2.0
                alphaPairsChanged += 1
                print "iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
        if (alphaPairsChanged == 0): iter += 1
        else: iter = 0
        print "iteration number: %d" % iter
    return b,alphas


def calcWs(alphas,dataArr,classLabels):
    X = mat(dataArr);labelMat = mat(classLabels).transpose()
    m,n = shape(X)
    w = zeros((n,1))
    for i in range(m):
        w +=multiply(alphas[i]*labelMat[i],X[i,:].T)
    return w



class optStruct:
    def __init__(self,dataMatIn,classLabels,C,toler):
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = shape(dataMatIn)[0]
        self.alphas = mat(zeros((m,1)))
        self.b = 0
        self.eCache = mat(zeros((m,2)))
        
def calacEk(oS,k):
    fXk = float(multiply(oS.alphas[k],oS.labelMat[k])*(oS.dataMatIn*oS.dataMatIn[k,:].T)) + oS.b
    Ek = fXk -float(os.LabeMat[k])
    return Ek

def selectJ(i,oS,Ei):
    maxK = -1;maxDeltaE = 0;Ej = 0
    oS.eCache[i] = [1,Ei]
    validEcacheList = nonzeros(oS.eCache[:,0].A)[0]
    if len(validEcacbeList) >1:
        for k in validEcacheList:
            if k == i : continue
            Ek = calcEk(oS,k)
            deltaE = abs(Ei - Ek)
            if(deltaE > maxDeltaE):
                maxK = k;maxDeltaE = delTaE;Ej = Ek
        return maxK,Ej
    else :
        j = selectJrand(o,oS.m)
        Ej = calcEk(oS,j)
    return j,Ej


def updateEk(oS,k):
    Ek = calcEk(oS,k)
    oS.eCache[k] = [1,Ek]

def innerL(i,oS):
    Ei = calcEk(oS,i)
    if((oS.labelMat[i]*Ei < -oS.tol)and(oS.alphas[i] < oS.C)) or((oS.label[i]*Ei > oS.tol)and(oS.alphas[i]>0)):
        j,Ej = seletJ(i,oS,Ei)
        alphaIold = oS.alphas[i].copy();alphaJold = oS.alphas[j].copy()
        if(oS.labelMat[i] != oS.alphas[j]):
            L = max(0,oS.alphas[i]-oS.alphas[j])
            H = min(oS.C,oS.C+oS.alphas[i]-oS.alphas[j])
        else:
            L = max(0,oS.alphas[i]+oS.alphas[j]-oS.C)
            H = min(oS.C,oS.alphas[i]+oS.alphas[j])
        if L==C : print "L=H"; return 0
        eta = 2.0*oS.X[i,:]*oS.X[j,:]-oS.X[i,:]*oS.X[i,:].T-os.X[j,:]*os.X[j,:].T
        if eta >= 0:print "eta>=0";return 0
        oS.alphas[j] -= oS.labelMat[j]*(Ei-Ej)/eta
        oS.alphas[j] = clipAlpha(oS.alphas[j],H,L)
        updateEk(oS,j)
        
        if(abs(oS.alphas[j]-alphaJold)<0.00001):
            print "j not moving engouh";return 0
        oS.alphas[i] += oS.labelMat[j]*oS.labelMat[i]*(alphaJold-oS.alphas[j])
        updateEk(oS,i)
        b1 = oS.b-Ei-oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.alphas[i,:]*oS.alphas[i,:].T-labelMat[j]*(oS.alphas[j]-alphaJold)*oS.alphas[i,:]*oS.alphas[j,:].T
        b2 = oS.b-Ej-oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.alphas[i,:]*oS.alphas[j,:].T-labelMat[j]*(oS.alphas[j]-alphaJold)*oS.alphas[j,:]*oS.alphas[j,:].T            
        if (0<oS.alphas[i]) and (oS.C>oS.alphas[i]) : oS.b = b1
        elif (0<oS.alphas[j]) and (oS.C>oS.alphas[j]) : oS.b = b2
        else:  oS.b = (b1+b2)/2.0          
        return 1
    else: return 0


def smoP(dataMatIn,classLabels,C,toler,maxIterm,kTup=('lin',0)):
    oS = optStruct(mat(dataMatIn),mat(classLabels).transpose(),C,toler)
    iter = 0
    entireSet = True; alphaPairsChanged = 0
    while (iter < maxIterm) and (alphaPairsChanged)>0 or entireSet:
        alphaPairsChanged = 0
        if entireSet :
            for i in range(oS.m):
                alphaPairsChanged += innerL(i,oS)
            print "fullSet,iter:%d i:%d,pairs changed:%d"%(iter,i,alphaPairsChanged)
            iter += 1
        else:
            nonBoundIs = nonzero((oS.alphas.A>0) * (oS.alphas.A<C))
            for i in nonBoundIs:
                alphaPairsChanged += inner(oS,i)
                print "non-bound,iter: %d i:%d,pairs changed:%d"%(iter,i,alphaPairsChanged)
            iter += 1
        if entireSet:entireSet = False
        elif (alphaPairsChanged == 0):entireSet = True
        print "iteration number : %d" %iter
    return oS.b,oS.alphas     

def plotImage(dataMat,labelClass):
    dataArr = array(dataMat);classArr = array(labelClass)
    length = len(dataMat)
    fig = plt.figure(figsize=(10,10),dpi=100,facecolor="white")
    ax = fig.add_subplot(111)
    for i  in range(length):
        if classArr[i] == 1:
            ax.scatter(dataArr[i,0],dataArr[i,1],marker='s',c="red")
        else:
            ax.scatter(dataArr[i,0],dataArr[i,1],c="blue")
    #plt.xlim
    b = -3.7320;w0=0.784038;w1=-0.262341
    
    X = arange(-2,12,0.1)
    Y =(-b-w0*X)/w1
    
    
    ax.plot(X,Y,lw=0.5,c="black")
    ax.axis([-2,12,-8,6])    
    plt.show()
        
        
        


    