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
    FILE* f = fopen("message.txt", "rb");
    char chr;
    int i = 0;
    while (chr = getc(f) != EOF)
    {
        buf[i++] = chr;
    }

    send(sock, buf, strlen(buf), 0);

    int bytes_accepted;
    recv(sock , &bytes_accepted , sizeof(int) , 0);

    printf("file length = %d, bytes accepted = %d\n", strlen(buf), bytes_accepted); 

    close(sock);
    return 0;
}
