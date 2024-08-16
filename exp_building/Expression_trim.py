import pandas as pd


def readexp_Trim(localpath):
    try:
        df=pd.read_csv(f"{localpath}exp_trim.csv")
        return df
    except Exception as e:
        print("The Exception in readexp_Trim Method:", e)


#getlcbdegree,getmctcdegree,gettrimholddegree
def find_trim_value(df,trimHoldnumber,cols):
    output=0
    try:
        for i,row in df.iterrows():
            if row["trimHoldnumber"]== trimHoldnumber:
                output=row[cols]
                break
        return output
    except Exception as e:
        print(f"The Exception in find_minmass_value{cols} Method:", e)
        return -1
#getholdbalLCB,getlcbconst,getmctcconst,gettrimholdconst,getvolumestart
def polynomial_trim(df,trimHoldnumber,cols):
    output=[]
    try:
        for i,row in df.iterrows():
            if row["trimHoldnumber"]== trimHoldnumber:
                output=row[cols]
                const=list(map(float, output.split(',')))
                break
        return const
    except Exception as e:
        print(f"The Exception in polynomial_trim{cols} Method:", e)
        return -1


# import csv
#
#
# class exp_trim:
#     def __init__(self, Vessel, trimHoldnumber, trimholddegree, trimholdconst, mctcdegree, lcbdegree, mctcconst,
#                  lcbconst, HOLDLCB, volume_start, volume_end, lcg):
#         self.Vessel = Vessel
#         self.trimHoldnumber = trimHoldnumber
#         self.trimholddegree = trimholddegree
#         self.trimholdconst = trimholdconst
#         self.mctcdegree = mctcdegree
#         self.lcbdegree = lcbdegree
#         self.mctcconst = mctcconst
#         self.lcbconst = lcbconst
#         self.HOLDLCB = HOLDLCB
#         self.volume_start = volume_start
#         self.volume_end = volume_end
#         self.lcg = lcg
#
#     @classmethod
#     def from_csv(cls, csv_file):
#         instances = []
#         try:
#             with open(csv_file, mode='r') as file:
#                 csv_reader = csv.DictReader(file)
#                 for row in csv_reader:
#                     try:
#                         trimholdconst = tuple(map(float, row['trimholdconst'].split(',')))
#                         mctcconst = tuple(map(float, row['mctcconst'].split(',')))
#                         lcbconst = tuple(map(float, row['lcbconst'].split(',')))
#                         volume_start = tuple(map(float, row['volume_start'].split(',')))
#                         volume_end = tuple(map(float, row['volume_end'].split(',')))
#                         lcg = tuple(map(float, row['lcg'].split(',')))
#                         instance = cls(
#                             Vessel=row["Vessel"],
#                             trimHoldnumber=int(row['trimHoldnumber']),
#                             trimholddegree=int(row['trimholddegree']),
#                             trimholdconst=trimholdconst,
#                             mctcdegree = int(row['mctcdegree']),
#                             mctcconst = mctcconst,
#                             lcbdegree = int(row['lcbdegree']),
#                             lcbconst = lcbconst,
#                             HOLDLCB=row["HOLDLCB"],
#                             volume_start=volume_start,
#                             volume_end=volume_end,
#                             lcg=lcg
#
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
#
#             'Vessel': self.Vessel ,
#             'trimHoldnumber': self.trimHoldnumber ,
#             'trimholddegree': self.trimholddegree,
#             'trimholddegree': self.trimholdconst ,
#             'mctcdegree': self.mctcdegree ,
#             'lcbdegree': self.lcbdegree ,
#             'mctcconst': self.mctcconst ,
#             'lcbconst': self.lcbconst,
#             'HOLDLCB': self.HOLDLCB ,
#             'volume_start': self.volume_start,
#             'volume_end': self.volume_end,
#             'lcg': self.lcg
#         }
#
#     @staticmethod
#     def get_hold_values(data, trimHoldnumber):
#         try:
#             for instance in data:
#                 # print(instance.trimHoldnumber,trimHoldnumber)
#                 if instance.trimHoldnumber == trimHoldnumber:
#                     # print("inside")
#                     return (instance.trimholddegree, instance.trimholdconst)
#             raise ValueError(f"Hold number {trimHoldnumber} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_mctc_values(data, trimHoldnumber):
#         try:
#             for instance in data:
#                 # print(instance.trimHoldnumber,trimHoldnumber)
#                 if instance.trimHoldnumber == trimHoldnumber:
#                     # print("inside")
#                     return (instance.mctcdegree, instance.mctcconst)
#             raise ValueError(f"Hold number {trimHoldnumber} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_lcb_values(data, trimHoldnumber):
#         try:
#             for instance in data:
#                 # print(instance.trimHoldnumber,trimHoldnumber)
#                 if instance.trimHoldnumber == trimHoldnumber:
#                     # print("inside")
#                     return (instance.lcbdegree, instance.lcbconst)
#             raise ValueError(f"Hold number {trimHoldnumber} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     def get_volume_values(data, trimHoldnumber):
#         try:
#             for instance in data:
#                 # print(instance.trimHoldnumber,trimHoldnumber)
#                 if instance.trimHoldnumber == trimHoldnumber:
#                     # print("inside")
#                     return ( instance.volume_start,instance.volume_end,instance.lcg)
#             raise ValueError(f"Hold number {trimHoldnumber} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#         # @staticmethod
#         # def get_tank_info_by_name(instances, tank_name=None):
#         #     try:
#         #         for instance in instances:
#         #             if tank_name is None or instance.tank_name == tank_name:
#         #                 return instance.tank_degree, instance.tank_const
#         #         raise ValueError(f"Tank name {tank_name} not found")
#         #     except Exception as e:
#         #         print(f"Error: {e}")
#         #         return None, None
#
# # Reading the content from the CSV file and storing it in a dictionary
# csv_file_path = "C:/Users/deenadayalan.pu/bcap_octeract_dependacy/bcap_optimizer/BCAP project/KAC/files/exp_trim.csv"
# trim_objects = exp_trim.from_csv(csv_file_path)
#
# # print(trim_objects)
#
# # # Get tankDegree and tankConst for a given tank name (optional)
# tank_name_to_find = 3# specify the tank name you want to find, or leave it as None for the first entry
# tank_degree = exp_trim.get_volume_values(trim_objects, tank_name_to_find)
# print(tank_degree)
# #
# # if tank_degree is not None and tank_const is not None:
# #     print(f"TankDegree: {tank_degree}, TankConst: {tank_const}")
# # else:
# #     print(f"Could not find tank info for tank name {tank_name_to_find}")