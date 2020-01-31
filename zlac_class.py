#!/usr/bin/python3

import serial
import time
import threading
import struct

motor_enable_date = b'\x00\x00\x01\x01'  # 设置速度模式02 00 C4 C6
motor_speed_mode = b'\x02\x00\xC4\xC6'  # 设置加减速时间0A 14 14 32
motor_accdec_set = b'\x0A\x14\x14\x32'  # 设置转速06 00 88 8E
motor_speed_set = b'\x06\x00\x88\x8E'  # 使能电机00 00 01 01
motor_status = b'\x80\x00\x80'
motor_start = b'\x00\x00\x01\x01'
motor_stop = b'\x00\x00\x00\x00'    # 停机电机 00 00 00 00

# zlacSerial = serial.Serial('/dev/ttyUSB0', 57600)
# zlacSerial.bytesize = 8
# zlacSerial.stopbits = 1
# zlacSerial.parity = "N"

class SpeedMotor:
    def __init__(self, device, speed):

        self.rel_speed = 0 # real speed 真实速度
        self.set_speed = 0 # set speed 设置的速度
        self.run = False # motor run flag 运行状态
        self.fault = None # fault state 故障状态
        self.voltage = 0 # motor voltage 电机电压
        self.current = 0 # motor current 电机电流
        self.serial = serial.Serial(device, 57600) # serial port setup 设置串口通讯
        self.serial.timeout = 0 # serial port timeout
        # start of thread 开启读数据线程
        threads = []
        t1 = threading.Thread(target=self.read_motor)
        threads.append(t1)
        t2 = threading.Thread(target=self.send_motor)
        threads.append(t2)
        for t in threads:
            t.start()
        self.serial.write(motor_speed_mode)
        time.sleep(0.1)
        self.serial.write(motor_accdec_set) # set acceleration and de-acceleration 设置加减速度
        time.sleep(0.1)

    def motor_speed_set(self):
            a1 = 6
            a4 = check_code(a1, self.set_speed)
            self.serial.write(struct.pack(">BhB", a1, self.set_speed, a4))

    def set_status(self):
            self.serial.write(motor_status)
            time.sleep(0.1)

    def motor_start(self):
            self.serial.write(motor_start)
            self.run = True

    def motor_stop(self):
            self.run = False
            self.serial.write(motor_stop)

    def read_motor(self):
            while True:
                n = self.serial.inWaiting()  # wait for data 等待数据的到来，并得到数据的长度
            '''
                if n:  # have return data 如果有数据
                    n = self.serial.read(n)  # 读取n位数据
                    s = [hex(x) for x in bytes(n)]
                    for i in range(len(s)):
                        s[i] = int(s[i], 16)
                    if len(s) == 32:
                        for i in range(int(len(s) / 4)):
                            addr = s[4 * i]
                            if addr == 128:
                                if s[2] == 0:
                                    print("Stopping condition 停止状态")
                                elif s[2] == 1:
                                    print("Moving condition 启动状态")
                                elif s[2] == 2:
                                    print("Over current 过流")
                                elif s[2] == 4:
                                    print("Over voltage 过压")
                                elif s[2] == 8:
                                    print("Encoder failure 编码器故障")
                                elif s[2] == 16:
                                    print("Over heat 过热")
                                elif s[2] == 32:
                                    print("Under voltage 欠压")
                                elif s[2] == 64:
                                    print("Overload 过载")
                            elif addr == 225:
                                high_data = s[4 * i + 1]
                                low_data = s[4 * i + 2]
                                self.voltage = high_data * 256 + low_data
                                print("电压 voltage: " + str(self.voltage))
                            elif addr == 226:
                                high_data = s[4 * i + 1]
                                low_data = s[4 * i + 2]
                                self.current = (int(high_data * 256 + low_data)) / 100
                                print("电流 current:" + str(self.current))
                            elif addr == 228:
                                high_data = s[4 * i + 1]
                                low_data = s[4 * i + 2]
                                self.rel_speed = (int(high_data * 256 + low_data)) * 6000 / 16384
                                print("转速 speed:" + str(self.rel_speed))
                            elif addr == 230:
                                None
                            elif addr == 231:
                                None
                            elif addr == 232:
                                None
                            elif addr == 233:
                                None
                    elif len(s) == 2:
                        if s[0] == 6:
                            print("speed initialise successfully 速度设置成功")
                #print("read motor")
                time.sleep(0.1)
            '''


    def send_motor(self):
        while True:
            if self.run:
                self.set_status()
                time.sleep(0.1) #0.2
                self.motor_speed_set()
                time.sleep(0.1) #0.3
                #print("send motor")

    '''
    通过a1,a2,a3三个码计算出校验和码
    '''

def check_code(a1, a2):
    buffer = struct.pack(">bh", a1, a2)
    buffer = buffer[0] + buffer[1] + buffer[2]
    check_num = (struct.pack(">l", buffer)[-1])
    return check_num

def main():
    pass

    # i = 0
    # direction = 0
    # m = SpeedMotor('/dev/ttyUSB0', 100)
    # m1 = SpeedMotor('/dev/ttyUSB1', 100)
    # m.motor_start()
    # m1.motor_start()
    # try:
    #     while True:
    #         #for i in range(0,300,10):
    #          m.set_speed = i
    #          m1.set_speed = -i
    #          time.sleep(0.5)
    #          if direction == 1:
    #              i -= 10
    #          else:
    #              i += 10
    #
    #          if i == 500:
    #             direction = 1
    #          elif i == -500:
    #             direction = 0
    #
    #         #print("In main program....")
    #         # m.motor_stop()
    # except:
    #     m1.motor_stop()

if __name__ == "__main__":
    main()
