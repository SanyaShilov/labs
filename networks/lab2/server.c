#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <arpa/inet.h>

#include "constants.h"

int main()
{
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in addr;

    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = inet_addr(IP);

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        perror("bind");
        exit(2);
    }

    listen(sock, 10);

    int sock_new = accept(sock, NULL, NULL);

    if (sock_new < 0)
    {
        perror("accept");
        exit(3);
    }

    char buf[BUF_SIZE];
    while (1)
    {
        int bytes_read = recv(sock_new, buf, BUF_SIZE, 0);
        if (bytes_read <= 0)
            break;
        buf[bytes_read] = 0;
        printf("%s", buf);
    }

    close(sock);
    return 0;
}
