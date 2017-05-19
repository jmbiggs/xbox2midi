import xbox
import mido

from mido import Message

class button:
    holding = False
    
    def __init__(self, description, get_button_down):
        self.description = description
        self.get_button_down = get_button_down    

class joystick:
    def __init__(self, description, get_value):
        self.description = description
        self.get_value = get_value

# define buttons
dpadUp = button("dpad up", "pad.dpadUp()")
dpadDown = button("dpad down", "pad.dpadDown()")
dpadLeft = button("dpad left", "pad.dpadLeft()")
dpadRight = button("dpad right", "pad.dpadRight()")
start = button("start", "pad.Start()")
leftStick = button("left stick button", "pad.leftThumbstick()")
rightStick = button("right stick button", "pad.rightThumbstick()")
a = button("a", "pad.A()")
b = button("b", "pad.B()")
x = button("x", "pad.X()")
y = button("y", "pad.Y()")
leftBumper = button("left bumper", "pad.leftBumper()")
rightBumper = button("right bumper", "pad.rightBumper()")

# define analog joysticks
leftX = joystick("left X", "pad.leftX()")
leftY = joystick("left Y", "pad.leftY()")
rightX = joystick("right X", "pad.rightX()")
rightY = joystick("right Y", "pad.rightY()")
leftTrigger = joystick("left trigger", "pad.leftTrigger()")    
rightTrigger = joystick("right trigger", "pad.rightTrigger()")

buttons = [dpadUp, dpadDown, dpadLeft, dpadRight, start, leftStick, rightStick, a, b, x, y, leftBumper, rightBumper]
joysticks = [leftX, leftY, rightX, rightY, leftTrigger, rightTrigger]

def convert_input_to_midi():
    # handle buttons
    for button in buttons:    
        if button.holding:
            # check if it is still actually holding
            if not eval(button.get_button_down):
                button.holding = False    
        else:
            # see if it is being pressed (for the first time)
            if eval(button.get_button_down):
                print button.description
                button.holding = True
    
    # handle analog sticks
    for joystick in joysticks:
        current_value = eval(joystick.get_value)
        if current_value >= 0.1 or current_value <= -0.1:
            print joystick.description, ":", current_value
    
def print_connected(connected):
    if connected:
        print "Controller Connected"
    else:
        print "Controller Disconnected"

def print_port(port):
    if port.closed:
        print "MIDI port closed"
    else:
        print "MIDI port open, connected to: ", port.name

if __name__ == "__main__":
    print "xbox2midi running: Press Back button to exit"

    pad = xbox.Joystick()
    connected = pad.connected()
    print_connected(connected)

    port = mido.open_output('DSI Tetra:DSI Tetra MIDI 1 20:0')
    port_open = not port.closed
    print_port(port)

    #print mido.get_output_names()
    msg = Message('note_on', note=60)
    port.send(msg)

    # Loop until back button is pressed
    while not pad.Back():
        # show connection status
        was_connected = connected
        connected = pad.connected()
        if was_connected != connected:
            print_connected(connected)

        # show port status
        was_open = port_open
        port_open = not port.closed
        if was_open != port_open:
            print_port(port)

        # run conversions on inputs
        convert_input_to_midi()

    # Close out when done
    pad.close()
    port.reset()
    port.close()
