import pandas as pd

def readexp_Hatch(localpath):
    try:
        df=pd.read_csv(f"{localpath}Hatchcover.csv")
        return df
    except Exception as e:
        print("The Exception in readexp_Hatch Method:", e)
#  getMaxDisplcament,getLBP,getHBottom,getFirsthatchDistfromAft,getLasthatchDistfromAft,getUDDraftMDegree,
def find_hatch_value(df,cols):
    output=0
    try:
        for i,row in df.iterrows():
            output=row[cols]
            break
        return output
    except Exception as e:
        print(f"The Exception in find_hatch_value{cols} Method:", e)
        return -1

#getUDDraftMConst
def polynomial_hatch(df,cols):
    output=[]
    try:
        for i,row in df.iterrows():
            output=row[cols]
            const=list(map(float, output.split(',')))
            break
        return const
    except Exception as e:
        print(f"The Exception in polynomial_hatch{cols} Method:", e)
        return -1