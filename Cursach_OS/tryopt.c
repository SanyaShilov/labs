#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
    int flags, opt;
    int nsecs, tfnd;

   nsecs = 0;
    tfnd = 0;
    flags = 0;
    while ((opt = getopt(argc, argv, "p:t:")) != -1) {
        switch (opt) {
        case 'p':
            printf("%s\n", optarg);
            break;
        case 't':
            nsecs = atoi(optarg);
            printf("%d\n", nsecs);
            break;
        default:
            exit(EXIT_FAILURE);
        }
    }

   exit(EXIT_SUCCESS);
}

