

import json
import os
import pandas

def getReferenceData():
    
    current_dir = os.getcwd()

    # Construct the full path to the subdirectory
    name = os.path.join(current_dir, "..","images",'sizing_summary_based_on_max_run_08222023.csv')

    fname = os.path.join(name)
    master_df = pandas.read_csv(fname,index_col=0)

    return master_df

def getCustomerEnv():

    current_dir = os.getcwd()

    # Construct the full path to the subdirectory
    name = os.path.join(current_dir, "..","input",'spec.json')
    fname = os.path.join(name)
    data = json.load(open(fname))

    # we are foced to provide index as 0
    # not sure if this the best use of it
    df = pandas.DataFrame(data,index=[0])
    #print(df)
    return df