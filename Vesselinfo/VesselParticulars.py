# import pandas as pd
#
# def readVesselParticulars(localpath):
#     try:
#
#         df_vesselparticulars=pd.read_csv(f"{localpath}\VesselParticulars.csv")
#         return df_vesselparticulars
#     except Exception as e:
#         print("The Exception in readVesselParticulars Method:", e)
#
# def get_hold_vcg(df):
#     hold_vcg = {}
#     try:
#         for index, row in df.iterrows():
#             hold_vcg[row["Hold No."]] = row["VCG"]
#     except Exception as e:
#         print("The Exception in get_hold_vcg Method:", e)
#     return hold_vcg
#
# def get_weight_and_volume_max_bounds(df, colname, holdno):
#     try:
#         filter_df = df[df["Hold No."] == holdno]
#         value = filter_df[colname].iloc[0]  # Get the value from the DataFrame
#         # Convert the value to a string, remove comma, and convert to float
#         value_float = float(str(value).replace(',', ''))
#         return value_float
#     except Exception as e:
#         print(f"The Exception in get_weight_and_volume_max_bounds {colname} Method", e)
#     return 0
import pandas as pd

import pandas as pd

# class VesselParticular:
#     def __init__(self, Hold_No, Lengh, Breath, Height, Max_Weight_MT, Stowage_factor_MT_M3,
#                  Volume_without_Hatch, Hatch_Volume, LCG, VCG):
#         self.Hold_No = Hold_No
#         self.Lengh = Lengh
#         self.Breath = Breath
#         self.Height = Height
#         self.Max_Weight_MT = Max_Weight_MT
#         self.Stowage_factor_MT_M3 = Stowage_factor_MT_M3
#         self.Volume_without_Hatch = Volume_without_Hatch
#         self.Hatch_Volume = Hatch_Volume
#         self.LCG = LCG
#         self.VCG = VCG
#
# class VesselParticulars:
#     def __init__(self):
#         self.vessel_dict = {}
#
#     def read_csv(self, localpath):
#         df = pd.read_csv(f"{localpath}/VesselParticulars.csv")
#         for _, row in df.iterrows():
#             vp = VesselParticular(
#                 row['Hold No.'], row['Lengh'], row['Breath'], row['Height'],
#                 row['Max. Weight (MT)'], row['Stowage factor(MT/M3)'],
#                 row['Volume without Hatch'], row['Hatch Volume'],
#                 row['LCG'], row['VCG']
#             )
#             self.vessel_dict[vp.Hold_No] = vp
#         return self.vessel_dict
#
#     def get_vessel_data(self):
#         return self.vessel_dict
#
#     # def extract_field(self, field_name):
#     #     return [getattr(vp, field_name) for vp in self.vessel_dict.values()]
#
# # # Instantiate the class
# # vessel_particulars = VesselParticulars()
# #
# # # Specify the local path
# # localpath = 'C:/Users/deenadayalan.pu/Bcap_python/BCAP_New/BCAP project/PMM/files'
# #
# # # Read the CSV file and get the vessel data
# # vesselinfo = vessel_particulars.read_csv(localpath)
# #
# # # Extract specific field data, for example 'LCG'
# # lcg_values = vessel_particulars.extract_field('LCG')
# #
# # print("LCG Values:", lcg_values)
# #
# # # Print the vessel data to verify the output
# # print("vesselinfo", vesselinfo)
import csv

# Read CSV file into a list of dictionaries
def readVesselParticulars(file_path):
    data_list = []
    with open(f"{file_path}\VesselParticulars.csv", mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_list.append(row)
    return data_list

def getHoldVolumeMaxBounds(vessel,holdNo):
    try:
        vessel_data = [item for item in vessel if int(item["Hold No."]) == int(holdNo)]
        if vessel_data:
            # print( float(vessel_data[0]["Volume without Hatch"]))
            return float(vessel_data[0]["Volume without Hatch"])
        else:
            return 0
    except Exception as e:
        print(f"The Exception in getHoldVolumeMaxBounds Method", e)
        return 0

        # vessel_data = [item for item in vessel if item["Hold No."] == holdNo]
        # print("vessel_data",vessel_data)


def getHoldWeightMaxBounds(vessel,holdNo):
    try:
        vessel_data = [item for item in vessel if int(item["Hold No."]) == int(holdNo)]
        # print("vessel_data",vessel_data)
        if vessel_data:
            return float(vessel_data[0]["Max. Weight (MT)"])
        else:
            return 0
    except Exception as e:
        print(f"The Exception in getHoldVolumeMaxBounds Method", e)
        return 0
