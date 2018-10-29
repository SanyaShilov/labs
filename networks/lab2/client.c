#include <sys/socket.h> 
#include <netinet/in.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <arpa/inet.h>
#include <string.h>

#include "constants.h"

int main(void)
{
    int sock = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = inet_addr(IP);

    if(connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        perror("connect");
        exit(2);
    }

    char buf[BUF_SIZE];
    FILE* f = fopen("message.txt", "r");
    while (fgets(buf, BUF_SIZE, f))
    {
        send(sock, buf, strlen(buf), 0);
    }

    close(sock);
    return 0;
}
