import pandas as pd, math
import numpy as np
import matplotlib.pyplot as plt

dataFiles = [
    { "name": "g10g", "latMin":0, "latMax":50, "lngMin":0, "lngMax":90, "elMin":-407, "elMax":8752, "columns":10800, "rows":6000 }
]
    
def fileIndex(lng,lat,fileEntry, resolution):
    column= math.floor(lng*resolution);


fileIndex(28.903099362154144,40.24157520289902,dataFiles[0],120);
