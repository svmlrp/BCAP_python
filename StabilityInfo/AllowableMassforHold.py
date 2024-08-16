import pandas as pd

def readAllowableMassforHold(localpath):
    df=pd.read_csv(localpath)
    return df
df=readAllowableMassforHold("C:/Users/deenadayalan.pu/Downloads/files/files/AllowableMass.csv")
# print(df)
def do_linear_interpolation(wtdiff, aboverow_wt, belowrow_wt, draftdiff):
    return aboverow_wt + (wtdiff * draftdiff / (belowrow_wt - aboverow_wt))


def get_max_and_min_weight_of_mean_draft(holdno, allowablemass, meandraft):
    holdmaxweight = 0
    holdminweight = 0
    WeightArray = []

    try:
        if meandraft > 0:
            filtered_above = allowablemass[
                (allowablemass['Draft at mid-Hold(m)'] <= meandraft) & (allowablemass['Hold'] == holdno)]
            filtered_below = allowablemass[
                (allowablemass['Draft at mid-Hold(m)'] >= meandraft) & (allowablemass['Hold'] == holdno)]

            if not filtered_above.empty:
                aboverow = filtered_above.iloc[-1]  # Get the last row
                upperbound = not filtered_below.empty

                if upperbound and aboverow['Draft at mid-Hold(m)'] == meandraft:
                    holdmaxweight = aboverow['Max. sea (MT)']
                    holdminweight = aboverow['Min. sea (MT)']
                elif upperbound:
                    belowrow = filtered_below.iloc[0]  # Get the first row
                    draftdiff = meandraft - aboverow['meanDraft']

                    wtdiff = belowrow['Max. sea (MT)'] - aboverow['Max. sea (MT)']
                    holdmaxweight = (
                        aboverow['Max. sea (MT)'] if aboverow['Max. sea (MT)'] == belowrow['Max. sea (MT)']
                        else do_linear_interpolation(wtdiff, aboverow['Max. sea (MT)'], belowrow['Max. sea (MT)'], draftdiff)
                    )

                    wtdiff = belowrow['Min. sea (MT)'] - aboverow['Min. sea (MT)']
                    holdminweight = (
                        aboverow['Min. sea (MT)'] if aboverow['Min. sea (MT)'] == belowrow['Min. sea (MT)']
                        else do_linear_interpolation(wtdiff, aboverow['Min. sea (MT)'], belowrow['Min. sea (MT)'], draftdiff)
                    )
                else:
                    holdmaxweight = aboverow['Max. sea (MT)']
                    holdminweight = aboverow['Min. sea (MT)']

        WeightArray.append(holdmaxweight)
        WeightArray.append(holdminweight)

    except Exception as e:
        print("The Exception in get_max_and_min_weight_of_mean_draft Method:", e)

    return WeightArray

# df2=get_max_and_min_weight_of_mean_draft(5,df,18)
# print(df2)