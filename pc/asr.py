import os
import subprocess
import signal
import time
import struct

ROOT     = os.getcwd()
ARC      = 'Mac64'  # 'Mac64'
ASR_ROOT = os.path.join(ROOT, 'ASR_ROOT')
BIN         = os.path.join(ROOT, 'bin', ARC)

# sox configuration
SampleRate = '8000'
NumChannels = '1'
if ARC.startswith('Linux'):
    BufferSize = '100'   # buffer size(in samples)
elif ARC.startswith('Mac'):
    BufferSize = '1000'   
else:
    BufferSize = '100'
    print('Warning: Unknown architecture\n')

KILL_WAIT = 0.5

# bin setup
REC         = os.path.join(BIN, 'rec')
PLAY        = os.path.join(BIN, 'play')
VAD         = os.path.join(BIN, 'vad')
HCOMPV      = os.path.join(BIN, 'HCompV')
HCOPY       = os.path.join(BIN, 'HCopy')
HEREST      = os.path.join(BIN, 'HERest')
if ARC.startswith('Linux'):
    HPARSE  = os.path.join(BIN, 'HParse')
elif ARC.startswith('Mac'):
    HPARSE  = os.path.join(BIN, 'HParse.py')
HVITE       = os.path.join(BIN, 'HVite')

# training configuration
HCOPY_CFG = os.path.join(ROOT, 'config', 'hcopy.cfg')
TRACE_LEVEL = '1'
NumEMIter = 3
NDIM = 12

# decoding configuration
BNF         = os.path.join(ASR_ROOT, 'decode', 'gram.bnf')
SLF         = os.path.join(ASR_ROOT, 'decode', 'gram.slf')
DICT        = os.path.join(ASR_ROOT, 'decode', 'dict')
AMLIST      = os.path.join(ASR_ROOT, 'decode', 'amlist')
AM          = os.path.join(ASR_ROOT, 'decode', 'model')
REC_MLF     = os.path.join(ASR_ROOT, 'decode', 'rec.txt')
DECODE_SCP  = os.path.join(ASR_ROOT, 'decode', 'decode.scp')
decRaw      = os.path.join(ASR_ROOT, 'decode', 'raw.htk')
decVad      = os.path.join(ASR_ROOT, 'decode', 'vad.htk')
decFea      = os.path.join(ASR_ROOT, 'decode', 'fea.mfc')

def GetNumState(tag):
    tagRoot = os.path.join(ASR_ROOT, 'train', tag)
    NumFrames = 0
    fs = os.listdir(os.path.join(tagRoot, 'utt', 'fea'))
    for f in fs:
        fd = open(os.path.join(tagRoot, 'utt', 'fea', f), 'rb')
        NumFrames += struct.unpack('>i', fd.read(4))[0]  #for Big-Endian
        fd.close()
    NumFiles = len(fs)
    NumStates = int(float(NumFrames)/NumFiles/6)
    print(NumStates)
    return NumStates

