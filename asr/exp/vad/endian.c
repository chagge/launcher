#include <stdio.h>

int main() 
{
    int i = 1;
    printf("%d", (int)((*(char*)&i) == 1));
}
