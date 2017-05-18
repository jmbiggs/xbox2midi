import xbox

if __name__ == "__main__":
    pad = xbox.Joystick()

    print "xbox2midi running: Press Back button to exit"

    # Loop until back button is pressed
    while not pad.Back():

        # Show connection status
        if pad.connected():
            print "Connected   ",
        else:
            print "Disconnected",
    
	# Start reading input
	convertInputToMidi()

        # Move cursor back to start of line
        #print chr(13),
    # Close out when done
    joy.close()

def convertInputToMidi():
    # Left analog stick (-1 to 1)
    var leftX = pad.leftX()
    var leftY = pad.leftY()

    # Right analog stick (-1 to 1)
    var rightX = pad.rightX()
    var rightY = pad.rightY()    

    # Dpad (0 or 1)
    var dpadUp = pad.dpadUp()
    var dpadDown = pad.dpadDown()
    var dpadLeft = pad.dpadLeft()
    var dpadRight = pad.dpadRight()

    # Buttons (0 or 1)
    var start = pad.Start()
    var leftStick = pad.leftThumbstick()
    var rightStick = pad.rightThumbstick()
    var a = pad.A()
    var b = pad.B()
    var x = pad.X()
    var y = pad.Y()
    var leftBumper = pad.leftBumper()
    var rightBumper = pad.rightBumper()

    # Triggers (0 to 1)
    var leftTrigger = pad.leftTrigger()
    var rightTrigger = pad.rightTrigger()
