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
#include <time.h>
#include <getopt.h>

int parse_time(char* str_time, int* time);
int parse_pids(char* str_pids, int* pids, int* pids_count);
int parse_args(int argc, char** argv, int* time, int* pids, int* pids_count);

int* open_fds(int* pids, int pids_count);
void close_fds(int* fds, int pids_count);

FILE** open_logs(int* pids, int pids_count);
void close_logs(FILE** logs, int pids_count);

#endif // COMMON_H
