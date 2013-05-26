#!/usr/bin/python
import os, sys
import util
#-----------------------------------------------#
#          <parameter setting> 
#-----------------------------------------------#
# library size
N = 5
# BNF defined grammar
BNF = 'grammar/gram.bnf'		
# standard lattice file (SLF)
SLF = 'grammar/gram.slf'		
# dictionary
DICT = 'dict/dict.txt'
# master label file (MLF)
MLF = 'mlf/mlf.txt'
#-----------------------------------------------#
#          </parameter setting> 
#-----------------------------------------------#

cmds = util.BuildCommandList(N)
# grammar
util.GenBNF(cmds, BNF)
util.BNF2SLF(BNF, SLF)
# dict
util.GenDICT(cmds, DICT)
# MLF
util.GenMLF(cmds, MLF)

