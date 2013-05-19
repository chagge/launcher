#!/usr/bin/python

import os

os.system('ls wav > tmp')

for nameext in open('tmp', 'r').readlines():
	name, ext = os.path.splitext(nameext)
	print(name)

os.system('rm tmp')
