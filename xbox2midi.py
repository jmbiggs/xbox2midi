import xbox

class Button:
    holding = False
    
    def __init__(self, description, getButtonDown):
        self.description = description
        self.getButtonDown = getButtonDown    

class AnalogStick:
    def __init__(self, description, getValue):
        self.description = description
        self.getValue = getValue

# define buttons
dpadUp = Button("dpad up", "pad.dpadUp()")
dpadDown = Button("dpad down", "pad.dpadDown()")
dpadLeft = Button("dpad left", "pad.dpadLeft()")
dpadRight = Button("dpad right", "pad.dpadRight()")
start = Button("start", "pad.Start()")
leftStick = Button("left stick button", "pad.leftThumbstick()")
rightStick = Button("right stick button", "pad.rightThumbstick()")
a = Button("a", "pad.A()")
b = Button("b", "pad.B()")
x = Button("x", "pad.X()")
y = Button("y", "pad.Y()")
leftBumper = Button("left bumper", "pad.leftBumper()")
rightBumper = Button("right bumper", "pad.rightBumper()")

# define analog joysticks
leftX = AnalogStick("left X", "pad.leftX()")
leftY = AnalogStick("left Y", "pad.leftY()")
rightX = AnalogStick("right X", "pad.rightX()")
rightY = AnalogStick("right Y", "pad.rightY()")
leftTrigger = AnalogStick("left trigger", "pad.leftTrigger()")    
rightTrigger = AnalogStick("right trigger", "pad.rightTrigger()")

buttons = [dpadUp, dpadDown, dpadLeft, dpadRight, start, leftStick, rightStick, a, b, x, y, leftBumper, rightBumper]
joysticks = [leftX, leftY, rightX, rightY, leftTrigger, rightTrigger]

def convertInputToMidi():
    # handle buttons
    for button in buttons:    
        if button.holding:
            # check if it is still actually holding
            if not eval(button.getButtonDown):
                button.holding = False    
        else:
            # see if it is being pressed (for the first time)
            if eval(button.getButtonDown):
                print button.description
                button.holding = True
    
    # handle analog sticks
    for joystick in joysticks:
        currentValue = eval(joystick.getValue)
        if currentValue >= 0.1 or currentValue <= -0.1:
            print joystick.description, ":", currentValue
    
def printConnected(connected):
    if connected:
        print "Controller Connected"
    else:
        print "Controller Disconnected"

if __name__ == "__main__":
    print "xbox2midi running: Press Back button to exit"

    pad = xbox.Joystick()
    connected = pad.connected()
    printConnected(connected)

    # Loop until back button is pressed
    while not pad.Back():
        # Show connection status
        wasConnected = connected
        connected = pad.connected()
        if wasConnected != connected:
            printConnected(connected)

        # run conversions on inputs
        convertInputToMidi()

    # Close out when done
    pad.close()
