#include "common.h"


int main(int argc, char** argv)
{
    int time;
    int* pids = malloc(10 * sizeof(int));
    int pids_count = 0;
    char* message_to_kernel = malloc(1000);
    int result = parse_args(argc, argv, &time, pids, &pids_count, message_to_kernel);
    if (result != 2)
    {
        free(message_to_kernel);
        printf("invalid arguments, usage: main --time TIME --pids 'PID1 PID2 ...'\n");
        return -1;
    }

    char* command = malloc(1000);
    sprintf(command, "echo '%s' > /proc/course_project 2>/dev/null", message_to_kernel);
    system("sudo truncate -s 0 /var/log/syslog");
    system(command);
    grep_logs(pids, pids_count);

    free(pids);
    free(message_to_kernel);
    free(command);
    return 0;
}
