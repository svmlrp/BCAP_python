import pandas as pd

def readSchedule(localpath):
    try:
        df=pd.read_csv(localpath)
        return df
    except Exception as e:
        print("The Exception in readSchedule Method:", e)
        return -1
#getPortRotation,getPortRotationindex
def getPort_index(df,col):
    portRotation=[]
    try:
        for row in df:
            portRotation.append(row[col])
        return sorted(portRotation)
    except Exception as e:
        print("The Exception in getPortRotation Method:", e)
        return -1

#getActivPortVoyage,getActivPortIndex
def getActivPortVoyage_index(df,col):
    ActiveportIndex = 1
    try:
        for i,row in df.iterrows():
            if row["currentport"]=="Y" or row["currentport"]=="y":
                ActiveportIndex=row[col]
                break
        return ActiveportIndex
    except Exception as e:
        print("The Exception in getActivPortVoyage_index Method:", e)
        return -1

#getportname,getPortCode
def getportname_code(df,col):
    portname={}
    try:
        for i,row in df.iterrows():
            portname[row["Portindex"]]=row[col]
        return portname
    except Exception as e:
        print("The Exception in getportname_code Method:", e)
        return -1





