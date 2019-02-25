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


int main(void)
{
    fork();
    sleep(100000);
    return 0;
}

