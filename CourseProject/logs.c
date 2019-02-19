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
        system(command);
        int delayed = clock() + 10000;
        while (clock() < delayed);
        sprintf(command, "grep -Po 'course project %d \\K.*' /var/log/syslog >> %s", pids[i], filename);
        system(command);
    }
    free(command);
    free(filename);
}
