import pandas as pd

def readSFandBMFrameStation(localpath):
    df=pd.read_csv(f"{localpath}SFandBM.csv")
    return df
# df=readSFandBMFrameStation("C:/Users/deenadayalan.pu/Downloads/files/files/SFandBM.csv")
def is_numeric(input_str):
    try:
        # Attempt to parse the input string to a float
        float(input_str)
        return True
    except ValueError:
        return False
# getFrameStLCG,getFrameStDistAP,getFrameStationWtRatio
def get_LCG_DISTAP_WTRATIO(df,col1):
    output={}
    try:
        for index, row in df.iterrows():
            key = f"{row['ITEMS']} , {row['FRAMES']}"
            output[key] = row[col1]
    except Exception as e:
        print(f"The exception in get_LCG_DISTAP_WTRATIO {col1} method:", e)

    return output
# df2=get_LCG_DISTAP_WTRATIO(df,"LCG(from AP) in SFBMCalc")
# print(df2)

def getFrameStationItem(df):
    FmStItems={}
    try:
        for index, row in df.iterrows():
            frames = row['FRAMES']
            items = row['ITEMS']

            if frames in FmStItems:
                FmStItems[frames].append(items)
            else:
                FmStItems[frames] = [items]

    except Exception as e:
        print("The exception in getFrameStationItem method:", e)

    return FmStItems
# df2=getFrameStationItem(df)
# print(df2)
# getFwdDistFromAP,getAftDistFromAP
def getFwd_AFT_DistFromAP(df,col1):
    output={}
    try:
        for index, row in df.iterrows():
            if row["CATEGORY"]=="CARGO" and row["ITEMS"]:
                output[row["ITEMS"]] = row[col1]
    except Exception as e:
        print("The exception in getFwd_AFT_DistFromAP method:", e)

    return output

# df3=getFwd_AFT_DistFromAP(df,"Aft Dist from AP (m)")
# print(df3)

def getCargoHold(df):
    CargoHold=[]
    try:
        for index, row in df.iterrows():
            if row["CATEGORY"]=="CARGO" and row["ITEMS"]:
                if row["ITEMS"] not in CargoHold:
                    CargoHold.append(row["ITEMS"])
    except Exception as e:
        print("The exception in getCargoHold method:", e)

    return CargoHold


def read_aft_and_fwd_distance(localpath):
    try:
        df = pd.read_csv(localpath + "SFandBM.csv", dtype={'FRAMES': float})

        HoldDistance = {}
        HoldAftDist = {}
        HoldFwdDist = {}

        for index, row in df.iterrows():
            try:
                HoldAftDist[row['FRAMES']] = row['Aft Dist from AP (m)']
                HoldFwdDist[row['FRAMES']] = row['Fwd Dist from AP (m)']
            except Exception as e:
                print(f"Error processing row {index}: {e}")

        HoldDistance['HoldAftDist'] = HoldAftDist
        HoldDistance['HoldFwdDist'] = HoldFwdDist

        return HoldDistance

    except Exception as e:
        print("The exception in read_aft_and_fwd_distance method:", e)
        return {}