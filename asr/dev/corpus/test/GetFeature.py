#!/usr/bin/python
import os, sys
os.system('ls wav > wav.list')
names = []
for namext in open('wav.list', 'r').readlines():
    name, ext = os.path.splitext(namext)
    names.append(name)

# soxing ms-wav to htk-wav
for name in names:
    cmd = ' '.join([
				'sox', 
				os.path.join('wav', name+'.wav'),
				os.path.join('htk', name+'.htk'),
				'rate 8k'
				])
    os.system(cmd)

# applying vad to htk_wav
for name in names:
    cmd = ' '.join([
				'../vad/vad', 
				os.path.join('htk', name+'.htk'),
				os.path.join('htk_vad', name+'.htk')
				])
    os.system(cmd)

# generate hcopy.scp
fd = open('hcopy.scp', 'w+')
for name in names:
    fd.write(os.path.join('htk_vad', name+'.htk') + '\t' +
            os.path.join('mfc_vad', name+'.mfc') + '\n')
fd.close()

# feature extraction
CFG='hcopy.cfg'
SCP='hcopy.scp'
os.system('HCopy -A -D -T 3 -C ' + CFG + ' -S ' + SCP)
