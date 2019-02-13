#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/ioctl.h>
#include <linux/perf_event.h>
#include <asm/unistd.h>

static long
perf_event_open(struct perf_event_attr *hw_event, pid_t pid,
                int cpu, int group_fd, unsigned long flags)
{
    int ret;

    ret = syscall(__NR_perf_event_open, hw_event, pid, cpu,
                   group_fd, flags);
    return ret;
}

int main(int argc, char **argv)
{
    struct perf_event_attr pe;
    long long count;
    int fd;
    memset(&pe, 0, sizeof(struct perf_event_attr));
    pe.type = PERF_TYPE_SOFTWARE;
    pe.size = sizeof(struct perf_event_attr);
    pe.config = PERF_COUNT_SW_TASK_CLOCK;
    pe.disabled = 1;
    pe.exclude_kernel = 1;
    pe.exclude_hv = 1;
    int pid;
    scanf("%d", &pid);
    printf("pid: %d\n", pid);
    fd = perf_event_open(&pe, pid, -1, -1, 0);
    if (fd == -1) {
       fprintf(stderr, "Error opening leader %llx\n", pe.config);
       exit(EXIT_FAILURE);
    }
    ioctl(fd, PERF_EVENT_IOC_RESET, 0);
    ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);
    for (int t = 0; t < 10000000; ++t)
    {
        long long i = 0;
        for (long long j = 0; j < 100000000; ++j)
            i += j % 37;
        read(fd, &count, sizeof(long long));
        printf("Used %lld cpu clock\n", count);
    }
    ioctl(fd, PERF_EVENT_IOC_DISABLE, 0);
    close(fd);
}
