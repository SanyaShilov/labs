#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <asm/unistd.h>
#include <sys/types.h>
#include <sys/time.h>
#include <time.h>
#include <getopt.h>


#define DEBUG printf("debug %s %d\n", __FUNCTION__, __LINE__);


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
        printf("invalid arguments, usage: main --time MILLISECONDS --pids 'PID1 PID2 ...'\n");
        return -1;
    }

    FILE* f = fopen("/proc/course_project", "w");
    fprintf(f, "%s", message_to_kernel);
    fclose(f);

    FILE** files = malloc(100 * sizeof(int));
    for (i = 0; i < pids_count; ++i)
    {
        char filename[100];
        sprintf(filename, "./log/%d.log", pids[i]);
        files[i] = fopen(filename, "w");
        fprintf(files[i], "%20s | %20s | %20s | %10s | %10s | %10s | %10s\n",
                "Time", "CPU", "Memory", "Children", "Files", "Sockets", "Pipes");
    }

    char data[1000];
    f = fopen("/proc/course_project", "r");
    struct timeval tv1, tv2;
    for (int t = 0; t < time; ++t)
    {
        gettimeofday(&tv1, NULL);
        for (i = 0; i < pids_count; ++i)
        {
            fgets(data, 1000, f);
            fprintf(files[i], "%s", data);
        }
        gettimeofday(&tv2, NULL);
        usleep(1000 - (tv2.tv_usec - tv1.tv_usec) + (tv2.tv_sec - tv1.tv_sec) * 1000000); 
    }

    for (i = 0; i < pids_count; ++i)
        fclose(files[i]);
    fclose(f);
    free(files);
    free(pids);
    free(message_to_kernel);
    return 0;
}
