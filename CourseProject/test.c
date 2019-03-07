#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/ioctl.h>
#include <linux/perf_event.h>
#include <asm/unistd.h>
#include <sys/types.h>
#include <sys/time.h>
#include <time.h>
#include <getopt.h>
#include <dirent.h>
#include <wait.h>


int high_cpu_usage(void)
{
    int i = 0, j;
    while(1)
    {
        for (i = 0; i < 10000; ++i)
        {
            j = (j * j + 137) % (i * i + 173);
        }
        usleep(100);
    }
    return j;
}


int high_memory_usage(void)
{
    int** m = malloc(1000 * sizeof(int*));
    int i;
    for (i = 0; i < 1000; ++i)
        m[i] = NULL;
    while(1)
    {
        i = rand() % 1000;
        if (m[i])
        {
            free(m[i]);
            m[i] = NULL;
        }
        else
        {
            m[i] = malloc(1000000);
        }
        usleep(10);
    }
    return i;
}


int high_children_count(void)
{
    int max = rand() % 20;
    int current = 0;
    int status;
    while (1)
    {
        ++current;
        int pid = fork();
        usleep(3000);
        if (!pid)
            execl("mysleep", " ", NULL);
        else
        {
            if (current > max)
            {
                for (int i = 0; i < current - max; ++i)
                    wait(&status);
                current = max;
                max = rand() % 20;
            }
        }
    }
    return current;
}


int high_files_count(void)
{
    FILE** files = malloc(10 * sizeof(FILE*));
    int (*pipes)[2] = malloc(10 * sizeof(int*));
    for (int i = 0; i < 10; ++i)
    {
        files[i] = NULL;
        pipes[i][0] = NULL;
    }
    while (1)
    {
        int r = rand() % 10;
        if (rand() % 2)
        {
            if (files[r])
            {
                fclose(files[r]);
                files[r] = NULL;
            }
            else
            {
                files[r] = fopen("tmp", "r");
            }
        }
        else
        {
            if (pipes[r][0])
            {
                close(pipes[r][0]);
                close(pipes[r][1]);
                pipes[r][0] = NULL;
            }
            else
            {
                pipe(pipes[r]);
            }
        }
        usleep(3000);
    }
    return pipes[0][0];
}


int main(void)
{
    srand(time(NULL));
    if (fork() == 0)
        return high_cpu_usage();
    if (fork() == 0)
        return high_memory_usage();
    if (fork() == 0)
        return high_children_count();
    if (fork() == 0)
        return high_files_count();
    sleep(100000);
    return 0;
}
