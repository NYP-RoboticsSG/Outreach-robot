"""Simple example showing how to get gamepad events."""

from __future__ import print_function
import  zlac_class

from inputs import get_gamepad
import serial
import time
import threading
import struct
import gamepad
import math


def main():
    i = 0
    direction = 0
    game_control = gamepad.Gamepad('/dev/input/js0')
    m = zlac_class.SpeedMotor('/dev/ttyUSB0', 100)
    m1 = zlac_class.SpeedMotor('/dev/ttyUSB1', 100)
    m.motor_start()
    m1.motor_start()
    try:
        m.set_speed = 0
        m1.set_speed = 0
        """Just print out some event infomation when the gamepad is used."""
        while True:
            #events = get_gamepad()
            # for event in events:
            #     print(event.ev_type, event.code, event.state)
            x_speed = game_control.axis('x')
            y_speed = game_control.axis('y')
            #print("x_speed : ",x_speed,"y_speed : ",y_speed)

            if  abs(x_speed) > 0 or abs(y_speed)>0:
                if abs(y_speed) > 0 and x_speed == 0: # moving forward
                  m1.set_speed =math.floor(y_speed*300)
                  m.set_speed = math.floor(-y_speed*300)
                elif y_speed < 0 and x_speed< 0:       # turn left y is negative  x is negative
                    #print("Turn left")
                    m1.set_speed = math.floor(math.sqrt((y_speed**2 + x_speed**2)) * 300)
                    m.set_speed = math.floor(math.sqrt((y_speed**2 + x_speed**2)) * 300)
                elif y_speed < 0 and x_speed > 0:       # turn right y is negative  x is postive
                    #print("Turn right")
                    m1.set_speed = math.floor(math.sqrt((y_speed ** 2 + x_speed ** 2)) * -300)
                    m.set_speed = math.floor(math.sqrt((y_speed ** 2 + x_speed ** 2)) * -300)
                elif y_speed > 0 and x_speed< 0:       # reverse left y is postive  x is negative
                    #print("reverse left")
                    m1.set_speed = math.floor(math.sqrt((y_speed ** 2 + x_speed ** 2)) * 300)
                    m.set_speed = math.floor(math.sqrt((y_speed ** 2 + x_speed ** 2)) * 300)
                elif y_speed > 0 and x_speed >0:  # reverse right y is postive  x is positive
                    #print("reverse right")
                    m1.set_speed = math.floor(math.sqrt((y_speed ** 2 + x_speed ** 2)) * 300)
                    m.set_speed = math.floor(math.sqrt((y_speed ** 2 + x_speed ** 2)) * 300)
            elif x_speed == 0 and y_speed == 0:
                m.set_speed = 0
                m1.set_speed = 0

            time.sleep(0.1)
            # if direction == 1:
            #      i -= 10
            # else:
            #      i += 10
            # if i == 500:
            #     direction = 1
            # elif i == -500:
            #     direction = 0
         

    except:
        m.motor_stop()
        #




















        m1.motor_stop()

            #print("In main program....")
            # m.motor_stop()
if __name__ == "__main__":
    main()
