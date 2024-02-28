

import pandas as pd
import utility
from sklearn.linear_model import LinearRegression


def getSizing(df):
    
    WorkerMemoryWSSinGB = calculateMemorySizing(df,'ACMOthMemUsageWSSGB')
    MasterMemoryWSSinGB = calculateMemorySizing(df,'KubeAPIMemUsageWSSGB')
    WorkerCPUvCore = calculateCPUSizing(df,'ACMOthCPUCoreUsage')
    MasterCPUvCore = calculateCPUSizing(df,'KubeAPICPUCoreUsage')

    print("")
    print('PolicyCPUvCPUCore:',WorkerCPUvCore)
    print('MasterCPUvCore:',MasterCPUvCore)
    print('PolicyMemoryWSSinGB:',WorkerMemoryWSSinGB)
    print('KubeAPIMemUsageWSSGB:',MasterMemoryWSSinGB)
    print("")

    return WorkerCPUvCore , WorkerMemoryWSSinGB, MasterCPUvCore, MasterMemoryWSSinGB

def calculateMemorySizing(df, metricName):
    print('\nCalculating the sizing based on the input data .......')

    targetManagedClusters = df.targetManagedClusters[0] 
    numberOfPoliciesPerCluster = df. numberOfPoliciesPerCluster[0]
    keyPolicyMetrics = targetManagedClusters * numberOfPoliciesPerCluster

    master_df = utility.getReferenceData()
    master_df['policyMetrics']=master_df['cluster-count']*5
    master_df['policyMetrics']=master_df['policyMetrics'].astype(float)

    #we need to find out the line which closest to the keyPolicyMetrics in the master_df['policyMetrics']
    print("------------------------------------")
    X = master_df['policyMetrics'].values.reshape(-1,1)
    Y = master_df[metricName].values.reshape(-1,1)

    regressor = LinearRegression()  
    #training the algorithm
    regressor.fit(X,Y) 
    #To retrieve the intercept:
    alpha = regressor.intercept_
    print(f'alpha = {alpha}')
    #For retrieving the slope:
    beta = regressor.coef_
    print(f'beta = {beta}')

    y_pred = alpha + beta*keyPolicyMetrics
    print(f'A rough Predicted Memory need for {metricName} in GB for {keyPolicyMetrics} cluster x PoliciesPerCluster - IFF linearity holds = {y_pred} GB')

    print(float(y_pred))

    return float(y_pred)

def calculateCPUSizing(df, metricName):
    print('\nCalculating the sizing based on the input data .......')

    targetManagedClusters = df.targetManagedClusters[0] 
    numberOfPoliciesPerCluster = df. numberOfPoliciesPerCluster[0]
    keyPolicyMetrics = targetManagedClusters * numberOfPoliciesPerCluster

    master_df = utility.getReferenceData()
    master_df['policyMetrics']=master_df['cluster-count']*5
    master_df['policyMetrics']=master_df['policyMetrics'].astype(float)

    #we need to find out the line which closest to the keyPolicyMetrics in the master_df['policyMetrics']
    print("------------------------------------")
    X = master_df['policyMetrics'].values.reshape(-1,1)
    Y = master_df[metricName].values.reshape(-1,1)

    regressor = LinearRegression()  
    #training the algorithm
    regressor.fit(X,Y) 
    #To retrieve the intercept:
    alpha = regressor.intercept_
    print(f'alpha = {alpha}')
    #For retrieving the slope:
    beta = regressor.coef_
    print(f'beta = {beta}')

    y_pred = alpha + beta*keyPolicyMetrics
    print(f'A rough CPU in vCPU need for {metricName} in vCPU for {keyPolicyMetrics} cluster x PoliciesPerCluster - IFF linearity holds = {y_pred} vCPU')

    print(float(y_pred))

    return float(y_pred)