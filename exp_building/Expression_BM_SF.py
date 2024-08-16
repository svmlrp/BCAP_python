import pandas as pd
def readexp_BMSF(localpath):
    try:
        df=pd.read_csv(f"{localpath}Exp_bmsf.csv")
        return df
    except Exception as e:
        print("The Exception in readexp_BMSF Method:", e)
# df=readexp_BMSF("C:/Users/deenadayalan.pu/Downloads/files/files/Exp_bmsf.csv")
#GetDistfromAP,GetFramepositionfromaft,getcountBallastTank,getSFusedFrame,
# getBMusedFrame,getSFTrimCorDegree,getSFBaseDraftDegree,getBMBaseValueDegree,
# getBMTrimCorDegree
def find_Frame_value(df,Frame_number,cols):
    output=0
    try:
        for i,row in df.iterrows():
            if row["Frame_number"]== Frame_number:
                output=row[cols]
                break
        return output
    except Exception as e:
        print(f"The Exception in find_Frame_value{cols} Method:", e)
        return -1


#GetHoldbsttankLCG,GetHoldbsttankweight,GetHtank_Weight_Ration
def Frame_hold(df,Frame_number,cols):
    output=[]
    try:
        for i,row in df.iterrows():
            if row["Frame_number"]== Frame_number:
                output=row[cols]
                break
        return output
    except Exception as e:
        print(f"The Exception in Frame_hold{cols} Method:", e)
        return -1

def getcountBMusedFrame(df):
    countBMusedFrame=0
    try:
        for i, row in df.iterrows():
            if row["used_for_BM"]==1:
                countBMusedFrame += 1
        return countBMusedFrame
    except Exception as e:
        print(f"The Exception in getcountBMusedFrame Method:", e)
        return -1

#GetBMBaseConst,GetBMBaseTrimConst,getHoldBMMiConst,getSFBaseConst,getSFBaseTrimConst,
# getWtRatio_blst_tan,getLCG_blst_tank,getRatio_blst_tank,getRatio_hold
def polynomial_frame(df,Frame_number,cols):
    output=[]
    try:
        for i,row in df.iterrows():
            if row["Frame_number"]== Frame_number:
                output=row[cols]
                const=list(map(float, output.split(',')))
                break
        return const
    except Exception as e:
        print(f"The Exception in polynomial_frame{cols} Method:", e)
        return -1

# dd=polynomial(df,109,"BMBaseConst")
# print(dd)

def getBallast_tank_list(df):
    cc=""
    Ballast_tank_list=[]
    try:
        for i,row in df.iterrows():
            cc=row["Ballast_tank_lists"]
            Ballast_tank_list=cc.split(",")
            break
        return Ballast_tank_list
    except Exception as e:
        print(f"The Exception in getBallast_tank_list Method:", e)
        return -1




