import WriteRangeValueInFile


# def return_range_txt(value):
#     def return_range_txt_func1(value):
#         mac_address = "AB:CD:EF:12:34:56"
#         file_path = "calibrationConfigurationFile.txt"

#         rpm_range_info = WriteRangeValueInFile.read_rpm_range_info(file_path, mac_address)



#         range_values = []

#         with open("rangeValues.txt", "r") as file:
#             for line in file:
#                 start, end = map(int, line.strip().split())
#                 range_values.append(range(start, end))

#         print(range_values)

        
#         range_txt = None
#         for j in range(len(range_values)):
#             for i  in range_values[j]:
#                 if i == value:
#                     # print(rpm_range_info[1][j])
#                     range_txt = rpm_range_info[1][j]
#                 else:
#                     pass
                
#         return range_txt
#     return return_range_txt_func1(value)
    
# value = 350
# return_range_txt = return_range_txt(value)
# print(return_range_txt)


mac_address = "AB:CD:EF:12:34:56"
file_path = "calibrationConfigurationFile.txt"

rpm_range_info = WriteRangeValueInFile.read_rpm_range_info(file_path, mac_address)



range_values = []

with open("rangeValues.txt", "r") as file:
    for line in file:
        start, end = map(int, line.strip().split())
        range_values.append(range(start, end))

print(range_values)

value = 350
range_txt = None
for j in range(len(range_values)):
    for i  in range_values[j]:
        if i == value:
            # print(rpm_range_info[1][j])
            range_txt = rpm_range_info[1][j]
        else:
            pass
        
def return_range_txt():
    return range_txt