#include <stdlib.h>


int main(void)
{
    system("sudo insmod helloworld.ko");
    system("sudo rmmod helloworld");
    return 0;
}

