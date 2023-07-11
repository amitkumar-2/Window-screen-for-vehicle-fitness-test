from tkinter import Tk

from tkinter.ttk import Label, Progressbar, Button

import paho.mqtt.client as mqtt

import tkinter.ttk as ttk

from PIL import Image,ImageTk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import matplotlib

matplotlib.use("TkAgg")

from matplotlib.figure import Figure

import matplotlib.animation as animation

from matplotlib import style

import json

import calibrationForRange

import calibrationForLBF

import calibrationForRBF

# All Python Function are written here for this project
# Function for increasment of j For Time Graph
j = 0.1
def time_increasement():
    global j
    if j<300.1:
        j +=0.1
    # return None

# Python Function For Bar Progress and For Variable Changing
def on_mqttMessage(clien, userdata, msg):
    # Cleaning all data from rangeValues.txt file
    rangeValues_paths = ['rangeValuesForRPM.txt', 'rangeValuesForLBF.txt', 'rangeValuesForRBF.txt']
    for rangeValues_path in rangeValues_paths:
        with open(rangeValues_path, "w") as file:
            file.write("")
    
    
    
    if msg.topic == "001/TESTER/BREAK/BREAKFORCE": 
        message0 = str(msg.payload.decode("utf-8"))
        m_in = json.loads(message0)
        break_force_left = int(m_in['Break Force Left'])
        break_force_right = int(m_in['Break Force Right'])
        test_status = int(m_in['TestStatus'])
        axle_weight = int(m_in['Axle Weight'])
        rpm = int(m_in['rpm'])
        # Calling back function to increase time    
        time_increasement()
        
        # Code to calibrate rmp values
        file_path = "calibrationConfigurationRangeFile.txt"
        mac_address = "AB:CD:EF:12:34:56"
        value = rpm
        calibrated_variable_rpm = calibrationForRange.write_range_value(file_path, mac_address, value)
        
        # code to calibrate LBF values
        file_path = "calibrationConfigurationLBFFile.txt"
        mac_address = "AB:CD:EF:12:34:56"
        value = break_force_left
        calibrated_variable_lbf = calibrationForLBF.write_range_value(file_path, mac_address, value)
        m_lbf = calibrated_variable_lbf[0]
        c_lbf = calibrated_variable_lbf[1]
        calibrated_lbf = m_lbf*break_force_left + c_lbf
        
        # code to calibrate RBF values
        file_path = "calibrationConfigurationRBFFile.txt"
        mac_address = "AB:CD:EF:12:34:56"
        value = break_force_right
        calibrated_variable_rbf = calibrationForRBF.write_range_value(file_path, mac_address, value)
        m_rbf = calibrated_variable_rbf[0]
        c_rbf = calibrated_variable_rbf[1]
        calibrated_rbf = m_rbf*break_force_right + c_rbf
        
        
        bar1['value']=calibrated_lbf/3
        lbl2.config(text=calibrated_lbf)
        file = open("sampleText.txt", "a")
        file.writelines(repr(j) + ',' +repr(calibrated_lbf)+"\n")
        file.close()
    
        bar2['value'] = calibrated_rbf/3
        lbl3.config(text=calibrated_rbf)
        file = open("sampleText2.txt", "a")
        file.writelines(repr(j) + ',' +repr(calibrated_rbf) +"\n")
        file.close()
        
        car_testing_status(test_status)
        
        excelWeightlbl.config(text=axle_weight)
        
        # k = rpm_calibrated_variable.return_rpm_calibrated_variable(rpm)
        # print(k)
        # print(type(rpm))
        # calibrated_variable = demo(rpm)
        print("m value for RPM: ", calibrated_variable_rpm[0])
        m_rpm = calibrated_variable_rpm[0]
        c_rpm = calibrated_variable_rpm[1]
        calibrated_rpm = m_rpm*rpm + c_rpm
        # rpm_text.config(text=rpm)
        rpm_text.config(text=calibrated_rpm)
    
def publish_msg(topic,msg):
    client.publish(topic,msg)
    
def on_mqttConnect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("001/TESTER/BREAK/BREAKFORCE")
    
    

# Function to update graph
def animate(i):
    pullData = open("sampleText.txt","r").read()
    pullData2 = open("sampleText2.txt","r").read()
    dataList = pullData.split('\n')
    dataList2 = pullData2.split('\n')
    xList = []
    yList = []
    xList2 = []
    yList2 = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
            
    for eachLine2 in dataList2:
        if len(eachLine2) > 1:
            x, y = eachLine2.split(',')
            xList2.append(float(x))
            yList2.append(float(y))
    a.clear()
    a.plot(xList, yList, color='#CC0CA1')
    a.plot(xList2, yList2, color='#2BB3E1')
    a.tick_params(left = False)
    
