#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/ioctl.h>
#include <linux/perf_event.h>
#include <asm/unistd.h>
#include <sys/types.h>
#include <time.h>
#include <getopt.h>


static long perf_event_open(struct perf_event_attr *hw_event, pid_t pid,
                int cpu, int group_fd, unsigned long flags)
{
    int ret;
    ret = syscall(__NR_perf_event_open, hw_event, pid, cpu,
                   group_fd, flags);
    return ret;
}


int parse_time(char* str_time, int* time)
{
    *time = atoi(str_time);
    if (*time == 0)
        return -1;
    return 1;
}


int parse_pids(char* str_pids, int* pids, int* pids_count)
{
    int pid;
    *pids_count = 0;
    char* parsed = strtok(str_pids, " ,;");
    while (parsed != NULL)
    {
        pid = atoi(parsed);
        if (pid == 0)
            return -1;
        pids[*pids_count] = pid;
        ++(*pids_count);
        parsed = strtok(NULL, " ,;");
    }
    return 1;
}


int parse_args(int argc, char** argv, int* time, int* pids, int* pids_count)
{
    int result = 0;
    int c;
    struct option long_options[] = {
        {"pids", 1, 0, 0},
        {"time", 1, 0, 0},
        {0, 0, 0, 0}
    };
    int option_index = 0;
    while (1)
    {
        c = getopt_long(argc, argv, "p:t:", long_options, &option_index);
        if (c == -1)
            break;
        switch (c)
        {
            case 0:
                if (option_index == 0)
                    result += parse_pids(optarg, pids, pids_count);
                else if (option_index == 1)
                    result += parse_time(optarg, time);
                break;
            case 'p':
                result += parse_pids(optarg, pids, pids_count);
                break;
            case 't':
                result += parse_time(optarg, time);
                break;
            default:
                return -1;
        }
    }
    return result;
}


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
    fd = perf_event_open(&pe, pids[0], -1, -1, 0);
    if (fd == -1)
    {
       fprintf(stderr, "Error opening leader %llx\n", pe.config);
       exit(EXIT_FAILURE);
    }
    int end = clock() + time;
    ioctl(fd, PERF_EVENT_IOC_RESET, 0);
    ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);
    while (clock() < end)
    {
        read(fd, &count, sizeof(long long));
        printf("Used %lld cpu clock\n", count);
    }
    ioctl(fd, PERF_EVENT_IOC_DISABLE, 0);
    close(fd);
    free(pids);
    return 0;
}
