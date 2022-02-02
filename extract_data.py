import pandas as pd
import numpy as np

def extraction(filename):
    df = pd.read_excel(filename)
    employees = dict()
    data = df.to_numpy()
    m,n = data.shape
    for i in range(m):
        employees[data[i,0]] = {'Latitude' : data[i,1], 'Longitude' : data[i,2], 'Skill' : data[i,3], 'Level' : data[i,4] , 'WorkingStartTime' : data[i,5], 'WorkingEndTime' : data[i,6] }
    return employees