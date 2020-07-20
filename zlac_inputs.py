"""Simple example showing how to get gamepad events."""

from __future__ import print_function
import  zlac_class

from inputs import get_gamepad
import serial
import time
import threading
import struct

def main():
    i = 0
    direction = 0
    m = zlac_class.SpeedMotor('/dev/ttyUSB0', 100)
    m1 = zlac_class.SpeedMotor('/dev/ttyUSB1', 100)
    m.motor_start()
    m1.motor_start()
    try:
        """Just print out some event infomation when the gamepad is used."""
        while True:
            #events = get_gamepad()
            # for event in events:
            #     print(event.ev_type, event.code, event.state)
            i = 250
            m.set_speed = i
            m1.set_speed = -i
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
        m1.motor_stop()
            #print("In main program....")
            # m.motor_stop()
if __name__ == "__main__":
    main()
