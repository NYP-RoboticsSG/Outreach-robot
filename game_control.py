import gamepad

game_control = gamepad.Gamepad('/dev/input/js0')

while True:
    print("State: ", game_control.button('a'))
    #print("Axes: ",game_control.axis('y'))
    # print("connected: ",game_control.connected)
    # print('Device: ',game_control.device)
    # print("game Control: ",game_control.watch_all())
    # print("Inputs: ",game_control.watch_all())
    # print("Axes: ",game_control.inputs)
    #print("Button btn1", game_control.button('select'))
