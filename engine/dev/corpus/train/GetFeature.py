#!/usr/bin/python
import os, sys

cmd = './GenList.py > NameList.txt'
print(cmd)
os.system(cmd)

# convert wav to htk format
cmd = 'cat NameList.txt | ./wav2htk.py'
print(cmd)
os.system(cmd)

cmd = 'cat NameList.txt | ./GenScp.py > hcopy.scp'
print(cmd)
os.system(cmd)

cmd = './hcopy.py'
print(cmd)
os.system(cmd)
