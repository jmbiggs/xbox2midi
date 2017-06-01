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

    def flip_toggle(self):
        self.toggle = not self.toggle

class MidiConverter:
    note_is_on = False
    current_note = 48

    def __init__(self, ports, pad):
        self.ports = ports
        self.pad = pad
        
        # define analog joysticks
        self.leftX = Joystick("left X", "pad.leftX()", Message('control_change', control=OSC_1_SHAPE))
        self.leftY = Joystick("left Y", "pad.leftY()", Message('control_change', control=OSC_1_PITCH))
        self.rightX = Joystick("right X", "pad.rightX()", Message('control_change', control=OSC_2_SHAPE))
        self.rightY = Joystick("right Y", "pad.rightY()", Message('control_change', control=OSC_2_PITCH))
        self.leftTrigger = Joystick("left trigger", "pad.leftTrigger()", Message('control_change', control=OSC_1_FINE))
        self.rightTrigger = Joystick("right trigger", "pad.rightTrigger()", Message('control_change', control=OSC_2_FINE))

        # define buttons
        dpadUp = Button("dpad up", "pad.dpadUp()", lambda: self.change_note(12))
        dpadDown = Button("dpad down", "pad.dpadDown()", lambda: self.change_note(-12))
        dpadLeft = Button("dpad left", "pad.dpadLeft()", lambda: self.change_note(-1))
        dpadRight = Button("dpad right", "pad.dpadRight()", lambda: self.change_note(1))
        start = Button("start", "pad.Start()", lambda: self.toggle_note_on_off())
        leftStick = Button("left stick button", "pad.leftThumbstick()", lambda: self.leftY.flip_toggle())
        rightStick = Button("right stick button", "pad.rightThumbstick()", lambda: self.rightY.flip_toggle())
        a = Button("a", "pad.A()", lambda: self.change_note(-4))
        b = Button("b", "pad.B()", lambda: self.change_note(4))
        x = Button("x", "pad.X()", lambda: self.change_note(-7))
        y = Button("y", "pad.Y()", lambda: self.change_note(7))
        leftBumper = Button("left bumper", "pad.leftBumper()", lambda: self.leftTrigger.flip_toggle())
        rightBumper = Button("right bumper", "pad.rightBumper()", lambda: self.rightTrigger.flip_toggle())
        
        self.buttons = [dpadUp, dpadDown, dpadLeft, dpadRight, start, leftStick, rightStick, a, b, x, y, leftBumper, rightBumper]
        self.pitch_joysticks = [self.leftX, self.leftY, self.rightX, self.rightY]
        self.fine_joysticks = [self.leftTrigger, self.rightTrigger]

    # helper functions
    def change_note(self, amount):
        new_note = self.current_note + amount

        if new_note < 0 or new_note > 127:
            return

        for port in self.ports:
            port.send(Message('note_off', note=self.current_note))
        self.current_note = new_note
        for port in self.ports:
            port.send(Message('note_on', note=self.current_note))

    def toggle_note_on_off(self):
        self.note_is_on = not self.note_is_on
        if (self.note_is_on):
            for port in self.ports:
                port.send(Message('note_on', note=self.current_note))
        else:
            for port in self.ports:
                port.send(Message('note_off', note=self.current_note))

    def print_connected(self, connected):
        if connected:
            print "Controller Connected"
        else:
            print "Controller Disconnected"

    def print_ports(self):
        for port in self.ports:
            if port.closed:
                print "MIDI port closed"
            else:
                print "MIDI port open, connected to: ", port.name

    # main function
    def convert_input_to_midi(self):
        # handle buttons
        for button in self.buttons:    
            if button.holding:
                # check if it is still actually holding
                if not eval(button.get_button_down):
                    button.holding = False    
            else:
                # see if it is being pressed (for the first time)
                if eval(button.get_button_down):
#                    print button.description
                    if button.action is not None:
                        button.action()
                    button.holding = True
        
        # handle analog sticks
        for joystick in self.pitch_joysticks:
            current_value = eval(joystick.get_value)
#            print joystick.description, ":", current_value
            if not joystick.toggle:
                message = joystick.message
                if message is not None:
                    if current_value < 0:
                        message.value = (int)(abs(64 - (abs(current_value) * 63)))
                    else:
                        message.value = (int)(current_value * 63 + 64)
                    for port in self.ports:
                        port.send(message)
                
        for joystick in self.fine_joysticks:
            current_value = eval(joystick.get_value)
#            print joystick.description, ":", current_value
            message = joystick.message
            if message is not None:
                if not joystick.toggle:
                    message.value = (int)(current_value * 63 + 64)
                else:
                    message.value = (int)(abs(64 - (abs(current_value) * 63)))
                for port in self.ports:
                    port.send(message)
    
if __name__ == "__main__":
    print "xbox2midi running: Press Back button to exit"

    pad = xbox.Joystick()
    ports = []
    for port_name in mido.get_output_names():
        ports.append(mido.open_output(port_name))
    converter = MidiConverter(ports, pad)

    connected = converter.pad.connected()
    converter.print_connected(connected)

    ports_open = []
    for port in ports:
        ports_open.append(not port.closed)
    converter.print_ports()

    # Loop until back button is pressed
    while not converter.pad.Back():
        # show connection status
        was_connected = connected
        connected = converter.pad.connected()
        if was_connected != connected:
            converter.print_connected(connected)

        # show port status
        was_open = port_open
        ports_open = []
        for port in converter.ports:
            ports_open.append(not port.closed)
        for index in range(len(ports_open)):
            if was_open[index] != ports_open[index]:
                converter.print_port()

        # run conversions on inputs
        converter.convert_input_to_midi()

    # Close out when done
    converter.pad.close()
    for port in converter.ports:
        port.reset()
        port.close()
