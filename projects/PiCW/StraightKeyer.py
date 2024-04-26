# StraightKeyer - logic for a straight key

import InputOutputPort as port
import KeyingControl   as key
import TextKeyer       as txt

# callback function
#
def action(state):
    global pressing

    # almost pass-through
    #
    if state==key.PRESSED:
        key.mark()
        key.abort_request() # request to abort text keyer
        pressing=True
    elif state==key.RELEASED:
        key.space()
        pressing=False

# callback function to do nothing
#
def null_action(state):
    if state==key.PRESSED:
        key.abort_request()

# initialization
#
def getaction():
    return not not actstat  # to make return value to bool

def setaction(newact):
    global actstat

    if actstat != newact:
        actstat = not not newact
        if actstat:
            port.bind(port.In_C, action)
        else:
            port.bind(port.In_C, null_action)

actstat=False  # current status
setaction(True)

pressing=False
