#!/usr/bin/python
import os, sys

# CreateProto create a hmm proto file with following specifications:
# ns - number of states
# nd - feature vector dimension
def CreateHMMTopology(dirname, hmm, ns, nd,):
	fd = open(os.path.join(dirname, hmm), 'w+')#{{{
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
#}}}

for i in range(3, 11):
    os.system('rm -rf proto_{}'.format(i)) 
    os.system('mkdir proto_{}'.format(i)) 
    CreateHMMTopology('proto_{}'.format(i), 's000', i, 39)

    os.system('rm -rf hmm0_{}'.format(i)) 
    os.system('mkdir hmm0_{}'.format(i)) 
    os.system(' '.join([
            'HCompV',
            '-T', '1',
            '-m',
            '-S', 'train.scp',
            '-M', 'hmm0_{}'.format(i),
            'proto_{}/s000'.format(i)
            ]))
     
    os.system('rm -rf hmm1_{}'.format(i)) 
    os.system('mkdir hmm1_{}'.format(i)) 
    os.system(' '.join([
            'HERest',
            '-A',
            '-D',
            '-T', '1',
            '-I', 'train.mlf',
            '-S', 'train.scp',
            '-H', 'hmm0_{}/s000'.format(i),
            '-M', 'hmm1_{}'.format(i),
            '-s', 'hmm1_{}/stats'.format(i),
            '-m', '1',
            'hmmlist',
            '> hmm1_{}/logs'.format(i)
        ]))