# import csv
#
# class bmsfcalc:
#     def __init__(self, Frame_number, BMBaseValueDegree, BMTrimCorDegree, BMBaseConst, BMBaseTrimConst,
#                  SFBaseDraftDegree, SFTrimCorDegree, SFBaseConst, SFBaseTrimConst, used_for_BM,
#                  used_for_SF, Htank_Weight_Ratio, HoldBMMiConst, countBallastTank, Ballast_tank_list,
#                  DistfromAP, Hold_tanks_list, LCG_blst_tank, Ratio_blst_tank, Ratio_hold, HoldbsttankLCG):
#         self.Frame_number = Frame_number
#         self.BMBaseValueDegree = BMBaseValueDegree
#         self.BMTrimCorDegree = BMTrimCorDegree
#         self.BMBaseConst = BMBaseConst
#         self.BMBaseTrimConst = BMBaseTrimConst
#         self.SFBaseDraftDegree = SFBaseDraftDegree
#         self.SFTrimCorDegree = SFTrimCorDegree
#         self.SFBaseConst = SFBaseConst
#         self.SFBaseTrimConst = SFBaseTrimConst
#         self.used_for_BM = used_for_BM
#         self.used_for_SF = used_for_SF
#         self.Htank_Weight_Ratio = Htank_Weight_Ratio
#         self.HoldBMMiConst = HoldBMMiConst
#         self.countBallastTank = countBallastTank
#         self.Ballast_tank_list = Ballast_tank_list
#         self.DistfromAP = DistfromAP
#         self.Hold_tanks_list = Hold_tanks_list
#         self.LCG_blst_tank = LCG_blst_tank
#         self.Ratio_blst_tank = Ratio_blst_tank
#         self.Ratio_hold = Ratio_hold
#         self.HoldbsttankLCG = HoldbsttankLCG
#
#     @classmethod
#     def from_csv(cls, csv_file):
#         instances = []
#         try:
#             with open(f"{csv_file}\Exp_bmsf.csv", mode='r') as file:
#                 csv_reader = csv.DictReader(file)
#                 for row in csv_reader:
#                     try:
#                         instance = cls(
#                             Frame_number=float(row['Frame_number']),
#                             BMBaseValueDegree=float(row['BMBaseValueDegree']),
#                             BMTrimCorDegree=float(row['BMTrimCorDegree']),
#                             BMBaseConst=tuple(map(float, row['BMBaseConst'].split(','))),
#                             BMBaseTrimConst=tuple(map(float, row['BMBaseTrimConst'].split(','))),
#                             SFBaseDraftDegree=float(row['SFBaseDraftDegree']),
#                             SFTrimCorDegree=float(row['SFTrimCorDegree']),
#                             SFBaseConst=tuple(map(float, row['SFBaseConst'].split(','))),
#                             SFBaseTrimConst=tuple(map(float, row['SFBaseTrimConst'].split(','))),
#                             used_for_BM=row['used_for_BM'],
#                             used_for_SF=row['used_for_SF'],
#                             Htank_Weight_Ratio=tuple(map(float, row['Htank_Weight_Ratio'].split(','))),
#                             HoldBMMiConst=tuple(map(float, row['HoldBMMiConst'].split(','))),
#                             countBallastTank=int(row['countBallastTank']),
#                             Ballast_tank_list=tuple(map(str, row['Ballast_tank_list'].split(','))),
#                             DistfromAP=float(row['DistfromAP']),
#                             Hold_tanks_list=tuple(map(int, row['Hold_tanks_list'].split(','))),
#                             LCG_blst_tank= tuple(map(float, row['LCG_blst_tank'].split(','))),
#                             Ratio_blst_tank=tuple(map(float, row['Ratio_blst_tank'].split(','))),
#                             Ratio_hold=tuple(map(float, row['Ratio_hold'].split(','))),
#                             HoldbsttankLCG=tuple(map(float, row['HoldbsttankLCG'].split(',')))
#                         )
#                         instances.append(instance)
#                     except ValueError as e:
#                         print(f"Error converting row {row}: {e}")
#         except FileNotFoundError as e:
#             print(f"Error: {e}")
#         except Exception as e:
#             print(f"An unexpected error occurred: {e}")
#         return instances
#
#     def to_dict(self):
#         return {
#             'Frame_number': self.Frame_number,
#             'BMBaseValueDegree': self.BMBaseValueDegree,
#             'BMTrimCorDegree': self.BMTrimCorDegree,
#             'BMBaseConst': self.BMBaseConst,
#             'BMBaseTrimConst': self.BMBaseTrimConst,
#             'SFBaseDraftDegree': self.SFBaseDraftDegree,
#             'SFTrimCorDegree': self.SFTrimCorDegree,
#             'SFBaseConst': self.SFBaseConst,
#             'SFBaseTrimConst': self.SFBaseTrimConst,
#             'used_for_BM': self.used_for_BM,
#             'used_for_SF': self.used_for_SF,
#             'Htank_Weight_Ratio': self.Htank_Weight_Ratio,
#             'HoldBMMiConst': self.HoldBMMiConst,
#             'countBallastTank': self.countBallastTank,
#             'Ballast_tank_list': self.Ballast_tank_list,
#             'DistfromAP': self.DistfromAP,
#             'Hold_tanks_list': self.Hold_tanks_list,
#             'LCG_blst_tank': self.LCG_blst_tank,
#             'Ratio_blst_tank': self.Ratio_blst_tank,
#             'Ratio_hold': self.Ratio_hold,
#             'HoldbsttankLCG': self.HoldbsttankLCG
#         }
#
#     def get_BM_values(data, Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return (instance.BMBaseValueDegree, instance.BMTrimCorDegree, instance.BMBaseConst, instance.BMBaseTrimConst)
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error get_BM_values: {e}")
#             return None
#
#     def get_SF_values(data, Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return (instance.SFBaseDraftDegree, instance.SFTrimCorDegree, instance.SFBaseConst, instance.SFBaseTrimConst)
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_used_for_BM(data, Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return instance.used_for_BM
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_used_for_SF(data, Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return instance.used_for_SF
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_Htank_Weight_Ratio(data, Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return instance.Htank_Weight_Ratio
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_HoldBMMiConst(data, Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return instance.HoldBMMiConst
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_countBallastTank(data):
#         try:
#             if data:
#                 return data[0].countBallastTank
#             raise ValueError("No records available")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_Ballast_tank_list(data):
#         try:
#             if data:
#                 return data[0].Ballast_tank_list
#             raise ValueError("No records available")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_DistfromAP(data, Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return instance.DistfromAP
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_Hold_tanks_list(data):
#         try:
#             if data:
#                 return data[0].Hold_tanks_list
#             raise ValueError("No records available")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_LCG_blst_tank_Ratio_blst_tank(data, Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return instance.LCG_blst_tank, instance.Ratio_blst_tank
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_HoldBMMiConst_Ratio_hold(data, Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return instance.HoldBMMiConst, instance.Ratio_hold
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_HoldbsttankLCG(data, Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return instance.HoldbsttankLCG
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#     def getRatio_blst_tank(data,Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return instance.Ratio_blst_tank
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#     def getHold_tanks_list(data,Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return instance.Hold_tanks_list
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#     def getRatio_hold(data,Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return instance.Ratio_hold
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#     def GetHtank_Weight_Ration(data,Frame_number):
#         try:
#             for instance in data:
#                 if instance.Frame_number == Frame_number:
#                     return instance.Htank_Weight_Ratio
#             raise ValueError(f"Frame number {Frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
# csv_file_path = "C:/Users/deenadayalan.pu/bcap_octeract_dependacy/bcap_optimizer/BCAP project/FWA/files/Exp_bmsf.csv"
# bmsf_objects = bmsfcalc.from_csv(csv_file_path)
#
# # Get tankDegree and tankConst for a given tank name (optional)
# frame_to_find = 299  # specify the tank name you want to find, or leave it as None for the first entry
# x1  = bmsfcalc.get_HoldbsttankLCG(bmsf_objects, frame_to_find)
# # print(x1)
# # print(x2)
# # print(x3)
# # print(x4)
#
