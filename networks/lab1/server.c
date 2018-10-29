#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <stdio.h>

#include "constants.h"

int sock;

void sigint_handler(int signum)
{
    close(sock);
    exit(1);
}

int main(void)
{
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    signal(SIGINT, sigint_handler);

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = inet_addr(IP);

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        close(sock);
        perror("bind");
        exit(2);
    }

    char buf[BUF_SIZE];
    int size;
    while (1)
    {
        size = recv(sock, buf, sizeof(buf), 0);
        buf[size] = 0;
        printf("%s\n", buf);
    }
}
