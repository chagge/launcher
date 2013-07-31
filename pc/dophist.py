#!/usr/bin/python
from Tkinter import *
import subprocess
import signal
import os
import time

ASR_ROOT = '/home/jiayu/dophist/launcher/pc/ASR_ROOT'

BIN = os.path.join(ASR_ROOT, 'bin')
REC = os.path.join(BIN, 'rec')
VAD = os.path.join(BIN, 'vad')
HCOPY = 'HCopy'
HCOPY_CFG = os.path.join(BIN, 'hcopy.cfg')

Sox_SampleRate = '8000'
Sox_NumChannels = '1'
Sox_BufferSize = '100'   # buffer size(in samples)

NumEMIter = 3

curtag = ''
PidRec = 0
recAudio = os.path.join(ASR_ROOT, 'decode', 'audio.htk')

def create(tag):
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag))
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag, 'utt'))
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag, 'utt', 'raw'))
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag, 'utt', 'vad'))
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag, 'utt', 'fea'))
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag, 'am'))
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag, 'am', 'proto'))
    for i in range(0, NumEMIter+1):  # [0, NumEMIter]
        os.mkdir(os.path.join(ASR_ROOT, 'train', tag, 'am', 'iter'+str(i)))
 
#def addUtterToTag(audio, tag):

def train(tag):
    tagRoot = os.path.join(ASR_ROOT, 'train', tag)
    # amlist
    fd = open(os.path.join(tagRoot, 'amlist'), 'w+')
    fd.write(tag + '\n')
    fd.close()
    # dict
    fd = open(os.path.join(tagRoot, 'dict'), 'w+')
    fd.write(tag + '\t' + tag + '\n')
    fd.close()
    # mlf
    fd = open(os.path.join(tagRoot, 'mlf'), 'w+')
    buf = '\n'.join([
        '#!MLF!#',
        '"{}"'.format(os.path.join(tagRoot,'utt','fea','*.lab')),
        tag,
        '.'
        ])
    fd.write(buf)
    fd.close()

    # VAD: raw -> vad
    for f in os.listdir(os.path.join(tagRoot, 'utt', 'raw')):
        cmd = ' '.join([
                VAD,
                os.path.join(tagRoot, 'utt', 'raw', f),
                os.path.join(tagRoot, 'utt', 'vad', f)
                ])
        print(cmd)
        os.system(cmd)

    # feature extraction: vad -> fea 
    hcopy_scp = os.path.join(tagRoot, 'utt', 'hcopy.scp')
    fd = open(hcopy_scp, 'w+')
    for f in os.listdir(os.path.join(tagRoot, 'utt', 'vad')):
        [name, ext] = f.split('.')
        buf = ' '.join([
            os.path.join(tagRoot, 'utt', 'vad', f),
            os.path.join(tagRoot, 'utt', 'fea', name+'.mfc'),
            '\n'
            ])
        fd.write(buf)
    fd.close()
    cmd = ' '.join([
        HCOPY,
        '-A',
        '-D',
        '-T', '3',
        '-C', HCOPY_CFG,
        '-S', hcopy_scp,
        ])
    os.system(cmd)

    # train.scp
    train_scp = os.path.join(tagRoot, 'train.scp')
    fd = open(train_scp, 'w+')
    for f in os.listdir(os.path.join(tagRoot, 'utt', 'fea')):
        fd.write(os.path.join(tagRoot, 'utt', 'fea', f) + '\n')
    fd.close()

def remove(tag):
    os.system('rm -rf ' + os.path.join(ASR_ROOT, 'train', tag))

def recognize(audio):
    pass

def run(tag):
    os.system('python ' + os.path.join(ASR_ROOT, 'train', tag, 'op.py'))

def updateASR():
    pass

def LPressCallback(event):
    cmd = [
        REC,
        '-r' , Sox_SampleRate,
        '-c',  Sox_NumChannels,
        '--buffer', Sox_BufferSize,
        recAudio
        ]
    p = subprocess.Popen(cmd)
    PidRec = p.pid

def LReleaseCallback(event):
    os.kill(PidRec, signal.SIGINT)
    t = recognize(recAudio)
    run(t)

def RPressCallback(event):
    global curtag, PidRec
    curtag = 'T' + str(int(time.time()))
    create(curtag)
    utt = os.path.join(ASR_ROOT, 'train', curtag, 'utt', 'raw', curtag+'.htk')
    cmd = [
        REC,
        '-r' , Sox_SampleRate,
        '-c',  Sox_NumChannels,
        '--buffer', Sox_BufferSize,
        utt
        ]
    p = subprocess.Popen(cmd)
    PidRec = p.pid

def RReleaseCallback(event):
    global curtag, PidRec
    os.kill(PidRec, signal.SIGINT)
    #os.system('kill -s 2 ' + str(PidRec))
    train(curtag)
    updateASR()

root = Tk()

frame = Frame(root, width=180, height=180)
frame.pack()
frame.bind("<Button-1>", LPressCallback)
frame.bind("<ButtonRelease-1>", LReleaseCallback)
frame.bind("<Button-3>", RPressCallback)
frame.bind("<ButtonRelease-3>", RReleaseCallback)

root.mainloop()
