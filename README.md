# xbox2midi

Python script intended for Linux / Raspberry Pi use.  Converts XBox 360 controller inputs into MIDI commands.

## Getting Started

### Prerequisites

[Xbox.py](https://github.com/FRC4564/Xbox)

[Mido](https://github.com/mido/mido)

[rtmidi](https://github.com/thestk/rtmidi)

### Installing

1. [Follow installation instructions for xbox.py](https://github.com/FRC4564/Xbox), download and put the xbox.py file in the same folder as xbox2midi.py

2. Install Mido
```
pip install mido
```

3. Install rtmidi
```
pip install python-rtmidi
```

### Usage

You will most likely need to edit the script to get the functionality you want.

I set this up to control a DSI Tetra synthesizer, so consult the manual of your MIDI device to find the CC values you want to control, and update the script accordingly.

### Default controls

* Start Button - toggle note on/off
* Back Button - exits program

* Left Stick (x-axis) - OSC 1 shape
* Left Stick (y-axis) - OSC 1 pitch
* Right Stick (x-axis) - OSC 2 shape
* Right Stick (y-axis) - OSC 2 pitch
* Left Stick (pressed) - toggle up/down direction of OSC 1 pitch
* Right Stick (pressed) - toggle up/down direction of OSC 2 pitch

* Left Trigger - OSC 1 fine pitch
* Right Trigger - OSC 2 fine pitch
* Left Bumper - toggle up/down direction of OSC 1 fine pitch
* Right Bumper - toggle up/down direction of OSC 2 fine pitch

* D-Pad (up) - octave up
* D-Pad (down) - octave down
* D-Pad (left) - note down
* D-Pad (right) - note up

* A - note change: down a third (4 half steps)
* B - note change: up a third (4 half steps)
* X - note change: down a fifth (7 half steps)
* Y - note change: up a fifth (7 half steps)

## Author

jmbiggs, [jmbiggsdev@gmail.com](mailto:jmbiggsdev@gmail.com)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
