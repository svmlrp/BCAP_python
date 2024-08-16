import pandas as pd

def readTankPostion(localpath):
    df_TankPostion=pd.read_csv(localpath)
    return df_TankPostion

def getHoldBallastTankList(df, holdno):
    tankList = []
    try:
        filter_df = df[df["Hold No."] == holdno]
        tankList.append(filter_df["Tank Name"].iloc[0])
    except Exception as e:
        print("The Exception in getHoldBallastTankList", e)
    return tankList
