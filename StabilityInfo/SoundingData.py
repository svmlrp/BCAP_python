import pandas as pd

def readSoundingData(localpath):
    df=pd.read_csv(localpath)
    return df
# df=readSoundingData("C:/Users/deenadayalan.pu/Downloads/files/files/SoundingData.csv")
#getMinLCG,getMaxLCG
def getLCG(soundData, Name, find_min=True):
    lcg_value = 0
    try:
        filtered_data = [row for row in soundData if row['TANKNAME'] == Name]
        if filtered_data:
            if find_min:
                lcg_value = min(row['LCGLPP'] for row in filtered_data)
            else:
                lcg_value = max(row['LCGLPP'] for row in filtered_data)
    except Exception as e:
        print("The Exception in getLCG Method:", e)
    return lcg_value

def do_linear_interpolation(idiff, min_value, max_value, reqdiff):
    return min_value + (max_value - min_value) * (reqdiff / idiff)


def get_souding_lcg_and_vcg(name, volume, sounding_data):
    lcg_data = {}
    try:
        # Find Min and Max based on the conditions
        min_row = next(row for row in sounding_data if row['TANKNAME'] == name and row['VOLUMEINCUBE'] <= volume)
        max_row = next(row for row in sounding_data if row['TANKNAME'] == name and row['VOLUMEINCUBE'] >= volume)

        if min_row['VOLUMEINCUBE'] == max_row['VOLUMEINCUBE']:
            lcg_data[f"{name}LCG"] = min_row['LCGLPP']
            lcg_data[f"{name}VCG"] = min_row['VCGBL']
            lcg_data[f"{name}TCG"] = min_row['TCG']
            lcg_data[f"{name}VOLPercentage"] = min_row['VOLUMEINPERCENTAGE']
            lcg_data[f"{name}FSM"] = min_row['FSM']
        else:
            reqdiff = volume - min_row['VOLUMEINCUBE']
            idiff = max_row['VOLUMEINCUBE'] - min_row['VOLUMEINCUBE']

            lcg = do_linear_interpolation(idiff, min_row['LCGLPP'], max_row['LCGLPP'], reqdiff)
            vcg = do_linear_interpolation(idiff, min_row['VCGBL'], max_row['VCGBL'], reqdiff)
            tcg = do_linear_interpolation(idiff, min_row['TCG'], max_row['TCG'], reqdiff)
            vol_percentage = do_linear_interpolation(idiff, min_row['VOLUMEINPERCENTAGE'], max_row['VOLUMEINPERCENTAGE'], reqdiff)
            fsm = do_linear_interpolation(idiff, min_row['FSM'], max_row['FSM'], reqdiff)

            lcg_data[f"{name}LCG"] = lcg
            lcg_data[f"{name}VCG"] = vcg
            lcg_data[f"{name}TCG"] = tcg
            lcg_data[f"{name}VOLPercentage"] = vol_percentage
            lcg_data[f"{name}FSM"] = fsm

    except Exception as e:
        print("The exception in get_souding_lcg_and_vcg:", e)

    return lcg_data

# get_souding_lcg_and_vcg("HOLD1",750,df)