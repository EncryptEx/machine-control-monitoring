import gpiod

import time

# Define the control pins

ControlPin = [14, 15, 18, 23]

# Create a GPIO chip and get the lines

chip = gpiod.Chip('gpiochip4')

lines = [chip.get_line(pin) for pin in ControlPin]

# Configure the lines as outputs

for line in lines:

   line.request('stepper_motor', gpiod.LINE_REQ_DIR_OUT, 0)

# Define the segment pattern

seg_right_full = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

seg_left_full = [
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0]
]



seg_right = [

   [1, 0, 0, 0],

   [1, 1, 0, 0],

   [0, 1, 0, 0],

   [0, 1, 1, 0],

   [0, 0, 1, 0],

   [0, 0, 1, 1],

   [0, 0, 0, 1],

   [1, 0, 0, 1]

]

seg_left = [

   [0, 0, 0, 1],

   [0, 0, 1, 1],

   [0, 0, 1, 0],

   [0, 1, 1, 0],

   [0, 1, 0, 0],

   [1, 1, 0, 0],

   [1, 0, 0, 0],

   [1, 0, 0, 1]

]


halfstepEnabled = True

delay = 0.001 #You can control the acceleration from the delay value !

# Run the stepper motor for 512 steps

for i in range(512):

    if(halfstepEnabled):
        for halfstep in range(8):
            for pin in range(4):
                lines[pin].set_value(seg_right[halfstep][pin])
            time.sleep(delay)

    else: 
        for pin in range(4):
            lines[pin].set_value(seg_right_full[i%4][pin])
        time.sleep(delay)


for i in range(512):
    if(halfstepEnabled):
        for halfstep in range(8):
            for pin in range(4):
                lines[pin].set_value(seg_left[halfstep][pin])
            time.sleep(delay)

    else: 
        for pin in range(4):
            lines[pin].set_value(seg_left_full[i%4][pin])
        time.sleep(delay)

# Release the GPIO lines

for line in lines:

   line.release()


