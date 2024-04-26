# PiCW
A morse code keyer running on Raspberry Pi
by Kawamata Yoshihiro  [github.com/ykaw/PiCW](https://github.com/ykaw/PiCW/tree/master)

### MODIFIED by slowrunner to output audio to RPi audio jack
(It clicks like crazy but it works - pulseaudio underrun errors surpressed)
- Created/copied InputOutputPort_AudioJack_RPi_GPIO.py to InputOutputPort.py 
- See bottom of README for other system changes


## GPIO ports
* Two input ports for iambic paddles
  * supporting mode A and mode B
  * bug key emulation
  * side swiper emulation

* An input port for straight key

* An output port for TX control

* The PWM output for side tone

## CLI interface on RPi
* send message
  * with keyboard
  * from text files
* record/replay keying  
(both computer and manual keying)
* training mode  
with arbitrary set of characters
* variable gap length between every letters  
(especially useful for training)
* enable/disable
  * iambic paddles
  * straight key
  * tx control line
  * side tone (also can change freq.)
  
# See also
* docs/schematic.txt - schematic diagram of GPIO ports
* Supporting GPIO libraries
  * [pigpio](http://abyz.me.uk/rpi/pigpio/)(recommended)
  * [RPi.GPIO](https://sourceforge.net/projects/raspberry-gpio-python/)


### Slowrunner Setup
```
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
sudo apt-get install python-dev 
sudo pip3 install pyaudio

sudo pip3 install pysinewave
```

*** PiCW ***  

- git clone https://github.com/ykaw/PiCW.git  
- cp InputOutputPort_RP_GPIO.py InputOutputPort.py  
- edit in pysinewave audio  


```
pi@HamPi:~/HamPi/projects/PiCW $ ./PiCW.py
Welcome to PiCW.py
  '?'   for the short help.
  <TAB> for command completion.

18.0WPM:?

=====[ PiCW.py commands ]======================================================
                                       |
number   : set speed                   |
"<", ">" : slower/faster               |
" "text  : transmit text directly      |
                                       |record [on|off|start: record keying
tx [off|on]         : TX control line  |       |stop]
beep [off|on|freq]  : side tone        |play [speed]        : replay keying
straight [off|on]   : straight key     |training <CHARTYPES>: training mode
paddle [off|iambic|iambic-rev|bug|     |show                : display settings
        bug-rev|sideswiper]            |speed [WPM|CPM|QRS] : toggle speed unit
                    : paddle action    |lettergap [gapratio]: letter gap length
iambic [a|b]        : iambic mode      |load <file_name>    : load config
kb                  : keyboard transmit|help                : display help
xmit <file_name> ...: file transmit    |?                   : display this
                                       |quit, exit, bye     : exit from PiCW.py
                                       |
==========================================[ Type 'help' for more details ]=====

```


*** pulseaudio underrun  

sudo nano /etc/pulse/default.pa  

```
### Automatically load driver modules depending on the hardware available
# .ifexists module-udev-detect.so
# load-module module-udev-detect tsched=0
# .else
### Use the static hardware detection module (for systems that lack udev support)
# load-module module-detect
# .endif

### Alan get rid of underrun
load-module module-udev-detect tsched=0

$ pulseaudio -k
$ pulseaudio --start
```

*** too loud  
alsamixer  
- down arrow to about 50  
- Esc  

