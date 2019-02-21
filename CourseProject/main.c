#include "common.h"


int main(int argc, char** argv)
{
    int i;
    int time;
    int* pids = malloc(100 * sizeof(int));
    int pids_count = 0;
    char* message_to_kernel = malloc(1000);
    int result = parse_args(argc, argv, &time, pids, &pids_count, message_to_kernel);
    if (result != 2)
    {
        free(pids);
        free(message_to_kernel);
        printf("invalid arguments, usage: main --time TIME --pids 'PID1 PID2 ...'\n");
        return -1;
    }

    FILE* f = fopen("/proc/course_project", "w");
    fprintf(f, "%s", message_to_kernel);
    fclose(f);

    FILE** files = malloc(100 * sizeof(int));
    for (i = 0; i < pids_count; ++i)
    {
        char filename[100];
        sprintf(filename, "%d.log", pids[i]);
        files[i] = fopen(filename, "w");
        fprintf(files[i], "%20s | %20s | %20s | %10s | %10s | %10s | %10s\n",
                "Time", "CPU", "Memory", "Children", "Files", "Sockets", "Pipes");
    }
    char data[1000];
    f = fopen("/proc/course_project", "r");

    for (int j = 0; j < time; ++j)
    {
        for (i = 0; i < pids_count; ++i)
        {
            fgets(data, 1000, f);
            fprintf(files[i], "%s", data);
        }
    }

    for (i = 0; i < pids_count; ++i)
        fclose(files[i]);
    fclose(f);
    free(files);
    free(pids);
    free(message_to_kernel);
    return 0;
}
