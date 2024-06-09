#!/usr/bin/env python3

import pyaudio
import math

from ctypes import *
from contextlib import contextmanager

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)



def tone( freq , length): 

    bit_rate = 16000 #number of frames per second/frameset.      

    frequency = freq #in Hz, waves per second
    play_time = length #in seconds to play sound

    if frequency > bit_rate:
        bit_rate = frequency+100

    num_frames = int(bit_rate * play_time)
    total_frames = num_frames % bit_rate
    wave_info = ''    

    for x in range(num_frames):
     wave_info = wave_info+chr(int(math.sin(x/((bit_rate/frequency)/math.pi))*127+128))    

    for x in range(total_frames): 
     wave_info = wave_info+chr(128)

    with noalsaerr():
        p = PyAudio()
    stream = p.open(format = p.get_format_from_width(1), 
                    channels = 1, 
                    rate = bit_rate, 
                    output = True)

    stream.write(wave_info)
    stream.stop_stream()
    stream.close()
    p.terminate()



if __name__ == '__main__':
    frequency = 750 #Hz
    duration = 0.1   #seconds

    # PyAudio = pyaudio.PyAudio

    #Function to play frequency for given duration
    tone(frequency , duration)

