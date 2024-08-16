import pandas as pd

def readexp_Deflection(localpath):
    try:

        df=pd.read_csv(f"{localpath}Deflection.csv")
        return df
    except Exception as e:
        print("The Exception in readexp_Deflection Method:", e)
# csv_file_path = "D:/BCAP_python/BCAP project/FWA/files/Deflection.csv"
# df=readexp_Deflection(csv_file_path)

#getmid_ship_distance_from_AP,getFramepostionafp,getDistFromAft,getDistprevframe,
# getEndFrame,getMidframe,getUDDraftMDegree2,getUDDraftMDegreewfame
def find_deflection_value(df,Frame_number,cols):
    output=0
    try:
        for i,row in df.iterrows():
            if row["Frame_number"]== Frame_number:
                output=row[cols]
                break
        return output
    except Exception as e:
        print(f"The Exception in find_deflection_value{cols} Method:", e)
        return -1

def getUDDraftMDegreewfame(df):
    output=0
    try:
        for i,row in df.iterrows():
            output=row["UDDraftMDegree"]
            break
        return output
    except Exception as e:
        print(f"The Exception in getUDDraftMDegreewfame Method:", e)
        return -1
#getUDDraftMConst2,getUDDraftMConstwfame
def polynomial_deflection(df,Frame_number,cols):
    output=[]
    try:
        for i,row in df.iterrows():
            if row["Frame_number"]== Frame_number:
                output=row[cols]
                const=list(map(float, output.split(',')))
                break
        return const
    except Exception as e:
        print(f"The Exception in polynomial_deflection{cols} Method:", e)
        return -1
def getUDDraftMConstwfame(df,cols):
    output=[]
    try:
        for i,row in df.iterrows():
            cc=row[cols]
            const=list(map(float, cc.split(',')))
            output.append(const)
        return const
    except Exception as e:
        print(f"The Exception in getUDDraftMConstwfame Method:", e)
        return -1

