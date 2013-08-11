/********* ASR engine configuration *************/

const char * ASR_ROOT = "/home/jiayu/dophist/launcher/asr/dev/ASR_ROOT";
const int NumEMIter = 3;

/* asr engine interface */

int InitEnv(void);

int CreateTag(int tag);
int AddUtterance(int tag, const char * utt);
int TrainTag(int tag);

int RemoveTag(int tag);

int Decode(const char * utt);

