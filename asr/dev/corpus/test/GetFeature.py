#!/usr/bin/python
import os, sys

cmd = './genList.py > list.txt'
print(cmd)
os.system(cmd)

# convert wav to htk format
cmd = 'cat list.txt | ./wav2htk.py'
print(cmd)
os.system(cmd)

cmd = 'cat list.txt | ./genSCP.py > hcopy.scp'
print(cmd)
os.system(cmd)

cmd = './hcopy.py'
print(cmd)
os.system(cmd)
