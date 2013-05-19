#!/usr/bin/python

import os
from sys import stdin, stdout, exit

def idx2str(i):
	prefix = ''
	if i > 0 and i < 10:
		prefix = 's00'
	elif i < 100:
		prefix = 's0'
	elif i < 1000:
		prefix = 's'
	else:
		print('idx2str: index is out of range (0, 1000)')
		sys.exit(-1)
	return prefix + str(i)

i = 0
for l in stdin.readlines():
	i = i + 1
	stdout.write(idx2str(i) + '\t' + l.strip() + '\n')
