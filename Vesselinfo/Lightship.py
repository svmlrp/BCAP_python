import pandas as pd

def readLightShip(localpath):
    df_LightShip=pd.read_csv(f"{localpath}Lightship.csv")
    return df_LightShip

def getLightShipLMOM(df):
    lightshipLMOM=0
    try:
        for index, row in df.iterrows():
            lightshipLMOM+=df["WEIGHT"] * df["LCG (AP)"]
    except Exception as e:
        print("The Exception in getLightShipLMOM Method:", e)
    return lightshipLMOM.iloc[0]

def getLightshipweight(df):
    lightshipWt=0
    try:
        for index, row in df.iterrows():
            lightshipWt += df["WEIGHT"]
    except Exception as e:
        print("The Exception in getLightshipweight Method:", e)
    return lightshipWt.iloc[0]
