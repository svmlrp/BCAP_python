import pandas as pd


def readUserAllocation(localpath):
    try:
        df=pd.read_csv(localpath)
        return df
    except Exception as e:
        print("The Exception in readUserAllocation Method:", e)
