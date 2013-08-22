#!/usr/bin/python
from Tkinter import *
import time
import sys
import asr


# global variable
RecordingPID = 0

# ------------------  -----------------------------
def MouseL_Press(event):
    global RecordingPID
    RecordingPID = asr.StartRecordingForRecognition()
def MouseL_Release(event):
    global RecordingPID
    asr.EndRecordingForRecognition(RecordingPID)
    tag = asr.Recognize()
    asr.Run(tag)

# ------------------ tag manager window -----------------------
def MouseR_Click(event):
    managerWindow = Toplevel(root)
    frame  = Frame(managerWindow)
    frame.pack()

    listbox_tag   = Listbox(frame, height=22, selectmode='SINGLE')
    tagList = asr.GetTagList()
    for tag in tagList:
        listbox_tag.insert(END, tag)

    listbox_utt = Listbox(frame, height=22, selectmode='SINGLE')
    text_operation = Text(frame)

    button_addTag = Button(
            frame, 
            text = 'Add tag', 
            command = lambda : addTag(listbox_tag)
            )

    button_delTag = Button(
            frame, 
            text = 'Del tag', 
            command = lambda : delTag(listbox_tag)
            )

    button_playUtt = Button(
            frame, 
            text = 'Play', 
            command = lambda : playUtt(listbox_tag, listbox_utt)
            )

    button_addUtt  = Button(
            frame, 
            text = 'Add'
            )
    button_addUtt.bind('<Button-1>', lambda event : addUttPress(listbox_tag, listbox_utt))
    button_addUtt.bind('<ButtonRelease-1>', lambda event : addUttRelease())

    button_delUtt = Button(
            frame, 
            text = 'Del', 
            command = lambda : delUtt(listbox_tag, listbox_utt)
            )

    button_saveOperation = Button(
            frame, 
            text = 'Save', 
            command = lambda : saveOperation(listbox_tag, text_operation)
            )

    button_update = Button(
            frame, 
            text = 'Update Model', 
            command = lambda : update()
            )

    listbox_tag.bind('<<ListboxSelect>>', lambda event : changeTag(listbox_tag, listbox_utt, text_operation))

    # widgets layout
    listbox_tag.grid(row=0, column=0, columnspan=2)
    listbox_utt.grid(row=0, column=2, columnspan=3)
    text_operation.grid(row = 0, column = 5)
    button_addTag.grid(row=1, column=0)
    button_delTag.grid(row=1, column=1)
    button_playUtt.grid(row=1, column=2)
    button_addUtt.grid(row=1, column=3)
    button_delUtt.grid(row=1, column=4)
    button_saveOperation.grid(row=1, column = 5)
    button_update.grid(row=3, column = 0, columnspan = 5)



#----------------- GUI event handlers ----------------------------
def addTag(lb):
    t = time.time()
    tag = 'T' + str(int(t * 10))
    asr.Create(tag)
    lb.insert(END, tag)
    lb.activate(END)

def delTag(lb):
    tag = lb.get(ACTIVE)
    asr.Remove(tag)
    lb.delete(ACTIVE)

def changeTag(taglb, uttlb, text_operation):
    tag = taglb.get(taglb.curselection())
    print(tag)
    uttList = asr.GetUttList(tag)

    uttlb.delete(0, END)
    for utt in uttList:
        uttlb.insert(END, utt)

    text_operation.delete('1.0', END)
    lines = asr.GetOperation(tag)
    for l in lines:
        text_operation.insert(END, l)

def addUttPress(taglb, uttlb):
    global RecordingPID
    t = time.time()
    tag = taglb.get(ACTIVE)
    utt = 'S' + str(int(t*10)) + '.htk'
    RecordingPID = asr.StartRecordingUtt(tag, utt)
    uttlb.insert(END, utt)
    uttlb.activate(END)

def addUttRelease():
    global RecordingPID
    asr.EndRecordingUtt(RecordingPID)

def playUtt(taglb, uttlb):
    ti = taglb.get(ACTIVE)
    ui = uttlb.get(ACTIVE)
    print(ti, ui)
    asr.PlayUtt(ti, ui)


def delUtt(taglb, uttlb):
    ti = taglb.get(ACTIVE)
    ui = uttlb.get(ACTIVE)
    asr.RemoveUtt(ti, ui)
    uttlb.delete(ACTIVE)
    uttlb.activate(END)

def saveOperation(taglb, text):
    op = text.get('1.0', END)
    tag = taglb.get(ACTIVE)
    asr.WriteOperation(tag, op)

def update():
    asr.TrainAll()
    asr.UpdateASR()

root = Tk()

frame = Frame(root, width=100, height=100)
frame.pack()
frame.bind("<Button-1>", MouseL_Press)
frame.bind("<ButtonRelease-1>", MouseL_Release)
frame.bind("<Button-3>", MouseR_Click)
#frame.bind("<ButtonRelease-3>", MouseR_Release)

root.mainloop()
