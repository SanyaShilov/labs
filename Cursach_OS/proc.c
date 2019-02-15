#include "common.h"


int main(int argc, char** argv)
{
    int time;
    int* pids = malloc(100 * sizeof(int));
    int pids_count = 0;
    int result = parse_args(argc, argv, &time, pids, &pids_count);
    if (result != 2)
    {
        printf("invalid arguments\n");
        return -1;
    }

    FILE** logs = open_logs(pids, pids_count);
    int* fds = open_fds(pids, pids_count);

    long long count;
    int end = clock() + time;

    while (clock() < end)
    {
        for (int i = 0; i < pids_count; ++i)
        {
            read(fds[i], &count, sizeof(long long));
            fprintf(logs[i], "%lf\t%llu\n", now(), count);
        }
    }

    close_fds(fds, pids_count);
    close_logs(logs, pids_count);
    free(pids);
    return 0;
}
