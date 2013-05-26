#!/usr/bin/python
import os, sys

for l in sys.stdin.readlines():
	name = l.strip()
	if name == '':
		continue
	sys.stdout.write(
			os.path.join('htk', name+'.htk') + '\t' + 
			os.path.join('mfc', name+'.mfc') + '\n')

