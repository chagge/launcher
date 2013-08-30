#!/usr/bin/python
import sys

BNF = sys.argv[1]
SLF = sys.argv[2]

tags = []
lines = open(BNF, 'r').readlines()
for l in lines:
  fields = l.strip().split()
  for f in fields:
    if f[0] == 'T':
      tags.append(f.strip(';'))

fo = open(SLF, 'w+')
NumTags = len(tags)
fo.write('N={} L={}\n'.format(NumTags+3, NumTags*2+1))
# nodes
fo.write('I=0 W=!NULL\n')
fo.write('I=1 W=!NULL\n')
fo.write('I=2 W=!NULL\n')
for i in range(3, NumTags+3):
  fo.write('I={} W={}\n'.format(i, tags[i-3]))

# links
l = 0
for n in range(3, NumTags+3):
  fo.write('J={} S={} E={}\n'.format(l, 0, n))
  l += 1
for n in range(3, NumTags+3):
  fo.write('J={} S={} E={}\n'.format(l, n, 1))
  l += 1

fo.write('J={} S=1 E=2\n'.format(l))

fo.close()

