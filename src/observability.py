
import pandas
import os
import utility as utility

from sklearn.linear_model import LinearRegression

def getSizing(df):


    ObsMemoryWSSinGB = calculateMemorySizing(df)
    ObsCPUvCore = calculateCPUSizing(df)

    WorkerCPUvCore = ObsCPUvCore
    MasterCPUvCore = 0
    
    WorkerMemoryWSSinGB = ObsMemoryWSSinGB
    MasterMemoryWSSinGB = 0

    print("")
    print('ObsCPUvCore:',ObsCPUvCore)
    print('ObsMemoryWSSinGB:',ObsMemoryWSSinGB)
    print("")


    #return ObsCPUvCore , ObsMemoryWSSinGB
    return WorkerCPUvCore , WorkerMemoryWSSinGB, MasterCPUvCore, MasterMemoryWSSinGB

def calculateMemorySizing(df):
    print('\nCalculating the sizing based on the input data .......')

    number_of_managed_clusters = df.targetManagedClusters[0] 
    number_of_time_series_per_cluster = df. numberOfTimeSeriesPerCluster[0]

    master_df = utility.getReferenceData()

    print("Total Time Series count: ",number_of_managed_clusters*number_of_time_series_per_cluster)
    print("------------------------------------")
    X = master_df['TimeSeriesCount'].values.reshape(-1,1)
    Y = master_df['ACMObsMemUsageWSSGB'].values.reshape(-1,1)

    regressor = LinearRegression()  
    #training the algorithm
    regressor.fit(X,Y) 
    #To retrieve the intercept:
    alpha = regressor.intercept_
    print(f'alpha = {alpha}')
    #For retrieving the slope:
    beta = regressor.coef_
    print(f'beta = {beta}')

    y_pred = alpha + beta*number_of_managed_clusters*number_of_time_series_per_cluster
    print(f'A rough Predicted Memory need in GB for {number_of_managed_clusters*number_of_time_series_per_cluster} timeseries - IFF linearity holds = {y_pred} GB')

    print(float(y_pred))

    return float(y_pred)

def calculateCPUSizing(df):

    number_of_managed_clusters = df.targetManagedClusters[0] 
    number_of_time_series_per_cluster = df. numberOfTimeSeriesPerCluster[0]

    master_df = utility.getReferenceData()
    print("Total Time Series count: ",number_of_managed_clusters*number_of_time_series_per_cluster)
    print("------------------------------------")
    X = master_df['TimeSeriesCount'].values.reshape(-1,1)
    Y = master_df['ACMObsCPUCoreUsage'].values.reshape(-1,1)

    regressor = LinearRegression()  
    #training the algorithm
    regressor.fit(X,Y) 
    #To retrieve the intercept:
    alpha = regressor.intercept_
    print(f'alpha = {alpha}')
    #For retrieving the slope:
    beta = regressor.coef_
    print(f'beta = {beta}')

    y_pred = alpha + beta*number_of_managed_clusters*number_of_time_series_per_cluster
    print(f'A rough Predicted CPU vCPU needed for {number_of_managed_clusters*number_of_time_series_per_cluster} timeseries - IFF linearity holds = {y_pred} vCPU')

    print(float(y_pred))

    return float(y_pred)

