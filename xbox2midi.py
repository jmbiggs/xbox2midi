import xbox

class Button:
    holding = False
    
    def __init__(self, description, getButtonDown):
        self.description = description
        self.getButtonDown = getButtonDown    

def convertInputToMidi(pad, dpadUp):
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

    # Dpad (0 or 1)
    if not dpadUp.holding:
        if eval(dpadUp.getButtonDown):
            print dpadUp.description
            dpadUp.holding = True
    else:
        dpadUp.holding = False

    dpadDown = pad.dpadDown()
    if dpadDown:
        print "dpad down"

    dpadLeft = pad.dpadLeft()
    if dpadLeft:
        print "dpad left"

    dpadRight = pad.dpadRight()
    if dpadRight:
        print "dpad right"

    # Buttons (0 or 1)
    start = pad.Start()
    if start:
        print "start"

    leftStick = pad.leftThumbstick()
    if leftStick:
        print "left stick button"

    rightStick = pad.rightThumbstick()
    if rightStick:
        print "right stick button"
    
    a = pad.A()
    if a:
        print "a"
        
    b = pad.B()
    if b:
        print "b"
        
    x = pad.X()
    if x:
        print "x"
    
    y = pad.Y()
    if y:
        print "y"
    
    leftBumper = pad.leftBumper()
    if leftBumper:
        print "left bumper"
    
    rightBumper = pad.rightBumper()
    if rightBumper:
        print "right bumper"

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

	convertInputToMidi(pad, dpadUp)

    # Close out when done
    pad.close()
