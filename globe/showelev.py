import pandas as pd, math, struct, numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

RESOLUTION = 120

dataFiles = [
    { "name": "g10g", "latMin":0, "latMax":50, "lngMin":0, "lngMax":90, "elMin":-407, "elMax":8752, "columns":10800, "rows":6000 }
]

def readNumberFromFile(name,position):
    with open(name, "rb") as fh:
        buf = BytesIO(fh.read())
        buf.seek(position)
        val = struct.unpack("<H", buf.read(2))[0]
        fh.close()
        if val < 0: return 0
        return val

def fileIndex(lng,lat,fileEntry):
    column= math.floor(lng*RESOLUTION);
    row= math.floor(lat*RESOLUTION);
    rowIndex= row - fileEntry['latMin'] * RESOLUTION;
    columnIndex= column - fileEntry['lngMin'] * RESOLUTION;
    index= ((fileEntry['rows'] - rowIndex - 1) * fileEntry['columns'] + columnIndex) * 2;
    return index

def getElevation(lng, lat, findex):
    idx = fileIndex(lng, lat, dataFiles[findex]);
    val = readNumberFromFile(dataFiles[findex]['name'],idx)
    return val

val = getElevation(28.903099362154144,40.24157520289902,0)
print (val)
val = getElevation(40.26766536150578, 28.93888732350262,0)
print (val)
