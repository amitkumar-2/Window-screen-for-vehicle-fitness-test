import tkinter as tk
import math

class Speedometer(tk.Canvas):
    def __init__(self, parent, min_value, max_value):
        super().__init__(parent, width=310, height=310)
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value

        self.configure(bg='black', highlightthickness=0)
        self.create_oval(0, 0, 300, 300, width=3, outline='white', fill='black')
        self.create_text(150, 150, text='Speed', font=('Arial', 16))
        self.value_text = self.create_text(150, 180, text=str(self.value), font=('Arial', 24, 'bold'))
        
        # Add number indications
        num_ticks = 10  # Number of tick marks
        angle_range = 250  # Angle range for the tick marks
        angle_increment = angle_range / (num_ticks - 1)  # Angle increment between each tick mark

        for i in range(num_ticks):
            angle = -215 + i * angle_increment  # Calculate the angle for the tick mark
            radius = 140  # Radius for the tick mark

            x = 150 + radius * math.cos(math.radians(angle))
            y = 150 + radius * math.sin(math.radians(angle))

            value = int(min_value + (max_value - min_value) / (num_ticks - 1) * i)  # Calculate the value for the tick mark

            self.create_text(x, y, text=str(value), font=('Arial', 10), fill='white')


    def update_speed(self, speed):
        self.value = speed
        self.itemconfigure(self.value_text, text=str(self.value))

        # Calculate the angle for the needle
        # angle = (self.value - self.min_value) / (self.max_value - self.min_value) * 180 - 90
        angle = 55 + self.value

        # Calculate the coordinates of the quadrilateral points
        center_x = 150
        center_y = 150
        quad_width = 30
        quad_height = 80

        x1 = center_x - quad_width / 2
        y1 = center_y - quad_height / 2
        x2 = center_x + quad_width / 2
        y2 = center_y - quad_height / 2
        x3 = center_x + 1 / 2
        y3 = center_y + 280 / 2
        x4 = center_x - 1 / 2
        y4 = center_y + 280 / 2

        # Rotate the quadrilateral based on the angle
        rotated_points = rotate_points([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], center_x, center_y, angle)

        # Clear previous needle and draw the new quadrilateral
        self.delete('needle')
        self.create_polygon(rotated_points[0][0], rotated_points[0][1],
                            rotated_points[1][0], rotated_points[1][1],
                            rotated_points[2][0], rotated_points[2][1],
                            rotated_points[3][0], rotated_points[3][1],
                            fill='#ED7D1E', tags='needle')

def rotate_points(points, center_x, center_y, angle):
    rotated_points = []
    for x, y in points:
        rotated_x = center_x + (x - center_x) * math.cos(math.radians(angle)) - (y - center_y) * math.sin(math.radians(angle))
        rotated_y = center_y + (x - center_x) * math.sin(math.radians(angle)) + (y - center_y) * math.cos(math.radians(angle))
        rotated_points.append((rotated_x, rotated_y))
    return rotated_points




speed = [0]  # Store the speed value in a mutable object (list)

def update_speedometer():
    # Update the speed value here from your source (e.g., API or sensor reading)
    if speed[0] < 250:
        speed[0] += 1

    # Update the speedometer display
    speedometer.update_speed(speed[0])

    # Call this function again after a delay (e.g., 1 second)
    root.after(5, update_speedometer)

# Create the main window
root = tk.Tk()
root.config(bg='black')
root.title('Speedometer')

# Create the speedometer widget
speedometer = Speedometer(root, min_value=0, max_value=40)
speedometer.pack(padx=10, pady=10)

# Start updating the speedometer
if speed[0] == 0:
    update_speedometer()
else:
    pass

# Start the Tkinter event loop
root.mainloop()
