#!/usr/bin/python
import os, sys
from util import *
#-----------------------------------------------#
#          parameter setting 
DB = '../corpus'				# database
N = 5							# first N utterence in DB
BNF = 'grammar/gram.bnf'		# BNF defined grammar
SLF = 'grammar/gram.slf'		# standard lattice file (SLF)
Dict = 'dict/dict.txt'			# dictionary
MLF = 'mlf/mlf.txt' 			# master label file (MLF)
NDim = 39 						# feature dimension
#-----------------------------------------------#

#-----------------------------------------------#
#          data preparation
cmds = BuildCommandList(N)
#-----------------------------------------------#

#-----------------------------------------------#
#          grammar & dictionary
CreateBNF(cmds, BNF)
BNF2SLF(BNF, SLF)
CreateDict(cmds, Dict)
#-----------------------------------------------#
#          MLF
CreateMLF(cmds, MLF)
#-----------------------------------------------#

#-----------------------------------------------#
#          model training
for cmd in cmds:
	os.system('echo ../corpus/train/mfc/{hmm}.mfc > model/proto/{hmm}.scp'.format(hmm=cmd))
	CreateProto(cmd, 10, NDim)
for cmd in cmds:
	os.system('HCompV -T 7 -m -S model/proto/{hmm}.scp -M model/hmm0 model/proto/{hmm}'.format(hmm=cmd))
