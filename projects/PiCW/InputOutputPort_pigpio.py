# InputOutputPort_pigpio - interface to sense/control hardware port

# This module uses pigpio library.
#   http://abyz.me.uk/rpi/pigpio/
#
import pigpio

# connect to pigpiod daemon
#
pi=pigpio.pi()
if not pi.connected:
    exit()

# definition of ports
#   The numbers are Broadcom's GPIO number of BCM2835,
#   not RPi's assigned numbers.
#
In_A=23
In_B=24
In_C=25

Out_T=22  # TX Control line
Out_M=18  # PWM output - for side tone

# initialization of input ports
#
for port in [In_A, In_B, In_C]:
    pi.set_mode(port, pigpio.INPUT)

    # Input will be pulled-up.
    # So, to mark input port,
    # that pin should be contacted to GND,
    # via a current-limit resistor.
    #
    pi.set_pull_up_down(port, pigpio.PUD_UP)

    # anti-chattering
    # The tolerance is 3ms.
    #
    pi.set_glitch_filter(port, 3000)

# and initialization of output ports
#
pi.set_mode(Out_T, pigpio.OUTPUT)

Freq_M=1500 # side tone frequency (Hz)
pi.set_mode(Out_M, pigpio.OUTPUT)
pi.hardware_PWM(Out_M, Freq_M, 0)
pi.set_PWM_frequency(Out_M, Freq_M)

# activate TX control line
#
def txline_on():
    pi.write(Out_T, 1)

# deactivate TX control line
#
def txline_off():
    pi.write(Out_T, 0)

# activate side tone
#
def beep_on():
    pi.set_PWM_dutycycle(Out_M, 128)

# deactivate side tone
#
def beep_off():
    pi.set_PWM_dutycycle(Out_M, 0)

# get side tone frequency
#
def get_beepfreq():
    return pi.get_PWM_frequency(Out_M)

# set side tone frequency
#
def set_beepfreq(hz):
    pi.set_PWM_frequency(Out_M, hz)
    pi.set_PWM_dutycycle(Out_M, 0)

# get available side tone frequencies
#
def get_avail_beepfreq():
    saved_freq=get_beepfreq()

    set_beepfreq(50000)    # try too high freq
    hi_freq=get_beepfreq() # get actual result

    set_beepfreq(saved_freq)  # restore saved setting

    return [int(hi_freq/div_ratio+0.5)
            for div_ratio in [1, 2, 4, 5, 8,
                              10, 16, 20, 25, 32, 40, 50, 80,
                              100, 160, 200, 400, 800]]

# check current port status
#
def check_port(port):
    import KeyingControl as key

    if pi.read(port)==0:
        return key.PRESSED
    else:
        return key.RELEASED

# table for callback functions by every input port
#   empty at initial state
#
cb={}

# bind callback function to input port
#   This function is interface between pigpio and our
#   abstraction layer.
#
#   func is a function which has only parameter: func(state)
#
def bind(in_port, func):
    import KeyingControl as key

    if in_port in cb:
        cb[in_port].cancel()  #  unassign current callback if any

    cb[in_port]=pi.callback(in_port,
                            pigpio.EITHER_EDGE,
                            lambda p, s, t: func(key.PRESSED
                                                 if s==0
                                                 else key.RELEASED))

# termination process for this module
#
def terminate():

    # set output to low level
    txline_off()
    beep_off()

    # unbound all callbacks
    #
    for in_port in cb.keys():
        if in_port in cb:
            cb[in_port].cancel()

    # close connection to pigpiod
    #
    pi.stop()
