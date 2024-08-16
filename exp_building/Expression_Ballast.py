import pandas as pd


def readexp_Ballast(localpath):
    try:
        df=pd.read_csv(f"{localpath}Ballast.csv")
        return df
    except Exception as e:
        print("The Exception in readexp_Ballast Method:", e)

df=readexp_Ballast("C:/Users/deenadayalan.pu/Downloads/files/files/")



#getTankDegree,getTankConst

def find_value(df, Tank_name, ExpType, mode='TankDegree'):
    try:
        # Find the row where 'name' and 'Type' match the input values
        row = df[(df['Tank_name(Optional)'] == Tank_name) & (df['Expreesion type(Cargo/Ballast)'] == ExpType)]

        if not row.empty:
            if mode == 'TankDegree':
                return row.iloc[0]['TankDegree']
            elif mode == 'TankConst':
                con_str = row.iloc[0]['TankConst']
                con_list = [float(x) for x in con_str.split(',')]
                return con_list
        return 0 if mode == 'TankDegree' else []
    except Exception as e:
        print("The Exception in find_value Method", e)
        return -1
# df2=find_value(df,"NO.1 W.B.T.(P)","Cargo","TankConst")
# print(df2)


# import csv
#
# class Ballast:
#     def __init__(self, tank_name, tank_degree, tank_const):
#         self.tank_name = tank_name
#         self.tank_degree = tank_degree
#         self.tank_const = tank_const
#
#     @classmethod
#     def from_csv(cls, csv_file):
#         instances = []
#         try:
#             with open(f"{csv_file}Ballast.csv", mode='r') as file:
#                 csv_reader = csv.DictReader(file)
#                 for row in csv_reader:
#                     try:
#                         tank_const = tuple(map(float, row['TankConst'].split(',')))
#                         instance = cls(
#                             tank_name=row['Tank_name(Optional)'],
#                             tank_degree=int(row['TankDegree']),
#                             tank_const=tank_const
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
#             'tank_name': self.tank_name,
#             'tankDegree': self.tank_degree,
#             'tankConst': self.tank_const
#         }
#
#     @staticmethod
#     def get_tank_info_by_name(instances, tank_name=None):
#         try:
#             for instance in instances:
#                 # print(instance)
#                 if tank_name is None or instance.tank_name == tank_name:
#                     return instance.tank_degree, instance.tank_const
#             raise ValueError(f"Tank name {tank_name} not found")
#         except Exception as e:
#             print(f"Error: {e}")
#             return None, None

# Reading the content from the CSV file and storing it in a dictionary
# csv_file_path = "C:/Users/deenadayalan.pu/bcap_octeract_dependacy/bcap_optimizer/BCAP project/KAC/files/Ballast.csv"
# ballast_objects = Ballast.from_csv(csv_file_path)
#
# # Get tankDegree and tankConst for a given tank name (optional)
# tank_name_to_find = 'FORE PEAK TANK'  # specify the tank name you want to find, or leave it as None for the first entry
# tank_degree, tank_const = Ballast.get_tank_info_by_name(ballast_objects, tank_name_to_find)
#
# if tank_degree is not None and tank_const is not None:
#     print(f"TankDegree: {tank_degree}, TankConst: {tank_const}")
# else:
#     print(f"Could not find tank info for tank name {tank_name_to_find}")
