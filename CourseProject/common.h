#ifndef COMMON_H
#define COMMON_H

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

int parse_time(char* str_time, int* time);
int parse_pids(char* str_pids, int* pids, int* pids_count);
int parse_args(int argc, char** argv, int* time, int* pids, int* pids_count, char *message_to_kernel);

void grep_logs(int* pids, int pids_count);

#endif // COMMON_H
