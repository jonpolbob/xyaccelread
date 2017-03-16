import serial
import matplotlib.pyplot as plt
import numpy as np
import win32com.client
import time

connected = False

plt.ion()  # sets plot to animation mode

length = 200  # determines length of data taking session (in data points)
x = [0] * length  # create empty variable of length of test
y = [0] * length

xline, = plt.plot(x)  # sets up future lines to be modified
yline, = plt.plot(y)
plt.ylim(-15, 15)  # sets the y axis limits

# finds COM port that the Arduino is on (assumes only one Arduino is connected)
wmi = win32com.client.GetObject("winmgmts:")
comPort =None

for port in wmi.InstancesOf("Win32_SerialPort"):
    # print port.Name #port.DeviceID, port.Name
    if "Arduino" in port.Name:
        comPort = port.DeviceID
        print(comPort, "is Arduino")

if comPort == None:
    print("com not found"
          )
ser = serial.Serial(None, 115200,rtscts=False, dsrdtr=False)  # sets up serial connection (make sure baud rate is correct - matches Arduino)

ser.dtr=False
time.sleep(1)

#ser.rts=True
ser.dtr=True
ser.port=comPort
ser.open()
time.sleep(1)


#ser.close()
#ser = serial.Serial(comPort, 115200,rtscts=False, dsrdtr=False)  # sets up serial connection (make sure baud rate is correct - matches Arduino)

x=0
y=0

tabx = []
taby = []

connected = True
status =0

buffer =[]

fig = plt.figure()
axes = fig.add_subplot(111)

axes.set_autoscale_on(False)
#axes.autoscale_view(False,True,False)


count =0
while connected:
    ser.reset_input_buffer()
    buffer = []
    for valeur in ser.read(300):
        buffer.append(int(valeur))

    print('*')

    status=0
    xmax =0

    if len(tabx)>600:
        tabx = tabx[100:]
        taby = taby[100:]

    Seuil = 1

    save=0

    for valserin in buffer:
        if valserin & 0x80 != 0: #debut de trame
            x = (valserin & 0x07) <<7
            y = (valserin & 0x38) << 4
            status =1
        else:
            if status == 2:
                y += valserin
                status = 3

            if status == 1:
                x += valserin
                status = 2

        if status !=3:
            continue

        status=0

        xvallog = (x-512)/512*18
        xmax = max(xmax,xvallog)
        yvallog = (y-512)/512*18

        if xvallog>Seuil:
            save=1


        if (save==1):  #detection : on ernregistre tout
            tabx.append(xvallog)  # add new value as int to current list
            taby.append(yvallog)
            count=6
        else: #pas ens ave : on enregistre que les 30 derniers
            if len(tabx) > 30 and count ==0:
                tabx = tabx[1:]
                taby = taby[1:]
            tabx.append(xvallog)  # add new value as int to current list
            taby.append(yvallog)



    if save ==0 and count > 0:
        count -= 1

    print("MAX = ", xmax)

    #reset tableaux apres un
    if save ==0 and count ==0:
        tabx = []
        taby = []
        continue

    if len(tabx) < 30:
        continue

    plt.cla()
    axes.set_autoscale_on(True)
    axes.relim()
    axes.autoscale_view(False, True, True)

    axes.plot(range(len(tabx)),tabx)
    axes.plot(range(len(taby)), taby)

    plt.pause(0.001)  # in seconds pour reaffichage
    plt.draw()  # draws new plot



ser.close()  # closes serial connection (very important to do this! if you have an error partway through the code, type this into the cmd line to close the connection)

