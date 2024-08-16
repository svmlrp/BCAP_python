import pandas as pd

def readTankMapping(localpath):
    df_TankMapping=pd.read_csv(localpath)
    return df_TankMapping
df=readTankMapping("C:/Users/deenadayalan.pu/Downloads/files/files/TankMapping.csv")
def getBallastTankMapping(tankmapping_list):
    tankMap = {}
    try:
        for index, row in tankmapping_list.iterrows():
            tankMap[row["Tank name "]] = row["Mapping Tank name"]
    except Exception as e:
        print("The Exception in getBallastTankMapping", e)
    return tankMap

df2=getBallastTankMapping(df)
print(df2)