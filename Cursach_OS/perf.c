#include "common.h"


static long perf_event_open(struct perf_event_attr *hw_event, pid_t pid,
                int cpu, int group_fd, unsigned long flags)
{
    int ret;

    ret = syscall(__NR_perf_event_open, hw_event, pid, cpu,
                   group_fd, flags);
    return ret;
}


int* open_fds(int* pids, int pids_count)
{
    int* fds = malloc(pids_count * sizeof(int));
    for (int i = 0; i < pids_count; ++i)
    {
        struct perf_event_attr pe;
        memset((&pe), 0, sizeof(struct perf_event_attr));
        pe.type = PERF_TYPE_SOFTWARE;
        pe.size = sizeof(struct perf_event_attr);
        pe.config = PERF_COUNT_SW_TASK_CLOCK;
        pe.disabled = 1;
        pe.exclude_kernel = 1;
        pe.exclude_hv = 1;
        fds[i] = perf_event_open(&pe, pids[i], -1, -1, 0);
        ioctl(fds[i], PERF_EVENT_IOC_RESET, 0);
        ioctl(fds[i], PERF_EVENT_IOC_ENABLE, 0);
    }
    return fds;
}


void close_fds(int* fds, int pids_count)
{
    for (int i = 0; i < pids_count; ++i)
    {
        ioctl(fds[i], PERF_EVENT_IOC_DISABLE, 0);
        close(fds[i]);
    }
    free(fds);
}
