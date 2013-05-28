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

def CreateBNF(cmds, BNF):
	fd = open(BNF, 'w+')
	buf = '$command = ' + ' | \n'.join(cmds) + ';\n' + '($command)\n'
	fd.write(buf)
	fd.close()

def BNF2SLF(BNF, SLF):
	os.system('HParse {0} {1}'.format(BNF, SLF))

def CreateDict(cmds, Dict):
	fd = open(Dict, 'w+')
	for cmd in cmds:
		buf = cmd + '\t' + cmd + '\n'
		fd.write(buf)
	fd.close()

def CreateMLF(cmds, MLF):
	fd = open(MLF, 'w+')
	fd.write('#!MLF!#\n')
	for cmd in cmds:
		buf = '"*/{0}.lab"\n{1}\n.\n'.format(cmd, cmd)
		fd.write(buf)
	fd.close()

# CreateProto create a hmm proto file with following specifications:
# ns - number of states
# nd - feature vector dimension
def CreateProto(hmm, ns, nd):
	fd = open('model/proto/'+hmm, 'w+')
	mean = ''
	var  = ''
	for k in range(0, nd):
		mean += '0.0 '
		var  += '1.0 '

	fd.write(''.join([
		'~o <VecSize> ' + str(nd) + ' <MFCC_E_D_A_Z>\n', 
		'~h "{}"\n'.format(hmm),
		'<BeginHMM>\n',
		'<NumStates> ' + str(ns) + '\n'
		]))

	for s in range(2, ns):  # first and last are non-emitting states
		fd.write(''.join([
			'<State> ' + str(s) + '\n',
			'\t<Mean> ' + str(nd) + '\n',
			'\t' + mean + '\n',
			'\t<Variance> ' + str(nd) + '\n',
			'\t' + var + '\n'
		]))

	# construct TransP
	fd.write('<TransP> ' + str(ns) + '\n')
	for s in range(0, ns):   # TransP matrix covers states [1,max]
		row = []
		for k in range(0, ns):
			row.append('0.0')

		if s == 0:
			row[1] = '1.0'
		elif s == ns-1:
			pass
		else:
			row[s]   = '0.9'
			row[s+1] = '0.1'
		fd.write('\t' + ' '.join(row) + '\n')
	fd.write('<EndHMM>\n')
	fd.close()

