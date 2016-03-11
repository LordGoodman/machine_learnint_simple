import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


fig = plt.figure(figsize=(50,50),dpi = 100)

n = 60

X = np.array([i for i in range(-30,30)])
Y = np.random.uniform(-30,30,(n,1)) 



def update(frame):
    global X,Y
    xRandom = np.random.randint(-30,30)
    yRandom = np.random.normal(-30,30)
    Y[xRandom] = yRandom
    
    plt.clf()
   
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position(('data',0))
    ax.spines['left'].set_position(('data',0))
    
    plt.plot(X[:],Y[:],lw=1,c="red")
    
    
    #pplot.set_offsets()
    #pplot. plot(xRandom,yRandom,lw=0.5,c="red")
    
    
    return plt
    
animation = FuncAnimation(fig,update,interval=1)


plt.show()