#include <stdlib.h>
#include <stdio.h>
#include "asr.h"

#define MAX_STR_LEN 256

int 
getTagName(int tag, char *name)
{
//    if (tag<0 || tag>=1000) {
//        fprintf(stderr, "%s: tag index out of range [0, 1000)\n", __func__);
//        return -1;
//    } 
//
//    if (tag >= 0 && tag < 10) {
//        sprintf(name, "s00%d", tag);
//    } else if (tag >= 10 && tag < 100) {
//        sprintf(name, "s0%d", tag);
//    } else if (tag >= 100 && tag < 1000) {
//        sprintf(name, "s%d", tag);
//    }
//
    sprintf(name, "tag_%d", tag);
    return 0;
}

int 
CreateTag(int tag) 
{
    char buf[MAX_STR_LEN];
    char tagName[MAX_STR_LEN];
    int k;
    getTagName(tag, tagName);
    sprintf(buf, "mkdir -p %s/train/%s", ASR_ROOT, tagName);                  system(buf);
    sprintf(buf, "mkdir -p %s/train/%s/utt", ASR_ROOT, tagName);              system(buf);
    sprintf(buf, "mkdir -p %s/train/%s/utt/pcm", ASR_ROOT, tagName);          system(buf);
    sprintf(buf, "mkdir -p %s/train/%s/utt/dat", ASR_ROOT, tagName);          system(buf);
    sprintf(buf, "mkdir -p %s/train/%s/am", ASR_ROOT, tagName);               system(buf);
    sprintf(buf, "mkdir -p %s/train/%s/am/proto", ASR_ROOT, tagName);         system(buf);
    for (k = 0; k <= NumEMIter; k++) {
        sprintf(buf, "mkdir -p %s/train/%s/am/iter%d", ASR_ROOT, tagName, k); system(buf);
    }
    sprintf(buf, "touch %s/train/%s/amlist", ASR_ROOT, tagName);              system(buf);
    sprintf(buf, "touch %s/train/%s/dict", ASR_ROOT, tagName);                system(buf);
    sprintf(buf, "touch %s/train/%s/mlf", ASR_ROOT, tagName);                 system(buf);
    sprintf(buf, "touch %s/train/%s/scp", ASR_ROOT, tagName);                 system(buf);

    return 0;
}

int
RemoveTag(int tag)
{
    char buf[MAX_STR_LEN];
    char tagName[MAX_STR_LEN];
    getTagName(tag, tagName);
    sprintf(buf, "rm -rf %s/train/%s", ASR_ROOT, tagName);
    system(buf);
    return 0;
}

int 
AddUtterance(int tag, const char *utt) 
{
    char buf[MAX_STR_LEN];
    char tagName[MAX_STR_LEN];
    getTagName(tag, tagName);
    sprintf(buf, "cp %s %s/train/%s/utt/pcm/", utt, ASR_ROOT, tagName);
    system(buf);
}

int main() 
{
    //CreateTag(1);
    //AddUtterance(1, "s000.pcm");
    //RemoveTag(1);
    return 0;
}