# Function to define car testing status
def car_testing_status (status_code):
    if status_code == 0:
        testing_status.config(text="Ideal")
    elif status_code == 1:
        testing_status.config(text="Waiting For Vehicle")
    elif status_code == 2:
        testing_status.config(text="Starting Test")
    elif status_code == 3:  
        testing_status.config(text="Test Running")
    elif status_code == 4:
        testing_status.config(text="Test Finished")
    elif status_code == 5:
        testing_status.config(text="Test Failed", foreground='red')
        
# Function to reset page
def run():
    reset_first_page(root)
def reset_first_page (root):  
    publish_msg('001/OPERATOR/BREAK/REQ', 'START_TEST')


# Color variable to store color
root_background_color = '#B5E3CE'
dynamic_data_background_color = '#81D697'
dynamic_data_forground_color = '#000000'
information_text_background_color = '#4CF701'
information_text_forground_color = '#790140'
# Font family variable
font_family = 'Helvetica'

# This is main window configuration Sector
root = Tk()
root.config(background=root_background_color)
root.title("CTI Vehicle Fitness Test")
root.iconbitmap(r"C:\Users\cti-2\Downloads\R&D Team WhatsappFiles\CTIWhatsappForMe\WhatsApp-Image-2023-06-17-at-11.15.32-AM-_1_.ico")
root.geometry("1500x770")
root.minsize(1400,750)

# Adding background images to make rounded corner of labels
image = Image.open("Green.png")
width, height = 285, 70
image = image.resize((width, height), Image.ANTIALIAS)
image_tk = ImageTk.PhotoImage(image)
labelimg = Label(root, image=image_tk, relief='flat', borderwidth=0, background=root_background_color)
labelimg.place(x=440, y=100)

image1 = Image.open("Green.png")
width, height = 285, 70
image1 = image1.resize((width, height), Image.ANTIALIAS)
image1_tk = ImageTk.PhotoImage(image1)
labelimg1 = Label(root, image=image1_tk, relief='flat', borderwidth=0, background=root_background_color)
labelimg1.place(x=45, y=100)

# MQTT All Process Code Is Here
mqttBroker = "3.110.187.253"
client = mqtt.Client("Smartphone")
client.on_message = on_mqttMessage
client.on_connect = on_mqttConnect
client.connect(mqttBroker,1883,60)
client.loop_start()
#client.publish('TEST', 10)
#client.loop_stop()

# Heading Labeling
lbl1 = Label(root,text="Apply parking break to max and take a rest", foreground="white", background="black", font=(font_family, 25, 'bold'), width=100, padding=(250, 20))
lbl1.pack()

# Informating Text Labeling
informationLeftlbl = Label(root, text="Break Force Left", foreground=information_text_forground_color, background=information_text_background_color, font=(font_family, 15,'bold'))
informationLeftlbl.place(x=105, y=120)

informationRightlbl = Label(root, text="Break Force Right", foreground=information_text_forground_color, background=information_text_background_color, font=(font_family, 15,'bold'))
informationRightlbl.place(x=505, y=120)

# Variable Data Measurment Labeling
lbl2 = Label(root, text="0", foreground='#CC0CA1', background=dynamic_data_background_color, font=('font_family', 26,'bold'), padding=(60,20))
lbl2.place(x=100, y=200)

lbl3 = Label(root, text="0", foreground='#0187D5', background=dynamic_data_background_color, font=('font_family', 26,'bold'), padding=(60, 20))
lbl3.place(x=500, y=200)

# Progress bar Styling Color
s = ttk.Style()
s.theme_use("clam")
s.configure("red.Vertical.TProgressbar", foreground='#CC0CA1', background='#CC0CA1')
s.configure("yellow.Vertical.TProgressbar", foreground='#2BB3E1', background='#2BB3E1')

# Progress Bar widget
bar1 = Progressbar(root,orient='vertical', length=300,  style='red.Vertical.TProgressbar')
bar1.place(x=125, y=320, width=100)

bar2 = Progressbar(root,orient='vertical', length=300,  style="yellow.Vertical.TProgressbar")
bar2.place(x=525, y=320, width=100)

