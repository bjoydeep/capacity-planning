import pandas as pd
import utility
from sklearn.linear_model import LinearRegression


def getSizing(df):
    
    WorkerMemoryWSSinGB = calculateMemorySizing(df)
    MasterMemoryWSSinGB = 0
    WorkerCPUvCore = calculateCPUSizing(df)
    MasterCPUvCore = 0

    print("")
    print('SearchCPUvCPUCore:',WorkerCPUvCore)
    print('SearchMemoryWSSinGB:',WorkerMemoryWSSinGB)
    print("")

    return WorkerCPUvCore , WorkerMemoryWSSinGB, MasterCPUvCore, MasterMemoryWSSinGB

def calculateMemorySizing(df):
    print('\nCalculating the sizing based on the input data .......')

    targetManagedClusters = df.targetManagedClusters[0] 
    numberOfResourcesPerCluster = df. numberOfResourcesPerCluster[0]
    
    print("------------------------------------")
    # hard coding this till we bring in the new data
    y_pred = 10

    print(f'A rough Predicted Memory needed for {numberOfResourcesPerCluster} resources per cluster for {targetManagedClusters} clusters in GB - IFF linearity holds = {y_pred} GB')

    print(float(y_pred))


    return float(y_pred)

def calculateCPUSizing(df):
    print('\nCalculating the sizing based on the input data .......')

    targetManagedClusters = df.targetManagedClusters[0] 
    numberOfResourcesPerCluster = df. numberOfResourcesPerCluster[0]
    
    print("------------------------------------")
    # hard coding this till we bring in the new data
    y_pred = 5

    print(f'A rough CPU in vCPU needed for {numberOfResourcesPerCluster} resources per cluster for {targetManagedClusters} clusters in vCPU - IFF linearity holds = {y_pred} vCPU')

    print(float(y_pred))

    return float(y_pred)    