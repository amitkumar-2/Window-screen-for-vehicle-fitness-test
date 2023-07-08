import re

def read_rpm_range_info(file_name, mac_address):
    mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    range_pattern = r'^#\s*rpm_range_\d+$'
    range_min_pattern = r'^range_min = (\d+)$'
    range_max_pattern = r'^range_max = (\d+)$'
    
    
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
            elif current_range_txt:
                rpm_range_info.append(value_of_list.strip())
    
    if mac_address_info:
        only_range_min_values = []
        only_range_max_values = []
        values_to_store = []
        for value_of_range_txt in mac_address_info:
            range_min_match = re.match(range_min_pattern, value_of_range_txt)
            # print(range_min_match)
            if range_min_match:
                current_range_min_value = range_min_match.group()
                only_range_min_values.append(current_range_min_value)
        
        for value_of_range_txt in mac_address_info:
            range_max_match = re.match(range_max_pattern, value_of_range_txt)
            # print(range_max_match)
            if range_max_match:
                current_range_max_value = range_max_match.group()
                only_range_max_values.append(current_range_max_value)
        
    return rpm_range_info, rpm_ranges_list, only_range_min_values, only_range_max_values


mac_address = "AB:CD:EF:12:34:56"
file_path = "calibrationConfigurationFile.txt"

rpm_range_info = read_rpm_range_info(file_path, mac_address)

# range_values = []
only_range_min_values = []
only_range_max_values = []
if rpm_range_info:
    # print(rpm_range_info[3])
    for i in rpm_range_info[2]:
        exec(i)
        only_range_min_values.append(range_min)
    for i in rpm_range_info[3]:
        exec(i)
        only_range_max_values.append(range_max)
            
# print(only_range_max_values, only_range_min_values)
for m in range(len(only_range_min_values)):
    file = open("rangeValues.txt", "a")
    file.writelines(repr(only_range_min_values[m]) + ' ' +repr(only_range_max_values[m])+"\n")
    file.close()