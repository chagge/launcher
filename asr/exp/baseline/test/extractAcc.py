#!/usr/bin/python
import os,sys
d = 'reclogs'
N = 100
for n in range(1, N+1):
	lines = open(d + '/acc'+str(n)+'.txt', 'r').readlines()
	l = lines[-2]
	acc = l.strip().split(',')[0].split('=')[-1]
	sys.stdout.write(str(n) + '\t' + str(acc) + '\n')
