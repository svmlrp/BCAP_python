import pandas as pd

def readTankData(localpath):
    try:

        df=pd.read_csv(localpath)
        return df
    except Exception as e:
        print("The Exception in readTankData Method:", e)
        return -1

def getWeightConstantLMOM(df,polIndex):
    sumWCMOM = 0
    try:
        for i,row in df.iterrows():
            if row["POLIndex"]==polIndex:
                sumWCMOM+=row["weight"]*row["lcglpp"]
        return sumWCMOM
    except Exception as e:
        print("The Exception in getWeightConstantLMOM Method:", e)
        return -1

def getWeightConstantWeight(df,polIdx):
    sumWCWt = 0
    try:
        for row in df:
            if row["portindex"]==polIdx:
                sumWCWt+=row["weight"]
        return sumWCWt
    except Exception as e:
        print("The Exception in getWeightConstantWeight Method:", e)
        return -1

def getWCTankList(df,polIdx):
    data=[]
    try:
        for i, row in df.iterrows():
            if row["tankcategory"] !="WC" and row["POLIndex"] == polIdx:
                data.append(row["tankname"])
        return data
    except Exception as e:
        print("The Exception in getWCTankList Method:", e)
        return -1





