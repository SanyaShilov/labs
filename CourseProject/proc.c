#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <asm/unistd.h>
#include <sys/types.h>
#include <sys/time.h>
#include <time.h>
#include <getopt.h>


int main(int argc, char** argv)
{

    char data[1000];
    FILE* f = fopen("/proc/course_project", "r");
    fgets(data, 1000, f);
    printf("data %s\n", data);
    return 0;
}