def CreateHMMTopology(tag, ns, nd):
    tagRoot = os.path.join(ASR_ROOT, 'train', tag)
    fd = open(os.path.join(tagRoot, 'am', 'proto', tag), 'w+')
    mean = ''
    var  = ''
    for k in range(0, nd):
        mean += '0.0 '
        var  += '1.0 '

    fd.write(''.join([
        '~o <VecSize> ' + str(nd) + ' <MFCC_Z>\n', 
        '~h "{}"\n'.format(tag),
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
        elif s != (ns -1):
            row[s]   = '0.9'
            row[s+1] = '0.1'

        fd.write('\t' + ' '.join(row) + '\n')
    fd.write('<EndHMM>\n')
    fd.close()


#------------ exporting interface -------------------
def StartRecordingForRecognition():
    cmd = [
        REC,
        '-r' , SampleRate,
        '-c',  NumChannels,
        # '--buffer', BufferSize,
        decRaw
        ]
    p = subprocess.Popen(cmd)
    return p.pid

def EndRecordingForRecognition(PID):
    os.kill(PID, signal.SIGINT)
    time.sleep(KILL_WAIT)

def StartRecordingUtt(tag, utt):
    cmd = [
       REC,
        '-r' , SampleRate,
        '-c',  NumChannels,
        # '--buffer', BufferSize,
        os.path.join(ASR_ROOT, 'train', tag, 'utt', 'raw', utt)
        ]
    p = subprocess.Popen(cmd)
    return p.pid

def EndRecordingUtt(PID):
    os.kill(PID, signal.SIGINT)
    time.sleep(KILL_WAIT)

def Run(tag):
    print('running ' + str(tag))
    os.system('sh ' + os.path.join(ASR_ROOT, 'train', tag, 'op.sh'))

def TrainAll():
    tags = os.listdir(os.path.join(ASR_ROOT, 'train'))
    for tag in tags:
        Train(tag)

def UpdateASR():
    tags = os.listdir(os.path.join(ASR_ROOT, 'train'))
    print(tags)
    # create amlist
    fd = open(AMLIST, 'w+')
    for t in tags:
        fd.write(t + '\n')
    fd.close()
    # create BNF grammar
    fd = open(BNF, 'w+')
    buf = '$command = ' + ' | \n'.join(tags) + ';\n' + '($command)\n'
    fd.write(buf)
    fd.close()
    # create Standard Lattice File(SLF)
    subprocess.call([
        HPARSE,
        BNF,
        SLF
    ])
    # create dictionary
    fd = open(DICT, 'w+')
    for tag in tags:
        buf = tag + '\t' + tag + '\n'
        fd.write(buf)
    fd.close()
    # collect tag models
    if os.path.isfile(AM):
        os.remove(AM)
        os.system('touch ' + AM)
    for tag in tags:
        cmd = [
            'cat',
            os.path.join(ASR_ROOT, 'train', tag, 'am', 'iter'+str(NumEMIter), tag),
            '>>',
            AM
        ]
        os.system(' '.join(cmd))
    # hcopy.scp in decoder
    fd = open(os.path.join(ASR_ROOT, 'decode', 'hcopy.scp'), 'w+')
    fd.write(' '.join([
        decVad,
        '\t',
        decFea,
        '\n',
        ]))
    fd.close()
    # decode.scp
    fd = open(os.path.join(ASR_ROOT, 'decode', 'decode.scp'), 'w+')
    fd.write(decFea + '\n')
    fd.close()

def Recognize():
    decoderRoot = os.path.join(ASR_ROOT, 'decode')
    subprocess.call([
        VAD,
        os.path.join(decoderRoot, decRaw),
        os.path.join(decoderRoot, decVad)
        ])
    
    subprocess.call([
        HCOPY,
        '-A',
        '-D',
        '-T', TRACE_LEVEL,
        '-C', HCOPY_CFG,
        '-S', os.path.join(decoderRoot, 'hcopy.scp')
        ])

    subprocess.call([
        HVITE,
        '-A',
        '-D',
        '-T', TRACE_LEVEL,
        '-S', DECODE_SCP,
        '-H', os.path.join(decoderRoot, 'model'),
        '-l', '*',
        '-i', REC_MLF, 
        '-w', SLF,
        '-p', '0.0',
        '-n', '32', '5',    # output n-best result for further refinement
        #'-f',              # output state alignment
        DICT,
        AMLIST
        ])

    tag = open(REC_MLF, 'r').readlines()[2].split()[2]
    print(tag)
    return tag

def Create(tag):
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag))
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag, 'utt'))
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag, 'utt', 'raw'))
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag, 'utt', 'vad'))
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag, 'utt', 'fea'))
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag, 'am'))
    os.makedirs(os.path.join(ASR_ROOT, 'train', tag, 'am', 'proto'))
    for i in range(0, NumEMIter+1):  # [0, NumEMIter]
        os.mkdir(os.path.join(ASR_ROOT, 'train', tag, 'am', 'iter'+str(i)))
 
#def addUtterToTag(audio, tag):

