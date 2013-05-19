#!/usr/bin/python
import sys, os

wlist = []
for l in sys.stdin.readlines():
	if l.strip() != '':
		wlist.append(l.strip())

nWord = len(wlist)

sys.stdout.write('N={} L={}\n'.format(str(nWord+2), str(nWord*2)));

# node
for i in range(0, nWord):
	sys.stdout.write('I={} W={}\n'.format(str(i), wlist[i]))

S = nWord    # start node index
E = nWord+1  # end node index

sys.stdout.write('I={} W=!NULL\n'.format(str(S)))
sys.stdout.write('I={} W=!NULL\n'.format(str(E)))

# arc
a = 0
for n in range(0, nWord):
	sys.stdout.write('J={} S={} E={}\n'.format(str(a), str(S), str(n)))
	a+=1

for n in range(0, nWord):
	sys.stdout.write('J={} S={} E={}\n'.format(str(a), str(n), str(E)))
	a+=1
