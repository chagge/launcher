#!/usr/bin/python
from Tkinter import *
import subprocess
import signal
import os

ASR_ROOT = '/home/jiayu/dophist/launcher/pc/ASR_ROOT'
BIN = os.path.join(ASR_ROOT, 'bin')
Sox_Record = os.path.join(BIN, 'rec')
Sox_SampleRate = '8000'
Sox_NumChannels = '1'
Sox_BufferSize = '100'
AudioFile = 'record.wav'
RecPid = 0

def StartRecord(event):
    cmd = [
        Sox_Record,
        '-r' , Sox_SampleRate,
        '-c',  Sox_NumChannels,
        '--buffer', Sox_BufferSize,
        AudioFile
        ]
    p = subprocess.Popen(cmd)
    RecPid = p.pid

def StopRecord(event):
    os.kill(RecPid, signal.SIGINT)
    #os.system('kill -s 2 ' + str(RecPid))

root = Tk()
frame = Frame(root, width=300, height=300)

#frame.bind("<Button-1>", Listen)
#frame.bind("<ButtonRelease-1>", Recognise)

frame.bind("<Button-3>", StartRecord)
frame.bind("<ButtonRelease-3>", StopRecord)

frame.pack()
root.mainloop()
