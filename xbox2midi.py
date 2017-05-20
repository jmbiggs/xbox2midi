import xbox
import mido
from mido import Message

# define control change (CC) message values
OSC_1_PITCH = 20
OSC_2_PITCH = 24
OSC_1_FINE = 21
OSC_2_FINE = 25
OSC_1_SHAPE = 22
OSC_2_SHAPE = 26

class Button:
    holding = False
    
    def __init__(self, description, get_button_down, action):
        self.description = description
        self.get_button_down = get_button_down
        self.action = action

class Joystick:
    toggle = False
    
    def __init__(self, description, get_value, message):
        self.description = description
        self.get_value = get_value
        self.message = message

class MidiConverter:
    # local variables to keep track of things
    note_is_on = False
    adjust_osc_1_pitch = False
    adjust_osc_2_pitch = False
    #osc_1_fine_ascending = True
    #osc_2_fine_ascending = True
    current_note = 48

    def __init__(self, port, pad):
        self.port = port
        self.pad = pad
        
        # define analog joysticks
        leftX = Joystick("left X", "pad.leftX()", Message('control_change', control=OSC_1_SHAPE))
        leftY = Joystick("left Y", "pad.leftY()", Message('control_change', control=OSC_1_PITCH))
        rightX = Joystick("right X", "pad.rightX()", Message('control_change', control=OSC_2_SHAPE))
        rightY = Joystick("right Y", "pad.rightY()", Message('control_change', control=OSC_2_PITCH))
        leftTrigger = Joystick("left trigger", "pad.leftTrigger()", Message('control_change', control=OSC_1_FINE))
        rightTrigger = Joystick("right trigger", "pad.rightTrigger()", Message('control_change', control=OSC_2_FINE))

        # define buttons
        dpadUp = Button("dpad up", "pad.dpadUp()", lambda note=current_note: change_note(note + 12))
        dpadDown = Button("dpad down", "pad.dpadDown()", lambda note=current_note: change_note(note - 12))
        dpadLeft = Button("dpad left", "pad.dpadLeft()", lambda note=current_note: change_note(note + 1))
        dpadRight = Button("dpad right", "pad.dpadRight()", lambda note=current_note: change_note(note - 1))
        start = Button("start", "pad.Start()", lambda: toggle_note_on_off())
        leftStick = Button("left stick button", "pad.leftThumbstick()", None) #lambda: adjust_osc_1_pitch = not adjust_osc_1_pitch)
        rightStick = Button("right stick button", "pad.rightThumbstick()", None) #lambda: adjust_osc_2_pitch = not adjust_osc_2_pitch)
        a = Button("a", "pad.A()", lambda note=current_note: change_note(note - 4))
        b = Button("b", "pad.B()", lambda note=current_note: change_note(note + 4))
        x = Button("x", "pad.X()", lambda note=current_note: change_note(note - 7))
        y = Button("y", "pad.Y()", lambda note=current_note: change_note(note + 7))
        leftBumper = Button("left bumper", "pad.leftBumper()", None) #lambda: leftTrigger.toggle = not leftTrigger.toggle)
        rightBumper = Button("right bumper", "pad.rightBumper()", None) # lambda: rightTrigger.toggle = not rightTrigger.toggle)
        
        self.buttons = [dpadUp, dpadDown, dpadLeft, dpadRight, start, leftStick, rightStick, a, b, x, y, leftBumper, rightBumper]
        self.pitch_joysticks = [leftX, leftY, rightX, rightY]
        self.fine_joysticks = [leftTrigger, rightTrigger]

    # helper functions
    def change_note(self, new_note):
        if new_note < 0 or new_note > 127:
            return

        port.send(Message('note_off', note=current_note))
        self.current_note = new_note
        port.send(Message('note_on', note=current_note))

    def toggle_note_on_off(self):
        self.note_is_on = not note_is_on
        if (note_is_on):
            port.send(Message('note_on', note=current_note))
        else:
            port.send(Message('note_off', note=current_note))

    def print_connected(self, connected):
        if connected:
            print "Controller Connected"
        else:
            print "Controller Disconnected"

    def print_port(self):
        if port.closed:
            print "MIDI port closed"
        else:
            print "MIDI port open, connected to: ", port.name

    # main function
    def convert_input_to_midi(self):
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
                    if button.action is not None:
                        print button.action
                        button.action()
                    button.holding = True
        
        # handle analog sticks
        for joystick in pitch_joysticks:
            current_value = eval(joystick.get_value)
    #        print joystick.description, ":", current_value
            message = joystick.message
            if message is not None:
                if current_value < 0:
                    message.value = (int)(abs(64 - (abs(current_value) * 63)))
                else:
                    message.value = (int)(current_value * 63 + 64)
                port.send(message)
                
        for joystick in fine_joysticks:
            current_value = eval(joystick.get_value)
    #        print joystick.description, ":", current_value
            message = joystick.message
            if message is not None:
                if not joystick.toggle:
                    message.value = (int)(current_value * 63 + 64)
                else:
                    message.value = (int)(abs(64 - (abs(current_value) * 63)))
                port.send(message)
    
if __name__ == "__main__":
    print "xbox2midi running: Press Back button to exit"

    pad = xbox.Joystick()
    port = mido.open_output('DSI Tetra:DSI Tetra MIDI 1 20:0')    
    converter = MidiConverter(port, pad)

    connected = converter.pad.connected()
    converter.print_connected(connected)

    port_open = not port.closed
    converter.print_port()

    # Loop until back button is pressed
    while not converter.pad.Back():
        # show connection status
        was_connected = connected
        connected = converter.pad.connected()
        if was_connected != connected:
            converter.print_connected(connected)

        # show port status
        was_open = port_open
        port_open = not converter.port.closed
        if was_open != port_open:
            converter.print_port()

        # run conversions on inputs
        converter.convert_input_to_midi()

    # Close out when done
    converter.pad.close()
    converter.port.reset()
    converter.port.close()
