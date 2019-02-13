#include "common.h"


FILE** open_logs(int* pids, int pids_count)
{
    FILE** logs = malloc(pids_count * sizeof(FILE*));
    for (int i = 0; i < pids_count; ++i)
    {
        char filename[50];
        sprintf(filename, "%d.log", pids[i]);
        logs[i] = fopen(filename, "w");
    }
    return logs;
}


void close_logs(FILE** logs, int pids_count)
{
    for (int i = 0; i < pids_count; ++i)
        fclose(logs[i]);
    free(logs);
}
