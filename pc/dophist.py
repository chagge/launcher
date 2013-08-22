#!/usr/bin/python
from Tkinter import *
import time
import sys
import asr


# global variable
RecordingPID = 0

def MouseL_Press(event):
    global RecordingPID
    RecordingPID = asr.StartRecordingForRecognition()
def MouseL_Release(event):
    global RecordingPID
    asr.EndRecordingForRecognition(RecordingPID)
    tag = asr.Recognize()
    asr.Run(tag)

def MouseR_Click(event):
    managerWindow = Toplevel(root)
    tagList = asr.GetTagList()
    c = Frame(managerWindow)
    c.pack()

    tagListbox = Listbox(c,height=22, width=25, activestyle = 'underline')
    for tag in tagList:
        tagListbox.insert(END, tag)
    uttListbox = Listbox(c, height=22, activestyle = 'underline')
    scriptText   = Text(c)

    addTagButton     = Button(c, text = 'Add tag', command = lambda:addTag(tagListbox))
    delTagButton     = Button(c, text = 'Del tag', command = lambda:delTag(tagListbox))
    playUttButton    = Button(c, text = 'Play', command = lambda : playUtt(tagListbox, uttListbox))
    addUttButton     = Button(c, text = 'Add')
    delUttButton     = Button(c, text = 'Del', command = lambda : delUtt(tagListbox, uttListbox))
    saveScriptButton = Button(c, text = 'Save', command = lambda : saveScript(tagListbox, scriptText))
    updataButton     = Button(c, text = 'Update Model', command = lambda : trainUpdate())

    tagListbox.grid(row=0, column=0, columnspan=2)
    uttListbox.grid(row=0, column=2, columnspan=3)
    scriptText.grid(row = 0, column = 5)
    addTagButton.grid(row=1, column=0)
    delTagButton.grid(row=1, column=1)
    playUttButton.grid(row=1, column=2)
    addUttButton.grid(row=1, column=3)
    delUttButton.grid(row=1, column=4)
    saveScriptButton.grid(row=1, column = 5)
    updataButton.grid(row=3, column = 0, columnspan = 5)

    tagListbox.bind('<<ListboxSelect>>', lambda event : changeTag(tagListbox, uttListbox, scriptText))

    addUttButton.bind('<Button-1>', lambda event : addUttStart(tagListbox, uttListbox))
    addUttButton.bind('<ButtonRelease-1>', lambda event : addUttEnd())


def addTag(lb):
    t = time.time()
    tag = 'T' + str(int(t * 10))
    asr.Create(tag)
    lb.insert(END, tag)
    lb.activate(END)

def delTag(lb):
    idxs = lb.curselection()
    for i in idxs:
        tag = lb.get(i)
        asr.Remove(tag)
        lb.delete(i)

def changeTag(taglb, uttlb, script):
    i = taglb.curselection()
    tag = taglb.get(i)
    utts = asr.GetAllUtts(tag)

    uttlb.delete(0, END)
    for utt in utts:
        uttlb.insert(END, utt)

    script.delete('1.0', END)
    lines = asr.GetScript(tag)
    for l in lines:
        script.insert(END, l)

def addUttStart(taglb, uttlb):
    global RecordingPID
    t = time.time()
    utt = 'S' + str(int(t*10)) + '.htk'
    tag = taglb.get(ACTIVE)
    RecordingPID = asr.StartRecordingUtt(tag, utt)
    uttlb.insert(END, utt)

def addUttEnd():
    global RecordingPID
    asr.EndRecordingUtt(RecordingPID)

def playUtt(taglb, uttlb):
    ti = taglb.get(ACTIVE)
    ui = uttlb.get(ACTIVE)
    #print(ti, ui)
    asr.PlayUtt(ti, ui)

def addUtt(taglb, uttlb):
    global RecordingPID
    tag = taglb.get(ACTIVE)
    asr.StartRecordingForTag(tag)

def delUtt(taglb, uttlb):
    ti = taglb.get(ACTIVE)
    ui = uttlb.get(ACTIVE)
    asr.RemoveUtt(ti, ui)
    uttlb.delete(ACTIVE)

def saveScript(taglb, text):
    op = text.get('1.0', END)
    tag = taglb.get(ACTIVE)
    asr.WriteOperation(tag, op)

def trainUpdate():
    asr.TrainAll()
    asr.UpdateASR()

#def MouseR_Press(event):
#    global curtag, RecordingPID
#    curtag = 'T' + str(int(time.time()))
#    create(curtag)
#    utt = os.path.join(ASR_ROOT, 'train', curtag, 'utt', 'raw', curtag+'.htk')
#    cmd = [
#        REC,
#        '-r' , SampleRate,
#        '-c',  NumChannels,
#        '--buffer', BufferSize,
#        utt
#        ]
#    p = subprocess.Popen(cmd)
#    RecordingPID = p.pid
#
#def MouseR_Release(event):
#    global curtag, RecordingPID
#    os.kill(RecordingPID, signal.SIGINT)
#    time.sleep(KILL_WAIT)
#    #os.system('kill -s 2 ' + str(RecordingPID))
#    train(curtag)
#    updateASR()

root = Tk()

frame = Frame(root, width=100, height=100)
frame.pack()
frame.bind("<Button-1>", MouseL_Press)
frame.bind("<ButtonRelease-1>", MouseL_Release)
frame.bind("<Button-3>", MouseR_Click)
#frame.bind("<ButtonRelease-3>", MouseR_Release)

root.mainloop()
