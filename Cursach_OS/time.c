#include "common.h"


double now()
{
    struct timeval tv;
    gettimeofday(&tv,NULL);
    return tv.tv_sec + (double)tv.tv_usec / 1000000;
}
