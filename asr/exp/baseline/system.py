#!/usr/bin/python
import os, sys
#-----------------------------------------------#
#          parameter setting 
DB = '../corpus'				# database
MAXN = 100                       # first N utterence in DB
BNF = 'gram/gram.bnf'		# BNF defined grammar
SLF = 'gram/gram.slf'		# standard lattice file (SLF)
Dict = 'dict/dict.txt'			# dictionary
MLF = 'mlf/train.mlf' 			# master label file (MLF)
NDim = 39 						# feature dimension
HMMList = 'model/hmmlist'		# hmm list
TrainScp = 'model/train.scp'	# scp file for training data
TestScp = 'test/test.scp'
RecMLF = 'test/rec/test{ID}.rec'
RecAcc = 'test/acc/test{ID}.acc'
NumEMIter = 1
TraceLevel = '1'
NState = 10

#-----------------------------------------------#
#           utilities functions#{{{
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


# CreateProto create a hmm proto file with following specifications:
# ns - number of states
# nd - feature vector dimension
def CreateHMMTopology(dirname, hmm, ns, nd,):
	fd = open(os.path.join(dirname, hmm), 'w+')
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
#-----------------------------------------------#
#           system building script
#-----------------------------------------------#
for N in range(MAXN, MAXN+1):
    #-----------------------------------------------#
    #          data preparation
    hmmlist = BuildCommandList(N)
    os.system('rm -rf model/hmm*')
    #-----------------------------------------------#

    #-----------------------------------------------#
    #          grammar & dictionary
    CreateBNF(hmmlist, BNF)
    BNF2SLF(BNF, SLF)
    CreateDict(hmmlist, Dict)
    #-----------------------------------------------#
    #-----------------------------------------------#

    #-----------------------------------------------#
    #          EM training

    # hmmlist
    fd = open(HMMList, 'w+')
    for hmm in hmmlist:
        fd.write(hmm + '\n')
    fd.close()

    # train.mlf
    fd = open(MLF, 'w+')
    fd.write('#!MLF!#\n')
    for hmm in hmmlist:
        fd.write('"*/{model}.lab"\n{model}\n.\n'.format(model=hmm))
    fd.close()

    # train.scp
    fd = open(TrainScp, 'w+')
    for hmm in hmmlist:
        fd.write(os.path.join(DB, 'train', 'mfc_vad', hmm+'.mfc') + '\n')
    fd.close()

    # Create proto hmm
    for hmm in hmmlist:
        os.system('echo ../corpus/train/mfc_vad/{model}.mfc > model/proto/{model}.scp'.format(model=hmm))
        CreateHMMTopology('model/proto', hmm, NState, NDim)

    # flat start
    os.system('mkdir model/hmm0')
    for hmm in hmmlist:
        os.system(' '.join([
            'HCompV',
            '-T', TraceLevel,
            '-m',
            '-S', 'model/proto/{}.scp'.format(hmm),
            '-M', 'model/hmm0',
            'model/proto/{}'.format(hmm)
            ]))
        os.system('cat model/hmm0/s* > model/hmm0/MODEL')

    # EM
    for i in range(0, NumEMIter):
        os.system('mkdir model/hmm{}'.format(str(i+1)))
        os.system(' '.join([
            'HERest',
            '-A',
            '-D',
            '-T', TraceLevel,
            '-I', MLF,
            '-S', TrainScp,
            '-H', 'model/hmm{}/MODEL'.format(str(i)),
            '-M', 'model/hmm{}'.format(str(i+1)),
            '-m', '1',
            HMMList
        ]))
    #-----------------------------------------------#


    #-----------------------------------------------#
    #          test

    # test.scp
    fd = open(TestScp, 'w+')
    for hmm in hmmlist:
        fd.write(os.path.join(DB, 'test', 'mfc_vad', hmm+'.mfc') + '\n')
    fd.close()

    cmd = ' '.join([
        'HVite',
        '-A',
        '-D',
        '-T', TraceLevel,
        '-S', TestScp,
        '-H', 'model/hmm{}/MODEL'.format(NumEMIter),
        '-l', "'*'",
        '-i', RecMLF.format(ID = N),
        '-w', SLF,
        '-p', '0.0',
        '-n', '32', '5',
        #'-f',    # output state alignment
        Dict,
        HMMList
        ])
    print(cmd)
    os.system(cmd)

    # display result
    os.system(' '.join([
        'HResults',
        '-I', MLF,
        #'-p',
        HMMList,
        RecMLF.format(ID = N),
        '>' + RecAcc.format(ID = N)
        ]))
