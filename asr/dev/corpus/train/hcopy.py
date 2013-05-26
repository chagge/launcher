#!/usr/bin/python
from os import system

CFG='hcopy.cfg'
SCP='hcopy.scp'

system('HCopy -A -D -T 3 -C ' + CFG + ' -S ' + SCP)
