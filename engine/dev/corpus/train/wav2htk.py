#!/usr/bin/python
import os, sys

for l in sys.stdin.readlines():
	name = l.strip()
	if name != '':
		cmd = ' '.join([
					'sox', 
					os.path.join('wav', name+'.wav'),
					os.path.join('htk', name+'.htk'),
					'rate 8k'
					])
		os.system(cmd)

