#!/usr/bin/python3

import serial
import time
 
motor_enable_date=b'\x00\x00\x01\x01' #设置速度模式02 00 C4 C6
motor_speed_mode=b'\x02\x00\xC4\xC6' #设置加减速时间0A 14 14 32
motor_accdec_set=b'\x0A\x14\x14\x32' #设置转速06 00 88 8E
motor_speed_set=b'\x06\x00\x88\x8E' #使能电机00 00 01 01
motor_status=b'\x80\x00\x80'#停机电机 00 00 00 00
 
zlacSerial=serial.Serial('/dev/ttyUSB0',57600)
zlacSerial.bytesize = 8
zlacSerial.stopbits = 1
zlacSerial.parity = "N"
 

 
def motor_enable(serial):
    try:
        serial.write(motor_speed_mode)
        serial.write(motor_accdec_set)
        time.sleep(0.1)
        serial.write(motor_speed_set)
        time.sleep(0.1)
        serial.write(motor_enable_date)
        time.sleep(0.1)
        serial.write(motor_status)
        time.sleep(1)
        serial.write(motor_status)
        time.sleep(1)
        serial.write(motor_status)
        time.sleep(1)
        serial.write(motor_status)
 
        time.sleep(1)
 
        print('send ok')
    except:
 
        print('cant write motor_enable')

motor_enable(zlacSerial)
time.sleep(1)
n=zlacSerial.readline()

if n:
    data= [hex(x) for x in bytes(n)]
    print(data)
zlacSerial.flush()
 
#print('ok')
# 关闭 串口
if zlacSerial.isOpen():
    zlacSerial.close()
