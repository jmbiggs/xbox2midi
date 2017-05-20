import xbox
import mido
from mido import Message

class button:
    holding = False
    
    def __init__(self, description, get_button_down, action):
        self.description = description
        self.get_button_down = get_button_down
        self.action = action

class joystick:
    toggle = False
    
    def __init__(self, description, get_value, message):
        self.description = description
        self.get_value = get_value
        self.message = message

# define control change (CC) message values
osc_1_pitch = 20
osc_2_pitch = 24
osc_1_fine = 21
osc_2_fine = 25
osc_1_shape = 22
osc_2_shape = 26

# define analog joysticks
leftX = joystick("left X", "pad.leftX()", Message('control_change', control=osc_1_shape))
leftY = joystick("left Y", "pad.leftY()", Message('control_change', control=osc_1_pitch))
rightX = joystick("right X", "pad.rightX()", Message('control_change', control=osc_2_shape))
rightY = joystick("right Y", "pad.rightY()", Message('control_change', control=osc_2_pitch))
leftTrigger = joystick("left trigger", "pad.leftTrigger()", Message('control_change', control=osc_1_fine))
rightTrigger = joystick("right trigger", "pad.rightTrigger()", Message('control_change', control=osc_2_fine))

# define buttons
dpadUp = button("dpad up", "pad.dpadUp()", lambda note=note: change_note(note + 12))
dpadDown = button("dpad down", "pad.dpadDown()", lambda note=note: change_note(note - 12)))
dpadLeft = button("dpad left", "pad.dpadLeft()", lambda note=note: change_note(note + 1)))
dpadRight = button("dpad right", "pad.dpadRight()", lambda note=note: change_note(note - 1)))
start = button("start", "pad.Start()", lambda: toggle_note_on_off())
leftStick = button("left stick button", "pad.leftThumbstick()", lambda: global adjust_osc_1_pitch = not adjust_osc_1_pitch)
rightStick = button("right stick button", "pad.rightThumbstick()", lambda: global adjust_osc_2_pitch = not adjust_osc_2_pitch)
a = button("a", "pad.A()", lambda note=note: change_note(note - 4))
b = button("b", "pad.B()", lambda note=note: change_note(note + 4))
x = button("x", "pad.X()", lambda note=note: change_note(note - 7))
y = button("y", "pad.Y()", lambda note=note: change_note(note + 7))
leftBumper = button("left bumper", "pad.leftBumper()", lambda: global leftTrigger.toggle = not leftTrigger.toggle)
rightBumper = button("right bumper", "pad.rightBumper()", lambda: global rightTrigger.toggle = not rightTrigger.toggle)

# global variables to keep track of things
note_is_on = False
adjust_osc_1_pitch = False
adjust_osc_2_pitch = False
#osc_1_fine_ascending = True
#osc_2_fine_ascending = True
current_note = 48

buttons = [dpadUp, dpadDown, dpadLeft, dpadRight, start, leftStick, rightStick, a, b, x, y, leftBumper, rightBumper]
pitch_joysticks = [leftX, leftY, rightX, rightY]
fine_joysticks = [leftTrigger, rightTrigger]

port = None
pad = None

# helper functions
def change_note(new_note):
    if new_note < 0 or new_note > 127:
        return

    port.send(Message('note_off', note=note))
    global note = new_note
    port.send(Message('note_on', note=note))

def toggle_note_on_off():
    note_is_on = not note_is_on
    if (note_is_on):
        port.send(Message('note_on', note=note))
    else:
        port.send(Message('note_off', note=note))

def print_connected(connected):
    if connected:
        print "Controller Connected"
    else:
        print "Controller Disconnected"

def print_port():
    if port.closed:
        print "MIDI port closed"
    else:
        print "MIDI port open, connected to: ", port.name

# main functions
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
#                print button.description
                eval(button.action)
                button.holding = True
    
    # handle analog sticks
    for joystick in pitch_joysticks:
        current_value = eval(joystick.get_value)
#        print joystick.description, ":", current_value
        message = joystick.get_message()
        if not message is None:
            if current_value < 0:
                message.value = (int)(abs(64 - (abs(current_value) * 63)))
            else:
                message.value = (int)(current_value * 63 + 64)
            port.send(message)
            
    for joystick in fine_joysticks:
        current_value = eval(joystick.get_value)
#        print joystick.description, ":", current_value
        message = joystick.get_message()
        if not message is None:
            if not joystick.toggle:
                message.value = (int)(current_value * 63 + 64)
            else:
                message.value = (int)(abs(64 - (abs(current_value) * 63)))
            port.send(message)
    
if __name__ == "__main__":
    print "xbox2midi running: Press Back button to exit"

    global pad = xbox.Joystick()
    connected = pad.connected()
    print_connected(connected)

    global port = mido.open_output('DSI Tetra:DSI Tetra MIDI 1 20:0')
    port_open = not port.closed
    print_port(port)

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
        convert_input_to_midi(port)

    # Close out when done
    pad.close()
    port.reset()
    port.close()
