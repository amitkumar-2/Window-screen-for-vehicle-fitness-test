import re
import returnRangeTxt

def read_rpm_range_info(file_name, mac_address, rpm_range_txt):
    mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    range_pattern = r'^#\s*rpm_range_\d+$'
    
    
    with open(file_name, 'r') as file:
        lines = file.readlines()
        
    mac_address_info = []
    rpm_range_info = []
    rpm_ranges_list = []
    current_mac = None
    current_range_txt = None
    
    for line in lines:
        mac_match = re.match(mac_pattern, line)
        if mac_match:
            current_mac = mac_match.group()
        elif current_mac == mac_address:
            mac_address_info.append(line.strip())
    
    if mac_address_info:
        # print(mac_address_info)
        for value_of_list in mac_address_info:
            # print(value_of_list)
            range_txt_match = re.match(range_pattern, value_of_list)
            if range_txt_match:
                current_range_txt = range_txt_match.group()
                # print(current_range_txt)
                rpm_ranges_list.append(current_range_txt)
                # print(rpm_ranges_list)
            elif current_range_txt == rpm_range_txt:
                rpm_range_info.append(value_of_list.strip())
                # print(rpm_range_info[0])
                # if range_min:
                # print(range_min)
            
            
            
    return rpm_range_info, rpm_ranges_list
    # return mac_address_info


mac_address = "AB:CD:EF:12:34:56"
file_path = "calibrationConfigurationFile.txt"
range_txt = returnRangeTxt.return_range_txt()

# read_rpm_range_info(file_path, mac_address, range_txt)

rpm_range_info = read_rpm_range_info(file_path, mac_address, range_txt)

if rpm_range_info:
    # print(rpm_range_info[0])
    for i in rpm_range_info[0]:
        exec(i)
       

def return_calibration_values():
    return c,m