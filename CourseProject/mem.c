#include "common.h"


enum filetype
  {
    unknown,
    fifo,
    chardev,
    directory,
    blockdev,
    normal,
    symbolic_link,
    sock,
    whiteout,
    arg_directory
  };


int main(void)
{
    FILE* f = fopen("testfile", "w");
    FILE* f2 = fopen("testfile2", "w");
    fork();
    int* mem = malloc(100000000);
    struct dirent *next;
    DIR *dirp;
    dirp = opendir("/home/sanyash/myrepos");
    next = readdir(dirp);
    switch (next->d_type)
    {
                case DT_BLK:  printf("blockdev\n");		break;
                case DT_CHR:  printf("chardev\n");		break;
                case DT_DIR:  printf("directory\n");		break;
                case DT_FIFO: printf("fifo\n");		break;
                case DT_LNK:  printf("link\n");	break;
                case DT_REG:  printf("normal\n");		break;
                case DT_SOCK: printf("sock\n");		break;
    }
    fclose(f);
    sleep(100000);
    free(mem);
    fclose(f2);
    return 0;
}
