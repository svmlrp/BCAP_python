import pandas as pd

def readFrameStation(localpath):
    df=pd.read_csv(localpath)
    return df
# df=readFrameStation("C:/Users/deenadayalan.pu/Downloads/files/files/Framestations.csv")

# optimized all function in single function
#getBMPortNegativeLimit,getBMPortPostiveLimit,getSFPortNegativeLimit,getSFPortPostiveLimit,
# getArea,getMOMIntertia,getBMNegativeData,getBMPositiveData,getSFNegativeData,getSFPositiveData

def frame_col(df,col1,col2):
    output={}
    try:
        for index,row in df.iterrows():
            output[row[col1]] = row[col2]
    except Exception as e:
        print(f"The Exception in frame_col {col1,col2} Method:", e)
    return output
# frame_col=frame_col(df,"Frame","limitHarbmsag")
# print(frame_col)
