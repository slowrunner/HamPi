# CwUtilities - misc functions, etc... 

import sys
import tty
import termios
import KeyingControl   as key

# do something when any key typed
#     charfunc called when any key typed.
#     endfunc checks end condition
#     and termination process.
#
def with_keytyping(charfunc, endfunc):
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while True:
            ch=sys.stdin.read(1)
            if endfunc(ch):
                break
            else:
                charfunc(ch)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

# speed unit to display
#
speed_unit='WPM' # Use wpm as default

# return speed string to display
#
def speedstr():
    if speed_unit=='CPM':
        return "{:.1f}CPM".format(5.0*key.getspeed())
    elif speed_unit=='QRS':
        if key.dotlen<1.0:
            return "QRS{:.3f}".format(key.dotlen)
        else:
            return "QRS{:g}".format(key.dotlen)
    else:
        return "{:.1f}WPM".format(key.getspeed())

# conver user's input string to float
#
def speed2float(speed):
    if speed_unit=='CPM':
        return float(speed)/5.0
    elif speed_unit=='WPM':
        return float(speed)
    elif speed_unit=='QRS':
        return float(60/(50*float(speed)))

# simple progressbar
#
class ProgressBar():

    def __init__(self, maxbarlen, maxval):
        self.maxbarlen=maxbarlen  # character length of 100%
        self.maxval=maxval        # max vaules to handle
        self.barlen=0             # current filled length

    # setup scale
    #
    def begin(self):
        if 1<=self.maxbarlen:
            print('|', '-' * self.maxbarlen, '|', sep='')
            print('|', end='')
            sys.stdout.flush()

    # returns number of characters since last update
    #
    def diff(self, val):
        newbarlen=int(self.maxbarlen*val/self.maxval)
        diffval=newbarlen-self.barlen
        self.barlen=newbarlen
        return diffval

    # update bars to val
    #
    def update(self, val):
        if 1<=self.maxbarlen:
            print('*' * self.diff(val), end='')  # add new stars since last update
            sys.stdout.flush()

    # complete progress bar
    #
    def end(self, fullfill=False):
        if 1<=self.barlen:
            print(('*' if fullfill else ' ') * self.diff(self.maxval), '|', sep='')