def Train(tag):
    tagRoot = os.path.join(ASR_ROOT, 'train', tag)
    # amlist
    fd = open(os.path.join(tagRoot, 'amlist'), 'w+')
    fd.write(tag + '\n')
    fd.close()
    # dict
    fd = open(os.path.join(tagRoot, 'dict'), 'w+')
    fd.write(tag + '\t' + tag + '\n')
    fd.close()
    # mlf
    fd = open(os.path.join(tagRoot, 'train.mlf'), 'w+')
    buf = '\n'.join([
        '#!MLF!#',
        '"{}"'.format(os.path.join(tagRoot,'utt','fea','*.lab')),
        tag,
        '.\n'
        ])
    fd.write(buf)
    fd.close()

    # VAD: raw -> vad
    for f in os.listdir(os.path.join(tagRoot, 'utt', 'raw')):
        cmd = [
                VAD,
                os.path.join(tagRoot, 'utt', 'raw', f),
                os.path.join(tagRoot, 'utt', 'vad', f)
              ]
        print(cmd)
        subprocess.call(cmd)

    # feature extraction: vad -> fea 
    hcopy_scp = os.path.join(tagRoot, 'utt', 'hcopy.scp')
    fd = open(hcopy_scp, 'w+')
    for f in os.listdir(os.path.join(tagRoot, 'utt', 'vad')):
        [name, ext] = f.split('.')
        buf = ' '.join([
            os.path.join(tagRoot, 'utt', 'vad', f),
            os.path.join(tagRoot, 'utt', 'fea', name+'.mfc'),
            '\n'
            ])
        fd.write(buf)
    fd.close()
    cmd = [
            HCOPY,
            '-A',
            '-D',
            '-T', '3',
            '-C', HCOPY_CFG,
            '-S', hcopy_scp,
          ]
    subprocess.call(cmd)

    # train.scp
    train_scp = os.path.join(tagRoot, 'train.scp')
    fd = open(train_scp, 'w+')
    for f in os.listdir(os.path.join(tagRoot, 'utt', 'fea')):
        fd.write(os.path.join(tagRoot, 'utt', 'fea', f) + '\n')
    fd.close()

    ns = GetNumState(tag)
    CreateHMMTopology(tag, ns, NDIM)

    # flat-start initialization
    subprocess.call([
            HCOMPV,
            '-T', TRACE_LEVEL,
            '-f', '0.15',
            '-m',
            '-S', train_scp,
            '-M', os.path.join(tagRoot, 'am', 'iter0'),
            os.path.join(tagRoot, 'am', 'proto', tag)
            ])

    # EM iterative training
    for i in range(0, NumEMIter):
        subprocess.call([
            HEREST,
            '-A',
            '-D',
            '-T', TRACE_LEVEL,
            '-I', os.path.join(tagRoot, 'train.mlf'),
            '-S', os.path.join(tagRoot, 'train.scp'),
            '-m', '1',
            '-H', os.path.join(tagRoot, 'am', 'iter{}'.format(i), tag),
            '-H', os.path.join(tagRoot, 'am', 'iter{}'.format(i), 'vFloors'),
            '-M', os.path.join(tagRoot, 'am', 'iter{}'.format(i+1)),
            os.path.join(tagRoot, 'amlist')
        ])

def Remove(tag):
    os.system('rm -rf ' + os.path.join(ASR_ROOT, 'train', tag))
    print(tag + ' removed')

def GetTagList():
    return os.listdir(os.path.join(ASR_ROOT, 'train'))
def GetUttList(tag):
    return os.listdir(os.path.join(ASR_ROOT, 'train', tag, 'utt', 'raw'))
def GetOperation(tag):
    opfile = os.path.join(ASR_ROOT, 'train', tag, 'op.sh')
    if os.path.exists(opfile):
        lines = open(opfile, 'r').readlines()
        return lines
    return []
def PlayUtt(tag, utt):
    print('playing ' + os.path.join(ASR_ROOT, 'train', tag, 'utt', 'raw', utt))
    subprocess.call([
            PLAY,
            os.path.join(ASR_ROOT, 'train', tag, 'utt', 'raw', utt)
        ])
def RemoveUtt(tag,utt):
    print('removing ' + os.path.join(ASR_ROOT, 'train', tag, 'utt', 'raw', utt))
    subprocess.call([
            'rm',
            os.path.join(ASR_ROOT, 'train', tag, 'utt', 'raw', utt)
        ])

def WriteOperation(tag, op):
    fd = open(os.path.join(ASR_ROOT, 'train', tag, 'op.sh'), 'w+')
    for l in op:
        fd.write(l)
    fd.close()
