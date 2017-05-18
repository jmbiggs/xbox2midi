import xbox

def convertInputToMidi(pad):
    # Left analog stick (-1 to 1)
    leftX = pad.leftX()
    if leftX != 0:
        print("leftX: ", leftX, "\n");

    leftY = pad.leftY()

    # Right analog stick (-1 to 1)
    rightX = pad.rightX()
    rightY = pad.rightY()    

    # Dpad (0 or 1)
    dpadUp = pad.dpadUp()
    dpadDown = pad.dpadDown()
    dpadLeft = pad.dpadLeft()
    dpadRight = pad.dpadRight()

    # Buttons (0 or 1)
    start = pad.Start()
    leftStick = pad.leftThumbstick()
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

if __name__ == "__main__":
    print "xbox2midi running: Press Back button to exit"

    pad = xbox.Joystick()

    # Loop until back button is pressed
    while not pad.Back():

        # Show connection status
        if not pad.connected():
            print "Controller Disconnected"
            break
    
	# Start reading input
	convertInputToMidi(pad)

        # Move cursor back to start of line
        #print chr(13),
    # Close out when done
    pad.close()

