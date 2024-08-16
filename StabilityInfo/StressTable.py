import pandas as pd

def readSTable(localpath):
    df=pd.read_csv(localpath)
    return df