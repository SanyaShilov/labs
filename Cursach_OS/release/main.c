#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>


int main(void)
{
    system("sudo truncate -s 0 /var/log/syslog");
    system("sudo rmmod cursach  2>/dev/null");
    system("make >/dev/null");
    system("sudo insmod cursach.ko");
    system("echo go > /proc/cursach");
    for (int i = 0; i < 10; ++i)
    {
        system("cat /proc/cursach");
    }
    system("grep -Po \".*cursach \\K.*\" /var/log/syslog >tmp");
    return 0;
}

