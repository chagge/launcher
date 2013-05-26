import os
def idx2str(i):
	prefix = ''
	if i >= 0 and i < 10:
		prefix = 's00'
	elif i >= 10 and i < 100:
		prefix = 's0'
	elif i >= 100 and i < 1000:
		prefix = 's'
	else:
		print('idx2str: index is out of range [0, 1000)')
		sys.exit(-1)
	return prefix + str(i)

def BuildCommandList(n):
	cmds = []
	for i in range(0, n):
		cmds.append(idx2str(i))
	return cmds

def GenBNF(cmds, BNF):
	fd = open(BNF, 'w+')
	buf = '$command = ' + ' | \n'.join(cmds) + ';\n' + '($command)\n'
	fd.write(buf)
	fd.close()

def BNF2SLF(BNF, SLF):
	os.system('HParse {0} {1}'.format(BNF, SLF))

def GenDICT(cmds, DICT):
	fd = open(DICT, 'w+')
	for cmd in cmds:
		buf = cmd + '\t' + cmd + '\n'
		fd.write(buf)
	fd.close()

def GenMLF(cmds, MLF):
	fd = open(MLF, 'w+')
	fd.write('#!MLF!#\n')
	for cmd in cmds:
		buf = '"*/{0}.lab"\n{1}\n.\n'.format(cmd, cmd)
		fd.write(buf)
	fd.close()
