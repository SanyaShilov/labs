#include <stdio.h>     /* для printf */
#include <stdlib.h>    /* для exit */
#include <getopt.h>

int
main (int argc, char **argv) {
    int c;
    int digit_optind = 0;

    while (1) {
        int this_option_optind = optind ? optind : 1;
        int option_index = 0;
        static struct option long_options[] = {
            {"time", 1, 0, 0},
            {"pids", 1, 0, 0},
            {0, 0, 0, 0}
        };

        c = getopt_long(argc, argv, "",
                 long_options, &option_index);
        if (c == -1)
            break;

        switch (c) {
        case 0:
            printf ("параметр %s", long_options[option_index].name);
            if (optarg)
                printf (" с аргументом %s", optarg);
            printf ("\n");
            break;

        case '?':
	    printf("?\n");
            break;

        default:
            printf ("?? getopt возвратило код символа 0%o ??\n", c);
        }
    }

    if (optind < argc) {
        printf ("элементы ARGV, не параметры: ");
        while (optind < argc)
            printf ("%s ", argv[optind++]);
        printf ("\n");
    }

    exit (0);
}
