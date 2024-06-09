# HamPi
Collection of Amateur Radio (Ham) Programs for Raspberry Pi

- PiCW
- JS8Call
- WSJT-X


2024-06-09: Doc VNC Server, JS8Call and WSJT-X



* Installed PiOS Legacy 32-bit Bullseye  
- Configured for 2.4GHz WiFi  (Pi3B)  
- added ipv6.disable=1 at end of cmdline.txt  
- VNC Server setup


# *** PiCW ***  


```
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
sudo apt-get install python-dev 
sudo pip3 install pyaudio

sudo pip3 install pysinewave
```


- git clone https://github.com/ykaw/PiCW.git  
- cp InputOutputPort_RP_GPIO.py InputOutputPort.py  
- edit in pysinewave audio  


### Running PiCW

```
pi@HamPi:~ $ cd HamPi
pi@HamPi:~ $ ./PiCW.sh
or
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



## === Configuring vncserver

```
sudo raspi-config
Display Options->1920x1080
Enable VNC
Reboot Now? Yes


sudo cp /root/.vnc/config.d/vncserver-x11 /home/pi/.vnc/config.d/root_.vnc_config.d_vncserver-x11
cp .vnc/config.d/root_.vnc_config.d_vncserver-x11 .vnc/config.d/vncserver-x11


nano /home/pi/.vnc/config.d/vncserver-x11
add to file:
Authentication=VncAuth
Encryption=PreferOff

sudo cp .vnc/config.d/vncserver-x11 /root/.vnc/config.d/vncserver-x11
sudo vncpasswd -service
sudo systemctl restart vncserver-x11-serviced.service
vncserver-virtual :1 -geometry 1920x1080 -depth 24 -Authentication VncAuth -Encryption PreferOff -SecurityTypes StandardUser

TigerVNC



sudo systemctl status vncserver-x11-serviced.service 
● vncserver-x11-serviced.service - VNC Server in Service Mode daemon
     Loaded: loaded (/lib/systemd/system/vncserver-x11-serviced.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2024-06-08 21:49:12 EDT; 9min ago
   Main PID: 510 (vncserver-x11-s)
      Tasks: 5 (limit: 1595)
        CPU: 1.418s
     CGroup: /system.slice/vncserver-x11-serviced.service
             ├─510 /usr/bin/vncserver-x11-serviced -fg
             ├─532 /usr/bin/vncserver-x11-core -service
             ├─577 /usr/bin/vncagent service 0
             ├─898 /usr/bin/vncserverui service 0
             └─907 /usr/bin/vncserverui -statusicon 0

Jun 08 21:49:12 HamPi systemd[1]: Started VNC Server in Service Mode daemon.
Jun 08 21:49:13 HamPi vncserver-x11[532]: ServerManager: Server started
Jun 08 21:49:14 HamPi vncserver-x11[532]: ConsoleDisplay: Cannot find a running X server on vt1
Jun 08 21:49:14 HamPi vncserver-x11[532]: ConsoleDisplay: Found running X server (pid=552, binary=/usr/lib/xorg/Xorg)
Jun 08 21:57:07 HamPi vncserver-x11[532]: Connections: connected: 10.0.0.129::61001 (TCP)       <--- Splat-K  
Jun 08 21:57:07 HamPi vncserver-x11[532]: Connections: disconnected: 10.0.0.129::61001 (TCP) ([ConnFailed] No configured security type is supported by 3.3 VNC Viewer)

Jun 08 22:14:38 HamPi vncserver-x11[6311]: Connections: connected: 10.0.0.129::61007 (TCP)    <---- TigerVNC
Jun 08 22:14:45 HamPi vncserver-x11[6311]: Connections: authenticated: 10.0.0.129::61007 (TCP), as (anonymous) (d permissions)
Jun 08 22:30:56 HamPi vncserver-x11[6311]: Connections: disconnected: 10.0.0.129::61007 (TCP) ([EndOfStream] Disconnection by client)
```


# === JS8Call ===

### Installation
- sudo apt install js8call

### Running

TigerVNC into 10.0.0.xx
Terminal: pi@HamPi:~ $ js8call


- Set for Kenwood TS440S on COM3, audio to QMX device

- Log Dir:  /home/pi/.local/share/JS8Call


# === WSJT-X

### Installation
- sudo apt install wsjtx


### Running 
TigerVNC into 10.0.0.xxx
Terminal: pi@HamPi:~ $ wsjtx


- Set for Kenwood TS440S on COM3, audio to QMX device
