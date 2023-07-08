import returnRangeTxt
import returnFinalValueOfCalibration


def demo(value):
    mac_address = "AB:CD:EF:12:34:56"
    file_path = "calibrationConfigurationFile.txt"
    # value = 350
    range_txt = returnRangeTxt.return_range_txt(value)

    rpm_range_info = returnFinalValueOfCalibration.read_rpm_range_info(file_path, mac_address, range_txt)

    if rpm_range_info:
        # print(rpm_range_info[0])
        for i in rpm_range_info[0]:
            exec(i, globals())
    return m,c,no_of_holes, lbf_m, lbf_c, rbf_m, rbf_c
    


# demo()
# print(c)

# mac_address = "AB:CD:EF:12:34:56"
# file_path = "calibrationConfigurationFile.txt"
# value = 350
# range_txt = returnRangeTxt.return_range_txt(value)

# rpm_range_info = returnFinalValueOfCalibration.read_rpm_range_info(file_path, mac_address, range_txt)

# if rpm_range_info:
#     # print(rpm_range_info[0])
#     for i in rpm_range_info[0]:
#         exec(i)
       

# print(c)

# def return_calibration_values():
#     return c,m