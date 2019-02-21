#include "common.h"


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


int parse_args(int argc, char** argv, int* time, int* pids, int* pids_count, char* message_to_kernel)
{
    char* c_time = malloc(100);
    char* c_pids = malloc(900);
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
                {
                    strcpy(c_pids, optarg);
                    result += parse_pids(optarg, pids, pids_count);
                }
                else if (option_index == 1)
                {
                    strcpy(c_time, optarg);
                    result += parse_time(optarg, time);
                }
                break;
            case 'p':
                strcpy(c_pids, optarg);
                result += parse_pids(optarg, pids, pids_count);
                break;
            case 't':
                strcpy(c_time, optarg);
                result += parse_time(optarg, time);
                break;
            default:
                return -1;
        }
    }
    if (result == 2)
        sprintf(message_to_kernel, "%s", c_pids);
    free(c_time);
    free(c_pids);
    return result;
}
