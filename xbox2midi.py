import xbox

def convertInputToMidi(pad):
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
    dpadUp = pad.dpadUp()
    if dpadUp:
        print "dpad up"

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
        print "leftStick"

    rightStick = pad.rightThumbstick()
    a = pad.A()
    b = pad.B()
    x = pad.X()
    y = pad.Y()
    leftBumper = pad.leftBumper()
    rightBumper = pad.rightBumper()

    # Triggers (0 to 1)
    leftTrigger = pad.leftTrigger()
    rightTrigger = pad.rightTrigger()

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
	convertInputToMidi(pad)

        # Move cursor back to start of line
        #print chr(13),
    # Close out when done
    pad.close()

