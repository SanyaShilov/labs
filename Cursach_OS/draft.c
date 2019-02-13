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

    int* fds = open_fds(pids, pids_count);

    long long count;
    int end = clock() + time;

    for (int i = 0; i < pids_count; ++i)
    {
        ioctl(fds[i], PERF_EVENT_IOC_RESET, 0);
        ioctl(fds[i], PERF_EVENT_IOC_ENABLE, 0);
    }

    while (clock() < end)
    {
        for (int i = 0; i < pids_count; ++i)
        {
            read(fds[i], &count, sizeof(long long));
            printf("pid %d used %lld cpu clock\n", pids[i], count);
        }
    }

    for (int i = 0; i < pids_count; ++i)
        ioctl(fds[i], PERF_EVENT_IOC_DISABLE, 0);

    close_fds(fds, pids_count);
    free(pids);
    return 0;
}
