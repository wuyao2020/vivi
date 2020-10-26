#!/home/wuyao/miniconda3/envs/wython/bin/python
import numpy as np
import scipy.io as io
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import json 
import os

with open("./vivi1.json","r") as f:
    vivi = json.load(f)

key =  vivi["key"]["name"]
dimension = vivi["key"]["dimension"]

figsize = vivi["viCloud"]["figsize"]
indexLoop = vivi["viCloud"]['indexLoop']

epg2eps = vivi["key"]["epg2eps"]
[width, height] = vivi["base"]["meshsize"]

fontsize = vivi["base"]["fontsize"]
font=FontProperties(fname=vivi["base"]["fontPath"])

serialLength = vivi['base']["serialLength"]
path = vivi['base']["absolutePath"] + vivi['vtu2mat']["subDirectory"] + vivi["base"]["filePrefix"]
outPath = vivi["base"]["absolutePath"] + vivi["viCloud"]["subDirectory"] + key  + "/"
isExists = os.path.exists( outPath )
if not isExists:
    os.mkdir( outPath )

timeUnit = vivi["base"]["timeUnit"]
timeHigh = vivi["base"]["timeHigh"]
timeInterval = vivi["viCloud"]["timeInterval"]
timeStart = vivi["viCloud"]["timeStart"]
timeFlag = vivi["viCloud"]["timeFlag"]
timeStrLength = vivi["viCloud"]["timeStrLength"]

outFormat = vivi["base"]["outFormat"]
dpi = vivi["base"]["dpi"]

barMin = vivi["colorBar"]["barMin"]
barMinStr = vivi["colorBar"]["barMinStr"]
barLacation = vivi["colorBar"]["barLacation"]
vmin = vivi["colorBar"]["vmin"]
vmax = vivi["colorBar"]["vmax"]

axis = vivi["base"]["axis"]
override = vivi["base"]["override"]


begin = indexLoop[0]
end = indexLoop[2]
num = (int) ( ( end - begin )/indexLoop[1] ) + 1
loopList = np.linspace( begin, end, num, dtype=np.int)

for i in loopList:
    fig, ax = plt.subplots( figsize=figsize )

    index = str( i ).zfill( serialLength )
    filename = path + index + "_" + key + ".mat"
    data = io.loadmat( filename )
    cloud = np.asarray( data[key] ).flatten()

    if dimension != 1:
        cloud = cloud.reshape((int) ( len(cloud)/dimension ), dimension)
        newCloud = (cloud[:,0]**2 + cloud[:,1]**2 + cloud[:,2]**2 )**0.5
        cloud = newCloud
            
    if epg2eps == True:
        cloud = 1 - cloud

    cloud = np.flipud( cloud.reshape(width, height).T )
    h = ax.imshow( cloud - barMin, vmin=vmin, vmax=vmax, cmap=plt.cm.jet )
    
    if timeFlag == True:
        time =  round( timeInterval*i/indexLoop[1], 3)
        title = str( time )
        if ( len(title) < timeStrLength ):
            title += (timeStrLength - len(title))*'0'
        ax.set_title( title + " " + timeUnit, y=timeHigh, fontsize=fontsize, font=font )
    ax.axis(axis)
    plt.colorbar(h)
    plt.savefig(outPath + key + index + "." + outFormat , dpi=dpi, bbox_inches = 'tight')
    print("The file has been written in \" " + outPath + key + index + "." + outFormat + " \" ")
    plt.close()


print('done!')

