from tkinter import *

from tkinter.ttk import *

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

# All Python Function are written here for this project
# Function for increasment of j For Time Graph
j = 0.1
def time_increasement():
    global j
    if j<30.1:
        j +=0.1
    # return None

# Python Function For Bar Progress and For Variable Changing
def on_message(clien, userdata, msg):
    message0 = str(msg.payload.decode("utf-8"))
    m_in = json.loads(message0)
    msg1 = m_in['Break Force Left']
    msg2 = m_in['Break Force Right']
    message1 = int(m_in['Break Force Left'])
    message2 = int(m_in['Break Force Right'])
    message3 = int(m_in['TestStatus'])
    message4 = int(m_in['Axle Weight'])
    
    # Calling back function to increase time    
    time_increasement()
    
    bar1['value']=message1/3
    lbl2.config(text=message1)
    file = open("sampleText.txt", "a")
    file.writelines(repr(j) + ',' +repr(message1)+"\n")
    file.close()
    
    bar2['value'] = message2/3
    lbl3.config(text=message2)
    file = open("sampleText2.txt", "a")
    file.writelines(repr(j) + ',' +repr(message2) +"\n")
    file.close()
    
    car_testing_status(message3)
    
    excelWeightlbl.config(text=message4)
    
    
    

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
        testing_status.config(text="Test Failed")


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
root.geometry("1400x750")

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
client.connect(mqttBroker)
client.subscribe("001/TESTER/BREAK/BREAKFORCE")
client.on_message = on_message
client.subscribe("TEMPRATURE")
client.on_message = on_message
client.loop_start()

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
bar1 = Progressbar(root,orient=VERTICAL, length=300,  style='red.Vertical.TProgressbar')
bar1.place(x=125, y=320, width=100)

bar2 = Progressbar(root,orient=VERTICAL, length=300,  style="yellow.Vertical.TProgressbar")
bar2.place(x=525, y=320, width=100)

# Making Labels for progressbar measurement Numbers For Progressbar 1
measurmentLabel1= Label(root, text=0, font=(15), background=root_background_color)
measurmentLabel1.place(x=110, y=608)
measurmentLabel1= Label(root, text=50, font=(15), background=root_background_color)
measurmentLabel1.place(x=100, y=558)
measurmentLabel1= Label(root, text=100, font=(15), background=root_background_color)
measurmentLabel1.place(x=90, y=508)
measurmentLabel1= Label(root, text=150, font=(15), background=root_background_color)
measurmentLabel1.place(x=90, y=458)
measurmentLabel1= Label(root, text=200, font=(15), background=root_background_color)
measurmentLabel1.place(x=90, y=408)
measurmentLabel1= Label(root, text=250, font=(15), background=root_background_color)
measurmentLabel1.place(x=90, y=358)
measurmentLabel1= Label(root, text=300, font=(15), background=root_background_color)
measurmentLabel1.place(x=90, y=308)

# Making Labels for progressbar measurement Numbers For Progressbar 2
measurmentLabel1= Label(root, text=0, font=(15), background=root_background_color)
measurmentLabel1.place(x=510, y=608)
measurmentLabel1= Label(root, text=50, font=(15), background=root_background_color)
measurmentLabel1.place(x=500, y=558)
measurmentLabel1= Label(root, text=100, font=(15), background=root_background_color)
measurmentLabel1.place(x=490, y=508)
measurmentLabel1= Label(root, text=150, font=(15), background=root_background_color)
measurmentLabel1.place(x=490, y=458)
measurmentLabel1= Label(root, text=200, font=(15), background=root_background_color)
measurmentLabel1.place(x=490, y=408)
measurmentLabel1= Label(root, text=250, font=(15), background=root_background_color)
measurmentLabel1.place(x=490, y=358)
measurmentLabel1= Label(root, text=300, font=(15), background=root_background_color)
measurmentLabel1.place(x=490, y=308)

# Code To show excel waight
excelWeightlbl_text = Label(root, text="Axle Weight", foreground=information_text_forground_color, background=information_text_background_color, font=(font_family, 14,'bold'), padding=(20,10))
excelWeightlbl_text.place(x=290, y=358)

excelWeightlbl = Label(root, text="1500", foreground=dynamic_data_forground_color, background=dynamic_data_background_color, font=(font_family, 14,'bold'), padding=(20,10))
excelWeightlbl.place(x=330, y=418)

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

testing_status = Label(root, text="Waiting For Vehicle", font=(font_family, 14, 'bold'), background=dynamic_data_background_color, foreground=dynamic_data_forground_color, padding=(5,5))
testing_status.place(x=1050, y=115)

# Test result ok or not ok
test_result_text = Label(root, text="Test Result:", font=(font_family, 18, 'bold'), background=information_text_background_color, foreground=information_text_forground_color, padding=(20,5))
test_result_text.place(x=450, y=655)

test_result = Label(root, text="NOT OK", font=(font_family, 16, 'bold'), background=dynamic_data_background_color, foreground=dynamic_data_forground_color, padding=(20,5))
test_result.place(x=640, y=655)

root.mainloop()

















# import tkinter as tk
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# data = {'year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
#         'unemployment_rates': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
#         }

# dataframe = pd.DataFrame(data)


# root = tk.Tk()

# figure = plt.Figure(figsize=(5,4), dpi=100)

# # Number of rows, number of cols, index position
# figure_plot = figure.add_subplot(1, 1, 1)
# figure_plot.set_ylabel('Unemployment Rate')
# line_graph = FigureCanvasTkAgg(figure, root)
# line_graph.get_tk_widget().pack(side='right')
# dataframe = dataframe[['year', 'unemployment_rates']].groupby('year').sum()
# dataframe.plot(kind='line', legend=True, ax=figure_plot,
#                color='red', marker='o', fontsize=10)
# figure_plot.set_title('Year vs. Unemployment Rate')

# print(data['year'][0])

# root.mainloop()