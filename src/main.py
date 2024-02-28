
#import urllib3
import sys
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime
import matplotlib.pyplot as plt
import os
import pandas

import utility as utility
import policy as policy
import observability as observability
import search as search

#This global variable (dataframe) is used to store the calculated results
#from each of the pillars of ACM
initialDF = pandas.DataFrame(columns=['Domain', 'WorkerCPUvCore', 'WorkerMemoryWSSinGB', 'MasterCPUvCore', 'MasterMemoryWSSinGB'])

def main():
    print('\n Starting to calculate .......')
    #print(sys.modules)
    ref_df = utility.getReferenceData()
    print('\nReference data from Scale lab.......')
    print(ref_df)

    target_df= utility.getCustomerEnv()
    print('\nCustomer specifications - input to sizing calculations.......')
    print(target_df)
    proceed = validateInput(target_df)

    if proceed:
        print('\nProceeding with the calculation .......')
        PolicyCPUvCore , PolicyMemoryWSSinGB, MasterCPUvCore, MasterMemoryWSSinGB = policy.getSizing(target_df)
        aggregateResults('Policy', PolicyCPUvCore , PolicyMemoryWSSinGB, MasterCPUvCore, MasterMemoryWSSinGB)
        
        ObsCPUvCore , ObsMemoryWSSinGB, _ ,_ = observability.getSizing(target_df)
        aggregateResults('Observability', ObsCPUvCore , ObsMemoryWSSinGB, 0, 0)

        SearchCPUvCore , SearchMemoryWSSinGB, _ ,_ = search.getSizing(target_df)
        aggregateResults('Search', SearchCPUvCore , SearchMemoryWSSinGB, 0, 0)

        # TODO:        
        # we need to check if resulting etcd size is close to 6GB
        # we need to check if we need to add the consumption of non-ACM/KubeAPI/etcd resources 
        summarizeResults()



def validateInput(df):

    print('\nValidating the input data .......')


    if df.targetManagedClusters[0] <= 10:
        print("Since the Number of managed clusters is fairly low, ( ",df.targetManagedClusters[0] ," ) we advise to use the sizig of the bu-demo system")
        sys.exit(1)

    # 3000 managaed clusters * 5 policies per cluster = 15000
    elif df.targetManagedClusters[0]*df.numberOfPoliciesPerCluster[0] > 15000:
        print("Since the Number of managed clusters * number of policies is ( ",
              df.targetManagedClusters[0]*df.numberOfPoliciesPerCluster[0]," ) which is greater than 15,000, we advise to ask for manual sizing estimate")
        sys.exit(1)

    elif df.targetManagedClusters[0] > 3000:
        print("Since the Number of managed clusters is high, ( ",df.targetManagedClusters[0] ," ) we advise to ask for manual sizing estimate")
        sys.exit(1)    

    return True   

# Careful: This method is mutating a global variable!
def aggregateResults(Domain, WorkerCPUvCore, WorkerMemoryWSSinGB, MasterCPUvCore, MasterMemoryWSSinGB):

    print('Adding data for ', Domain,'.......')

    global initialDF

    # initialize list of lists
    data = [[Domain, WorkerCPUvCore, WorkerMemoryWSSinGB, MasterCPUvCore, MasterMemoryWSSinGB]]
    df = pandas.DataFrame(data, columns=['Domain', 'WorkerCPUvCore', 'WorkerMemoryWSSinGB', 'MasterCPUvCore', 'MasterMemoryWSSinGB'])
    initialDF = pandas.concat([initialDF, df], ignore_index=True)
    
    return

def summarizeResults():
    print('\nSummarizing the results ......')
    print('-------------------------------------------------------------')
    
    print('')
    print(initialDF)
    print('')
    
    initialDF['WorkerCPUvCore']=initialDF['WorkerCPUvCore'].astype(float)
    initialDF['WorkerMemoryWSSinGB']=initialDF['WorkerMemoryWSSinGB'].astype(float)
    initialDF['MasterCPUvCore']=initialDF['MasterCPUvCore'].astype(float)
    initialDF['MasterMemoryWSSinGB']=initialDF['MasterMemoryWSSinGB'].astype(float)
    #print(initialDF.describe())
    #print(initialDF.dtypes)

    print('Worker CPU vCore total: ',initialDF['WorkerCPUvCore'].sum())
    print('Worker Memory WSS in GB total: ',initialDF['WorkerMemoryWSSinGB'].sum())
    print('Master CPU vCore total: ',initialDF['MasterCPUvCore'].sum())
    print('Master Memory WSS in GB total: ',initialDF['MasterMemoryWSSinGB'].sum())
    print('-------------------------------------------------------------')


if __name__ == "__main__":
    main()