#!/home/wuyao/miniconda3/envs/wython/bin/python
"""
函数功能：将mfix生成的vtu格式文件，指定的物理量导出为mat格式

@author: wuyao
@date: 2020/10/23

----------  函数参数  ----------
filename: 一个字符串，要处理vtu文件的绝对地址
keys: 一个字符串列表，字符串为要输出的参数，默认值为
    ["EP_G","P_G", "Gas_Velocity", "Solids_Velocity_1"]，
    即气体体积份额、气体压力、气体速度和固相1的速度


----------  输出返回 ------------
返回值为本次处理消耗的时间，单位s
输出文件为输入文件同名，位置也在同一目录下


---------- 使用备注 ----------
1. 当有大量数据需要导出时，比如多个时间步长的文件，请使用脚本调用本文件
2. keys参数指定为整数“51”时，可导出全部变量为mat，但不必要时请不要这么做
3. 导出的文件您可以通过matlab进一步处理，当您没有matlab授权时可以使用octave、sklearn(python)等工具

"""

import vtk
import numpy as np
import time
import os
import scipy.io as io
import json



def vtu2mat(filename, outPath, keys = ["EP_G","P_G", "Gas_Velocity", "Solids_Velocity_1"]):

    tic = time.time()

    # get name of outfile
    filePath, tempfileName = os.path.split(filename)
    truefileName, extension = os.path.splitext(tempfileName)
    del extension, filePath
    outfileName = outPath + truefileName 


    # Read the source file.
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update() 
    
    # read cellData
    odb = reader.GetOutputDataObject(0)
    cellData = odb.GetCellData()

    # loop for keys
    for key in keys:
        data = cellData.GetArray( key )

        length = data.GetDataSize()

        out = np.zeros( length )

        for i in range(length):
            out[i] = data.GetValue( i )

        io.savemat( outfileName+"_"+key+".mat", {key:out})
                                                  

    toc = time.time()
    return toc - tic


if __name__ == '__main__':
    timeCost = 0

    with open("./vivi1.json","r") as f:
        vivi = json.load(f)

    path = vivi["base"]["absolutePath"] + vivi["base"]["filePrefix"]
    
    outPath = vivi["base"]["absolutePath"] + vivi["vtu2mat"]["subDirectory"]
    isExists = os.path.exists( outPath )
    if not isExists:
        os.mkdir( outPath )

    serialLength = vivi["base"]["serialLength"]
    indexLoop = vivi['vtu2mat']['indexLoop']
    keys = vivi['vtu2mat']['keyLoop']

    loopTimes = (int) ( ( indexLoop[2] - indexLoop[0] )/indexLoop[1] ) + 1
    for i in range(loopTimes):
        index = str( indexLoop[0] + i*indexLoop[1] ).zfill( serialLength )
        filename = path + index + ".vtu"
        timeCost += vtu2mat( filename, outPath, keys )

    print("time cost : ", timeCost, " s")
    print("The file has been written in \" " + outPath + " \"\n")


    






