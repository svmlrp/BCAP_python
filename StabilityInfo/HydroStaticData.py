import pandas as pd

def readHydroStatic(localpath):
    df=pd.read_csv(f"{localpath}Hydrostatic_Data.csv")
    return df
# df=readHydroStatic("C:/Users/deenadayalan.pu/Downloads/files/files/Hydrostatic_Data.csv")
def do_linear_interpolation(idiff, df1_val, df2_val, reqdiff):
    return df1_val + (df2_val - df1_val) * reqdiff / idiff

def getStatbilityinfo(trim, draft_mean, df):
    # print("trim, draft_mean, df",trim, draft_mean, df)
    try:
        lstrims = sorted(df['Trim'].unique())
        mintrim = max(filter(lambda i: i <= trim, lstrims), default=None)
        maxtrim = min(filter(lambda i: i >= trim, lstrims), default=None)

        if mintrim is None or maxtrim is None:
            raise ValueError("Trim value is out of the range of available trims in the DataFrame")

        mintrimvar = {}
        maxtrimvar = {}
        res = {}

        for i, itrim in enumerate([mintrim, maxtrim], start=1):
            df1 = df[(df['Trim'] == itrim) & (df['DRAFT'] <= draft_mean)].tail(1)
            df2 = df[(df['Trim'] == itrim) & (df['DRAFT'] >= draft_mean)].head(1)

            if df1.empty or df2.empty:
                raise ValueError(f"No data available for trim {itrim} and draft mean {draft_mean}")

            df1 = df1.iloc[0]
            df2 = df2.iloc[0]

            reqdiff = draft_mean - df1['DRAFT']
            idiff = df2['DRAFT'] - df1['DRAFT']

            for c in df1.index:
                if idiff == 0:
                    (mintrimvar if i == 1 else maxtrimvar)[c] = df2[c]
                else:
                    (mintrimvar if i == 1 else maxtrimvar)[c] = do_linear_interpolation(idiff, df1[c], df2[c], reqdiff)

        reqdiff = trim - mintrim
        idiff = maxtrim - mintrim

        for c in mintrimvar.keys():
            if idiff == 0:
                res[c] = maxtrimvar.get(c, 0)
            else:
                res[c] = do_linear_interpolation(idiff, mintrimvar.get(c, 0), maxtrimvar.get(c, 0), reqdiff)

        return res
    except Exception as e:
        print("Exceptionz while doing the interpolation get_stability_info ==> ", e)
        return None



def getStatbilityData(trim, displacement, df):
    try:
        lstrims = sorted(df['TRIM'].unique())
        mintrim = max(filter(lambda i: i <= trim, lstrims), default=None)
        maxtrim = min(filter(lambda i: i >= trim, lstrims), default=None)

        if mintrim is None or maxtrim is None:
            raise ValueError("Trim value is out of the range of available trims in the DataFrame")

        mintrimvar = {}
        maxtrimvar = {}
        res = {}

        for i, itrim in enumerate([mintrim, maxtrim], start=1):
            df1 = df[(df['TRIM'] == itrim) & (df['DISPL'] <= displacement)].tail(1)
            df2 = df[(df['TRIM'] == itrim) & (df['DISPL'] >= displacement)].head(1)

            if df1.empty or df2.empty:
                raise ValueError(f"No data available for trim {itrim} and displacement {displacement}")

            df1 = df1.iloc[0]
            df2 = df2.iloc[0]

            reqdiff = displacement - df1['DISPL']
            idiff = df2['DISPL'] - df1['DISPL']

            for c in df1.index:
                if idiff == 0:
                    (mintrimvar if i == 1 else maxtrimvar)[c] = df2[c]
                else:
                    (mintrimvar if i == 1 else maxtrimvar)[c] = do_linear_interpolation(idiff, df1[c], df2[c], reqdiff)

        reqdiff = trim - mintrim
        idiff = maxtrim - mintrim

        for c in mintrimvar.keys():
            if idiff == 0:
                res[c] = maxtrimvar.get(c, 0)
            else:
                res[c] = do_linear_interpolation(idiff, mintrimvar.get(c, 0), maxtrimvar.get(c, 0), reqdiff)

        return res
    except Exception as e:
        print("Exception while doing the get_stability_data interpolation ==> ", e)
        return None

# df_sta=get_stability_data(-2,32496,df)
# print(df_sta)