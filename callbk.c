void callback(const geometry_msgs::Twist & cmd_input)
//订阅/cmd_vel主题回调函数
{    string port("/dev/ttyUSB0");    //小车串口号
      unsigned long baud = 115200;    //小车串口波特率
       serial::Serial my_serial(port, baud, serial::Timeout::simpleTimeout(1000)); //配置串口
       angular_temp = cmd_input.angular.z ;//获取/cmd_vel的角速度,rad/s
       linear_temp = cmd_input.linear.x ;//获取/cmd_vel的线速度.m/s     //将转换好的小车速度分量为左右轮速度
       left_speed_data.d = linear_temp - 0.5f*angular_temp*D ;
       right_speed_data.d = linear_temp + 0.5f*angular_temp*D ;     //存入数据到要发布的左右轮速度消息
       left_speed_data.d*=ratio;   //放大１０００倍，mm/s
       right_speed_data.d*=ratio;//放大１０００倍，mm/s
       for(int i=0;i<4;i++)    //将左右轮速度存入数组中发送给串口
        {
            speed_data[i]=right_speed_data.data[i];
            speed_data[i+4]=left_speed_data.data[i];
         }     //在写入串口的左右轮速度数据后加入”/r/n“
       speed_data[8]=data_terminal0;
       speed_data[9]=data_terminal1;    //写入数据到串口
       my_serial.write(speed_data,10);
}
