#!/home/wuyao/miniconda3/envs/wython/bin/python
import numpy as np
import scipy.io as io
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import json 
import os
import time as ti

with open("./vivi1.json","r") as f:
    vivi = json.load(f)


key =  vivi["key"]["name"]
dimension = vivi["key"]["dimension"]

figsize = vivi["viTimeCloud"]["figsize"]
[row, col] = vivi["viTimeCloud"]["plotRowCol"]
indexLoop = vivi["viTimeCloud"]['indexLoop']

epg2eps = vivi["key"]["epg2eps"]
[width, height] = vivi["base"]["meshsize"]

fontsize = vivi["base"]["fontsize"]
font=FontProperties(fname=vivi["base"]["fontPath"])

serialLength = vivi['base']["serialLength"]
path = vivi['base']["absolutePath"] + vivi['vtu2mat']["subDirectory"] + vivi["base"]["filePrefix"]
outPath = vivi["base"]["absolutePath"] + vivi["viTimeCloud"]["subDirectory"]
isExists = os.path.exists( outPath )
if not isExists:
    os.mkdir( outPath )

timeUnit = vivi["base"]["timeUnit"]
timeHigh = vivi["base"]["timeHigh"]
timeInterval = vivi["viTimeCloud"]["timeInterval"]
timeStart = vivi["viTimeCloud"]["timeStart"]
timeFlag = vivi["viTimeCloud"]["timeFlag"]
timeStrLength = vivi["viTimeCloud"]["timeStrLength"]

outFormat = vivi["base"]["outFormat"]
dpi = vivi["base"]["dpi"]

barMin = vivi["colorBar"]["barMin"]
barMinStr = vivi["colorBar"]["barMinStr"]
barLacation = vivi["colorBar"]["barLacation"]
vmin = vivi["colorBar"]["vmin"]
vmax = vivi["colorBar"]["vmax"]

axis = vivi["base"]["axis"]
override = vivi["base"]["override"]

if row == 1 :
    fig, ax = plt.subplots(row, col, figsize=figsize )
    for j in range(col):
        index = str( indexLoop[0] + j*indexLoop[1] ).zfill( serialLength )
        filename = path + index + "_" + key +".mat"
        data = io.loadmat( filename )
        cloud = np.asarray( data[key] ).flatten()
        if dimension != 1:
            cloud = cloud.reshape((int) ( len(cloud)/dimension ), dimension)
            newCloud = (cloud[:,0]**2 + cloud[:,1]**2 + cloud[:,2]**2 )**0.5
            cloud = newCloud
            
        if epg2eps == True:
            cloud = 1 - cloud

        cloud = np.flipud( cloud.reshape(width, height).T )
        h = ax[j].imshow( cloud - barMin, cmap=plt.cm.jet )

        if timeFlag == True:
            time =  round(timeInterval*j + timeStart, 3)
            title = str( time )
            ax[j].set_title( title + " " + timeUnit, y=timeHigh, fontsize=fontsize, font=font )
        ax[j].axis('off')
else:
    fig, ax = plt.subplots(row, col, figsize=figsize )
    for i in range(row):
        for j in range(col):
            index = str( i*indexLoop[1]*col + j*indexLoop[1] + indexLoop[0] ).zfill( serialLength )
            filename = path + index + "_" + key +".mat"
            data = io.loadmat( filename )
            cloud = np.asarray( data[key] ).flatten()
            if dimension != 1:
                cloud = cloud.reshape((int) ( len(cloud)/dimension ), dimension)
                newCloud = (cloud[:,0]**2 + cloud[:,1]**2 + cloud[:,2]**2 )**0.5
                cloud = newCloud
            
            if epg2eps == True:
                cloud = 1 - cloud

            cloud = np.flipud( cloud.reshape(width, height).T )
            h = ax[i,j].imshow( cloud - barMin, vmin=vmin, vmax=vmax, cmap=plt.cm.jet )

            if timeFlag == True:
                time =  round(timeInterval*(i*col + j) + timeStart, 3)
                title = str( time )
                if ( len(title) < timeStrLength ):
                    title += (timeStrLength - len(title))*'0'
                ax[i,j].set_title( title + " " + timeUnit, y=timeHigh, fontsize=fontsize, font=font )
            ax[i,j].axis( axis )
   

cbar_ax = fig.add_axes( barLacation )
cbar = plt.colorbar(h, cax=cbar_ax)
cbar_ax.set_title(barMinStr, fontsize=fontsize, font=font)
for item in cbar.ax.yaxis.get_ticklabels():
    item.set_font(font)

if epg2eps == True:
    key = "EP_S"

outfile = outPath + key + "." + outFormat
if override == False:
    isExists = os.path.exists( outfile )
    if isExists:
        outfile = outPath + key + "_" + str( (int) (ti.time()) ) + "." + outFormat

fig.canvas.set_window_title(outfile)
plt.savefig( outfile , dpi=dpi, bbox_inches = 'tight' )
plt.show()
print('done!')
print("The file has been written in \" " + outfile + " \"\n")
