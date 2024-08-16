import pandas as pd

def readBallastDetail(localpath):
    df_BallastDetail=pd.read_csv(localpath)
    return df_BallastDetail
# df=readBallastDetail("C:/Users/deenadayalan.pu/Downloads/files/files/VesselBallestWt.csv")
def readBallastWt(df, cargoWeight):
    try:
        for index, row in df.iterrows():
            if row["cargowt"] >= cargoWeight:
                return row["Ballestwt"]
                break
    except Exception as e:
        print("The Exception in readBallastWt Method:", e)

# df2=readBallastWt(df,10000)
# print(df2)