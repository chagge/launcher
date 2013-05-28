#!/usr/bin/python
import os, sys
from util import *
#-----------------------------------------------#
#          parameter setting 
DB = '../corpus'				# database
N = 20							# first N utterence in DB
BNF = 'grammar/gram.bnf'		# BNF defined grammar
SLF = 'grammar/gram.slf'		# standard lattice file (SLF)
Dict = 'dict/dict.txt'			# dictionary
MLF = 'mlf/train.mlf' 			# master label file (MLF)
NDim = 39 						# feature dimension
HMMList = 'model/hmmlist'		# hmm list
TrainScp = 'model/train.scp'	# scp file for training data
TestScp = 'test/test.scp'
RecResult = 'test/test.rec'
EMIter = 2
TraceLevel = '1'


#-----------------------------------------------#

#-----------------------------------------------#
#          data preparation
hmmlist = BuildCommandList(N)
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
	fd.write(os.path.join(DB, 'train', 'mfc', hmm+'.mfc') + '\n')
fd.close()

# Create proto hmm
for hmm in hmmlist:
	os.system('echo ../corpus/train/mfc/{model}.mfc > model/proto/{model}.scp'.format(model=hmm))
	CreateProto(hmm, 10, NDim)

# flat start
for hmm in hmmlist:
	os.system(' '.join([
		'HCompV',
		'-T', TraceLevel,
		'-m',
		'-S', 'model/proto/{model}.scp'.format(model=hmm),
		'-M', 'model/hmm0',
		'model/proto/{model}'.format(model=hmm)
		]))
	os.system('cat model/hmm0/s* > model/hmm0/MODEL')

#EM
for i in range(0, EMIter):
	os.system('rm -rf model/hmm{}'.format(str(i+1)))
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
	fd.write(os.path.join(DB, 'test', 'mfc', hmm+'.mfc') + '\n')
fd.close()

os.system(' '.join([
	'HVite',
	'-A',
	'-D',
	'-T', TraceLevel,
	'-S', TestScp,
	'-H', 'model/hmm{}/MODEL'.format(EMIter),
	'-l \*',
	'-i', RecResult,
	'-w', SLF,
	'-p', '0.0',
	Dict,
	HMMList
	]))

# display result
os.system(' '.join([
	'HResults',
	'-I', MLF,
	//'-p',
	HMMList,
	RecResult
	]))