# import csv
#
# class Deflection:
#     def __init__(self, UDDraftMDegree, UDDraftMConst, mid_ship_distance_from_AP, frame_number, Framepostionafp, DistFromAft, Distprevframe, EndFrame, Midframe):
#         self.UDDraftMDegree = UDDraftMDegree
#         self.UDDraftMConst = UDDraftMConst
#         self.mid_ship_distance_from_AP = mid_ship_distance_from_AP
#         self.frame_number = frame_number
#         self.Framepostionafp = Framepostionafp
#         self.DistFromAft = DistFromAft
#         self.Distprevframe = Distprevframe
#         self.EndFrame = EndFrame
#         self.Midframe = Midframe
#
#     @classmethod
#     def from_csv(cls, csv_file):
#         instances = []
#         try:
#             with open(csv_file, mode='r') as file:
#                 csv_reader = csv.DictReader(file)
#                 for row in csv_reader:
#                     try:
#                         instance = cls(
#                             UDDraftMDegree=float(row['UDDraftMDegree']),
#                             UDDraftMConst=tuple(map(float, row['UDDraftMConst'].split(','))),
#                             mid_ship_distance_from_AP=float(row['mid_ship_distance_from_AP']),
#                             frame_number=float(row['Frame_number']),
#                             Framepostionafp=float(row['Framepostionafp']),
#                             DistFromAft=float(row['DistFromAft']),
#                             Distprevframe=float(row['Distprevframe']),
#                             EndFrame=int(row['EndFrame']),
#                             Midframe=int(row['Midframe'])
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
#             'UDDraftMDegree': self.UDDraftMDegree,
#             'UDDraftMConst': self.UDDraftMConst,
#             'mid_ship_distance_from_AP': self.mid_ship_distance_from_AP,
#             'frame_number': self.frame_number,
#             'Framepostionafp': self.Framepostionafp,
#             'DistFromAft': self.DistFromAft,
#             'Distprevframe': self.Distprevframe,
#             'EndFrame': self.EndFrame,
#             'Midframe': self.Midframe
#         }
#
#     @staticmethod
#     def get_first_record(instances):
#         try:
#             if instances:
#                 instance = instances[0]
#                 return instance.UDDraftMDegree, instance.UDDraftMConst
#             else:
#                 raise ValueError("No records available")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None, None
#
#     @staticmethod
#     def get_mid_ship_distance(instances, frame_number):
#         try:
#             for instance in instances:
#                 if instance.frame_number == frame_number:
#                     return instance.mid_ship_distance_from_AP
#             raise ValueError(f"Frame number {frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     @staticmethod
#     def get_Framepostionafp(instances, frame_number):
#         try:
#             for instance in instances:
#                 if instance.frame_number == frame_number:
#                     return instance.Framepostionafp
#             raise ValueError(f"Frame number {frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     @staticmethod
#     def get_DistFromAft(instances, frame_number):
#         try:
#             for instance in instances:
#                 if instance.frame_number == frame_number:
#                     return instance.DistFromAft
#             raise ValueError(f"Frame number {frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     @staticmethod
#     def get_Distprevframe(instances, frame_number):
#         try:
#             for instance in instances:
#                 if instance.frame_number == frame_number:
#                     return instance.Distprevframe
#             raise ValueError(f"Frame number {frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     @staticmethod
#     def get_EndFrame(instances, frame_number):
#         try:
#             for instance in instances:
#                 if instance.frame_number == frame_number:
#                     return instance.EndFrame
#             raise ValueError(f"Frame number {frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
#     @staticmethod
#     def get_Midframe(instances, frame_number):
#         try:
#             for instance in instances:
#                 if instance.frame_number == frame_number:
#                     return instance.Midframe
#             raise ValueError(f"Frame number {frame_number} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#
# # Reading the content from the CSV file and storing it in a dictionary
# csv_file_path = "D:/BCAP_python/BCAP project/FWA/files/Deflection.csv"
# deflection_objects = Deflection.from_csv(csv_file_path)
#
# # Get UDDraftMDegree and UDDraftMConst from the first record
# UDDraftMDegree, UDDraftMConst = Deflection.get_first_record(deflection_objects)
# print(f"UDDraftMDegree: {UDDraftMDegree}, UDDraftMConst: {UDDraftMConst}")
#
# # Example: Get mid_ship_distance_from_AP for a given frame number
# frame_number_to_find = 299 # specify the frame number you want to find
# mid_ship_distance = Deflection.get_mid_ship_distance(deflection_objects, frame_number_to_find)
# print(f"Mid ship distance from AP for frame {frame_number_to_find}: {mid_ship_distance}")
#
# # Example: Get Framepostionafp for a given frame number
# Framepostionafp = Deflection.get_Framepostionafp(deflection_objects, frame_number_to_find)
# print(f"Framepostionafp for frame {frame_number_to_find}: {Framepostionafp}")
#
# # Example: Get DistFromAft for a given frame number
# dist_from_aft = Deflection.get_DistFromAft(deflection_objects, frame_number_to_find)
# print(f"DistFromAft for frame {frame_number_to_find}: {dist_from_aft}")
#
# # Example: Get Distprevframe for a given frame number
# dist_prev_frame = Deflection.get_Distprevframe(deflection_objects, frame_number_to_find)
# print(f"Distprevframe for frame {frame_number_to_find}: {dist_prev_frame}")
#
# # Example: Get EndFrame for a given frame number
# end_frame = Deflection.get_EndFrame(deflection_objects, frame_number_to_find)
# print(f"EndFrame for frame {frame_number_to_find}: {end_frame}")
#
# # Example: Get Midframe for a given frame number
# mid_frame = Deflection.get_Midframe(deflection_objects, frame_number_to_find)
# print(f"Midframe for frame {frame_number_to_find}: {mid_frame}")
