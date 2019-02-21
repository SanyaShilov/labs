#include "common.h"


void grep_logs(int* pids, int pids_count)
{
    char* command = malloc(1000);
    char* filename = malloc(100);
    for (int i = 0; i < pids_count; ++i)
    {
        sprintf(filename, "%d.log", pids[i]);
        sprintf(command, "echo '%20s | %20s | %20s | %10s | %10s | %10s | %10s' > %s",
                "Time", "CPU", "Memory", "Children", "Files", "Sockets", "Pipes", filename);
        //system(command);
        int delayed = clock() + 100000;
        while (clock() < delayed);
        sprintf(command, "grep 'course project' /var/log/syslog");
        printf("%s\n", command);
        system(command);
    }
    free(command);
    free(filename);
}
