# HamPi
Collection of Amateur Radio (Ham) Programs for Raspberry Pi


2024-04-26: Setup Pi3B as HamPi  

* Installed PiOS Legacy 32-bit Bullseye  
- Configured for 2.4GHz WiFi  (Pi3B)  
- added ipv6.disable=1 at end of cmdline.txt  


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