# Making Labels for progressbar measurement Numbers For Progressbar 1
measurmentLabel1= Label(root, text=0, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=110, y=608)
measurmentLabel1= Label(root, text=50, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=100, y=558)
measurmentLabel1= Label(root, text=100, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=90, y=508)
measurmentLabel1= Label(root, text=150, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=90, y=458)
measurmentLabel1= Label(root, text=200, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=90, y=408)
measurmentLabel1= Label(root, text=250, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=90, y=358)
measurmentLabel1= Label(root, text=300, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=90, y=308)

# Making Labels for progressbar measurement Numbers For Progressbar 2
measurmentLabel1= Label(root, text=0, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=510, y=608)
measurmentLabel1= Label(root, text=50, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=500, y=558)
measurmentLabel1= Label(root, text=100, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=490, y=508)
measurmentLabel1= Label(root, text=150, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=490, y=458)
measurmentLabel1= Label(root, text=200, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=490, y=408)
measurmentLabel1= Label(root, text=250, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=490, y=358)
measurmentLabel1= Label(root, text=300, font=('',12, 'bold'), background=root_background_color)
measurmentLabel1.place(x=490, y=308)

# Code To show axle weight
excelWeightlbl_text = Label(root, text="Axle Weight", foreground=information_text_forground_color, background=information_text_background_color, font=(font_family, 14,'bold'), padding=(20,10))
excelWeightlbl_text.place(x=290, y=308)

excelWeightlbl = Label(root, text="1500", foreground=dynamic_data_forground_color, background=dynamic_data_background_color, font=(font_family, 14,'bold'), padding=(20,10))
excelWeightlbl.place(x=325, y=368)

# Code to Show RPM
rpm_text = Label(root, text="RPM", foreground=information_text_forground_color, background=information_text_background_color, font=(font_family, 14,'bold'), padding=(20,10))
rpm_text.place(x=325, y=450)

rpm_text = Label(root, text="220", foreground=dynamic_data_forground_color, background=dynamic_data_background_color, font=(font_family, 14,'bold'), padding=(20,10))
rpm_text.place(x=330, y=510)

# Code to show variable data in graph
style.use("ggplot")
f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

canvas = FigureCanvasTkAgg(f, root)
canvas.get_tk_widget().place(x=850, y=220)

# To show tool bar for graph on window
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas._tkcanvas.place(x=800, y=160)

# To update animate function at a interval of point of time
ani = animation.FuncAnimation(f, animate, interval=100)

# Break efficient text and value
break_efficient_text = Label(root, text="Break Efficiency:", font=(font_family, 18, 'bold'), background=information_text_background_color, foreground=information_text_forground_color, padding=(20,5))
break_efficient_text.place(x=50, y=655)

break_efficiency_variable = 90

break_efficient_value = Label(root, text= repr(break_efficiency_variable)  + "%", font=(font_family, 18, 'bold'), background=dynamic_data_background_color, foreground=dynamic_data_forground_color, padding=(30, 5))
break_efficient_value.place(x=300, y=655)

# Car testing progress status
testing_status_text = Label(root, text="Testing Status:", font=(font_family, 14, 'bold'), background=information_text_background_color, foreground=information_text_forground_color, padding=(20,5))
testing_status_text.place(x=850, y=115)

testing_status = Label(root, text="Ideal", font=(font_family, 14, 'bold'), background=dynamic_data_background_color, foreground=dynamic_data_forground_color, padding=(5,5))
testing_status.place(x=1050, y=115)

# Test result ok or not ok
test_result_text = Label(root, text="Test Result:", font=(font_family, 18, 'bold'), background=information_text_background_color, foreground=information_text_forground_color, padding=(20,5))
test_result_text.place(x=450, y=655)

test_result = Label(root, text="NOT OK", font=(font_family, 16, 'bold'), background=dynamic_data_background_color, foreground=dynamic_data_forground_color, padding=(20,5))
test_result.place(x=640, y=657)

# Styling reset buttom with the help of style configuration
s1 = ttk.Style()
def on_enter(event):
    s1.configure("Custom.TButton", foreground=information_text_forground_color, background='white', font =
               ('calibri', 15, 'bold'))
    
def on_leave(event):
    s1.configure("Custom.TButton", foreground=information_text_forground_color, background='white', font =
               ('calibri', 13, 'bold'))
    
s1.configure("Custom.TButton", foreground=information_text_forground_color, background='white', font =
               ('calibri', 13, 'bold'))

button = Button(root, text="Reset", width=10, style="Custom.TButton", command=run)
button.place(x=1175, y=670)

button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)


# rpm = 350
# calibrated_variable = demo(rpm)
# print(calibrated_variable[0])



root.mainloop()