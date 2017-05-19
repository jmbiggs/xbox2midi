import xbox

class Button:
    holding = False
    
    def __init__(self, description, getButtonDown):
        self.description = description
        self.getButtonDown = getButtonDown    

def convertInputToMidi(pad, buttons):
    
    # Buttons (0 or 1)
    for button in buttons:    
        if not button.holding:
            if eval(button.getButtonDown):
                print button.description
                button.holding = True
        else:
            button.holding = False
    
    # Left analog stick (-1 to 1)
    leftX = pad.leftX()
    if leftX != 0:
        print "leftX:", leftX

    leftY = pad.leftY()
    if leftY != 0:
        print "leftY:", leftY

    # Right analog stick (-1 to 1)
    rightX = pad.rightX()
    if rightX:
        print "rightX:", rightX

    rightY = pad.rightY()
    if rightY:
        print "rightY:", rightY

    # Triggers (0 to 1)
    leftTrigger = pad.leftTrigger()
    if leftTrigger != 0:
        print "left trigger:", leftTrigger
    
    rightTrigger = pad.rightTrigger()
    if rightTrigger != 0:
        print "right trigger:", rightTrigger
    
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
    
	# Start reading input
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

    buttons = [dpadUp, dpadDown, dpadLeft, dpadRight, start, leftStick, rightStick, a, b, x, y, leftBumper, rightBumper]

	convertInputToMidi(pad, buttons)

    # Close out when done
    pad.close()
